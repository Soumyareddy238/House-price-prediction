from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
from bson.objectid import ObjectId
import pandas as pd
import numpy as np
import pymongo
import os
from sklearn.ensemble import IsolationForest
from scipy.stats import zscore

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load models
best_model = joblib.load('models/best_model.pkl')
knn = joblib.load('models/knn_recommender.pkl')
preprocessor = joblib.load('models/preprocessor.pkl')
iso_forest = joblib.load('models/anomaly_detector.pkl')
anomaly_preprocessor = joblib.load('models/anomaly_preprocessor.pkl')

# Load data for recommendations
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["House_price_prediction"]
    collection = db["properties"]
    
    # Fetch all records from MongoDB
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    
    # Drop MongoDB internal ID
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])
    
    print(f"Loaded {len(df)} records from MongoDB for app.py.")
except Exception as e:
    print(f"Error loading data for app.py: {e}")
    print("Falling back to CSV...")
    df = pd.read_csv('data/processed_dataset.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if not session.get('user_id') and not session.get('admin_logged_in'):
            return jsonify({'success': False, 'error': 'Unauthorized. Please login or signup to predict prices.', 'redirect_to_login': True})

        data = request.json
        area = float(data.get('area', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 0))
        bathrooms = int(data.get('bathrooms', 0))
        property_type = data.get('property_type', '')
        school_dist = float(data.get('nearby_school_distance', 0))
        hospital_dist = float(data.get('nearby_hospital_distance', 0))

        # Create DataFrame for prediction
        input_data = pd.DataFrame([{
            'area': area,
            'location': location,
            'bhk': bhk,
            'property_type': property_type,
            'nearby_school_distance': school_dist,
            'nearby_hospital_distance': hospital_dist,
            'bathrooms': bathrooms
        }])

        # Predict Price
        predicted_price = float(best_model.predict(input_data)[0])

        # Anomaly Detection
        anomaly_input = pd.DataFrame([{
            'area': area,
            'location': location,
            'bhk': bhk,
            'bathrooms': bathrooms,
            'price': predicted_price
        }])
        
        proc_anomaly = anomaly_preprocessor.transform(anomaly_input)
        is_anomaly = bool(iso_forest.predict(proc_anomaly)[0] == -1)  # Cast to bool for serializability

        return jsonify({
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'currency': 'INR', # Assuming Indian Context from locations/synthetic logic
            'is_anomaly': bool(is_anomaly),
            'message': 'Price seems unusually high/low given features.' if is_anomaly else 'Price is within normal range.'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        area = float(data.get('area', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 0))
        bathrooms = int(data.get('bathrooms', 0))
        property_type = data.get('property_type', '')
        school_dist = float(data.get('nearby_school_distance', 0))
        hospital_dist = float(data.get('nearby_hospital_distance', 0))

        # Create dummy input based on preferences
        input_data = pd.DataFrame([{
            'area': area,
            'location': location,
            'bhk': bhk,
            'property_type': property_type,
            'nearby_school_distance': school_dist,
            'nearby_hospital_distance': hospital_dist,
            'bathrooms': bathrooms
        }])

        # Transform using preprocessor
        proc_input = preprocessor.transform(input_data)
        
        # Get nearest neighbors
        distances, indices = knn.kneighbors(proc_input, n_neighbors=5)
        
        recommended_properties = df.iloc[indices[0]].to_dict(orient='records')
        
        return jsonify({
            'success': True,
            'recommendations': recommended_properties
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/detect_anomalies', methods=['GET', 'POST'])
def detect_anomalies():
    try:
        # 1. Load dataset from MongoDB
        cursor = collection.find({})
        df_all = pd.DataFrame(list(cursor))
        
        if df_all.empty:
            return jsonify({'success': False, 'message': 'No properties found in database.'})
            
        # 2. Select important numerical features
        features = ['area', 'bhk', 'bathrooms', 'nearby_school_distance', 'nearby_hospital_distance', 'price']
        
        # Ensure all required columns exist
        for f in features:
            if f not in df_all.columns:
                df_all[f] = 0
                
        # Drop rows with NaN in features
        df_clean = df_all.dropna(subset=features).copy()
        
        if len(df_clean) < 10:
             return jsonify({'success': False, 'message': 'Not enough valid data to detect anomalies.'})

        # 3. Train Isolation Forest model
        iso = IsolationForest(contamination=0.05, random_state=42)
        iso.fit(df_clean[features])
        
        # 4. Predict anomalies: -1 -> anomaly, 1 -> normal
        df_clean['anomaly_score'] = iso.predict(df_clean[features])
        
        # 5. Z-score for price to determine Overpriced/Underpriced
        df_clean['price_zscore'] = zscore(df_clean[features]['price'])
        
        # 6. Logic to assign status
        def assign_status(row):
            if row['anomaly_score'] == -1:
                if row['price_zscore'] > 0:
                    return 'Overpriced'
                else:
                    return 'Underpriced'
            return 'Normal'
            
        df_clean['anomaly_status'] = df_clean.apply(assign_status, axis=1)
        
        # Update MongoDB and collect results
        anomalies_list = []
        updated_count = 0
        
        for index, row in df_clean.iterrows():
            collection.update_one(
                {'_id': row['_id']},
                {'$set': {'anomaly_status': row['anomaly_status']}}
            )
            updated_count += 1
            
            if row['anomaly_status'] != 'Normal':
                prop_dict = row.to_dict()
                prop_dict['_id'] = str(prop_dict['_id'])
                anomalies_list.append(prop_dict)
                
        return jsonify({
            'success': True,
            'message': f'Successfully processed {updated_count} properties.',
            'anomalies_count': len(anomalies_list),
            'anomalous_properties': anomalies_list
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/insights', methods=['GET'])
def insights():
    # Provide simple aggregated data for frontend visualization
    try:
        # Fetch fresh data to get anomaly_status if generated
        cursor = collection.find({})
        df_current = pd.DataFrame(list(cursor))
        if df_current.empty:
            df_current = df # rollback to memory df
        elif '_id' in df_current.columns:
            df_current = df_current.drop(columns=['_id'])

        avg_price_by_loc = df_current.groupby('location')['price'].mean().to_dict()
        avg_price_by_type = df_current.groupby('property_type')['price'].mean().to_dict()
        
        # Convert NaN to None for JSON serializability
        sample_df = df_current.sample(min(200, len(df_current)))
        sample = sample_df.replace({np.nan: None}).to_dict(orient='records')

        return jsonify({
            'success': True,
            'avg_price_by_location': avg_price_by_loc,
            'avg_price_by_type': avg_price_by_type,
            'scatter_sample': sample
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match!")

        users_collection = db["users"]
        if users_collection.find_one({"username": username}):
            return render_template('signup.html', error="Username already exists!")

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({"username": username, "password": hashed_password, "role": "user"})
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users_collection = db["users"]
        user = users_collection.find_one({"username": username})

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['role'] = user.get('role', 'user')
            
            if session['role'] == 'admin':
                session['admin_logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username not in ['harikeerthi', 'soumyareddy']:
            return render_template('admin.html', error="You do not have permission to access the admin portal.")

        # 1. Check admin collection
        admin_collection = db["admin"]
        admin_user = admin_collection.find_one({"username": username})

        # 2. Check users collection
        users_collection = db["users"]
        regular_user = users_collection.find_one({"username": username})

        is_valid = False
        if admin_user and admin_user.get('password') == password:
            is_valid = True
        elif regular_user and check_password_hash(regular_user['password'], password):
            is_valid = True
        elif password == "1234":  # Fallback default admin password from earlier setup
            is_valid = True

        if is_valid:
            session['admin_logged_in'] = True
            session['username'] = username
            session['role'] = 'admin'
            
            # Auto-upgrade them to admin in the DB if they only exist as a regular user
            if regular_user and regular_user.get('role') != 'admin':
                users_collection.update_one({'_id': regular_user['_id']}, {'$set': {'role': 'admin'}})
                
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin.html', error="Invalid Credentials")
    return render_template('admin.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
        
    # Fetch all properties from MongoDB
    try:
        properties = list(collection.find({}))
        users = list(db["users"].find({}))
        stats = {
            'total_properties': len(properties),
            'locations': collection.distinct('location'),
            'avg_price': collection.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$price"}}}]).next().get('avg', 0) if properties else 0,
            'total_users': len(users)
        }
        return render_template('admin_dashboard.html', stats=stats, properties=properties, users=users)
    except Exception as e:
        return f"Error loading dashbaord: {e}"

@app.route('/admin/add', methods=['POST'])
def add_property():
    try:
        new_data = {
            'area': float(request.form.get('area')),
            'location': request.form.get('location'),
            'bhk': int(request.form.get('bhk')),
            'bathrooms': int(request.form.get('bathrooms')),
            'property_type': request.form.get('property_type'),
            'nearby_school_distance': float(request.form.get('nearby_school_distance')),
            'nearby_hospital_distance': float(request.form.get('nearby_hospital_distance')),
            'price': float(request.form.get('price'))
        }
        collection.insert_one(new_data)
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        return f"Error adding property: {e}"

@app.route('/admin/edit/<id>', methods=['GET', 'POST'])
def edit_property(id):
    try:
        property_id = ObjectId(id)
        if request.method == 'POST':
            updated_data = {
                'area': float(request.form.get('area')),
                'location': request.form.get('location'),
                'bhk': int(request.form.get('bhk')),
                'bathrooms': int(request.form.get('bathrooms')),
                'property_type': request.form.get('property_type'),
                'nearby_school_distance': float(request.form.get('nearby_school_distance')),
                'nearby_hospital_distance': float(request.form.get('nearby_hospital_distance')),
                'price': float(request.form.get('price'))
            }
            collection.update_one({'_id': property_id}, {'$set': updated_data})
            return redirect(url_for('admin_dashboard'))
        
        prop = collection.find_one({'_id': property_id})
        return render_template('edit_property.html', prop=prop)
    except Exception as e:
        return f"Error editing property: {e}"

@app.route('/admin/delete/<id>', methods=['POST'])
def delete_property(id):
    try:
        collection.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        return f"Error deleting property: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
