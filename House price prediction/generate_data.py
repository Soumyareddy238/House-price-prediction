import pandas as pd
import numpy as np
import os
import pymongo

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)
num_samples = 1000

# Feature definitions
locations = ['Downtown', 'Suburbs', 'Business District', 'Industrial Area', 'Outskirts']
property_types = ['apartment', 'villa', 'independent house']
bhk_options = [1, 2, 3, 4, 5]

data = {
    'area': np.random.randint(500, 5000, num_samples),
    'location': np.random.choice(locations, num_samples),
    'bhk': np.random.choice(bhk_options, num_samples, p=[0.1, 0.4, 0.3, 0.15, 0.05]),
    'property_type': np.random.choice(property_types, num_samples, p=[0.6, 0.2, 0.2]),
    'nearby_school_distance': np.round(np.random.uniform(0.5, 15.0, num_samples), 1),
    'nearby_hospital_distance': np.round(np.random.uniform(0.5, 20.0, num_samples), 1)
}

df = pd.DataFrame(data)

# Bathrooms logical constraints (usually at least 1, max bhk + 1)
df['bathrooms'] = df['bhk'].apply(lambda x: np.random.randint(max(1, x-1), x+2))

# Introduce some missing values to test preprocessing pipelines
missing_indices = np.random.choice(df.index, size=50, replace=False)
df.loc[missing_indices, 'nearby_school_distance'] = np.nan

missing_indices2 = np.random.choice(df.index, size=30, replace=False)
df.loc[missing_indices2, 'bathrooms'] = np.nan

# Base price calculation logic
base_price_per_sqft = {
    'Downtown': 15000,
    'Business District': 12000,
    'Suburbs': 6000,
    'Industrial Area': 4000,
    'Outskirts': 3000
}

prop_multiplier = {
    'villa': 1.5,
    'independent house': 1.2,
    'apartment': 1.0
}

prices = []
for index, row in df.iterrows():
    # Base calculation
    price = row['area'] * base_price_per_sqft[row['location']]
    
    # Property type multiplier
    price *= prop_multiplier[row['property_type']]
    
    # Distance penalties (closer is better, standardizing between 0 and 1 multiplier adjustment)
    school_penalty = min(0.1, (row['nearby_school_distance'] if not np.isnan(row['nearby_school_distance']) else 5.0) * 0.01)
    hospital_penalty = min(0.1, (row['nearby_hospital_distance'] if not pd.isna(row['nearby_hospital_distance']) else 5.0) * 0.01)
    
    price *= (1 - school_penalty - hospital_penalty)
    
    # Add random noise for realistic variations (+/- 15%)
    noise = np.random.uniform(0.85, 1.15)
    price *= noise
    prices.append(np.round(price, 2))

df['price'] = prices

# We'll save it as CSV
df.to_csv('data/real_estate_dataset.csv', index=False)
print("Dataset created successfully at data/real_estate_dataset.csv with", len(df), "rows.")

# 7. Connect to MongoDB and insert data
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["House_price_prediction"]
    collection = db["properties"]
    
    # Clear existing data to avoid duplicates for this run
    collection.delete_many({})
    
    # Convert DataFrame to list of dictionaries
    records = df.to_dict(orient='records')
    
    # Insert into MongoDB
    collection.insert_many(records)
    print("Successfully inserted", len(records), "records into MongoDB database 'House_price_prediction' collection 'properties'.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
