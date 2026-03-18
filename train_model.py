import pandas as pd
import numpy as np
import os
import joblib
import pymongo
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neighbors import NearestNeighbors

# 1. Load Data
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["House_price_prediction"]
    collection = db["properties"]
    
    # Fetch all records from MongoDB
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    
    # Drop MongoDB internal ID if it exists
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])
    
    print(f"Loaded {len(df)} records from MongoDB.")
except Exception as e:
    print(f"Error loading data from MongoDB: {e}")
    print("Falling back to CSV...")
    df = pd.read_csv('data/real_estate_dataset.csv')

# 2. Data Preprocessing & Feature Engineering
# Create price_per_sqft feature
df['price_per_sqft'] = df['price'] / df['area']

# Drop target and engineered target derivative for features
X = df.drop(columns=['price', 'price_per_sqft'])
y = df['price']

numeric_features = ['area', 'bhk', 'bathrooms', 'nearby_school_distance', 'nearby_hospital_distance']
categorical_features = ['location', 'property_type']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# 3. Model Building & Evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
}

best_model = None
best_r2 = -float('inf')
best_model_name = ""

print("Model Evaluation:")
print("-" * 30)

for name, model in models.items():
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
    
    # Train
    pipeline.fit(X_train, y_train)
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"{name}:")
    print(f"  MAE : {mae:.2f}")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  R2  : {r2:.4f}\n")
    
    if r2 > best_r2:
        best_r2 = r2
        best_model = pipeline
        best_model_name = name

print(f"Selected Best Model: {best_model_name} with R2 = {best_r2:.4f}")

# 4. Save the best model
os.makedirs('models', exist_ok=True)
joblib.dump(best_model, 'models/best_model.pkl')
print("Saved best model to models/best_model.pkl")

# 5. Recommendation System (KNN)
# Fit KNN on all valid data using the preprocessor to transform the data representations
X_processed = preprocessor.fit_transform(X)
knn = NearestNeighbors(n_neighbors=5, metric='minkowski')
knn.fit(X_processed)

# Save the preprocessor and knn separately
joblib.dump(preprocessor, 'models/preprocessor.pkl')
joblib.dump(knn, 'models/knn_recommender.pkl')

# Save df to keep index alignment for recommendations
df.to_csv('data/processed_dataset.csv', index=False)
print("Saved KNN recommender and processed dataset.")

# 6. Anomaly Detection (Isolation Forest)
# We use Isolation Forest on the price vs features
X_anomaly = df[['area', 'location', 'bhk', 'bathrooms', 'price']]
# Simple preprocessing for anomaly detection just to build it
numeric_anomaly = ['area', 'bhk', 'bathrooms', 'price']
cat_anomaly = ['location']

preprocessor_anomaly = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_anomaly),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_anomaly)
    ])

X_anomaly_proc = preprocessor_anomaly.fit_transform(X_anomaly.dropna())
iso_forest = IsolationForest(contamination=0.05, random_state=42)
iso_forest.fit(X_anomaly_proc)

joblib.dump(preprocessor_anomaly, 'models/anomaly_preprocessor.pkl')
joblib.dump(iso_forest, 'models/anomaly_detector.pkl')
print("Saved Anomaly Detector.")
print("Training script completed successfully!")
