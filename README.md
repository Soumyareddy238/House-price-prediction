<<<<<<< HEAD
# Smart Real Estate Price Prediction and Recommendation System

An end-to-end Machine Learning web application designed to predict house prices with high accuracy, recommend similar properties, and detect market anomalies.

## 🚀 Features
- **Price Prediction**: Real-time estimation based on area, location, BHK, and property type using XGBoost.
- **Recommendations**: Personalized property suggestions using K-Nearest Neighbors (KNN).
- **Anomaly Detection**: Identification of overpriced or underpriced properties via Isolation Forest.
- **Market Insights**: Interactive visualizations of price trends and property distributions using Chart.js.
- **Premium UI**: Modern, glassmorphism-inspired dashboard for a professional user experience.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Machine Learning**: Scikit-Learn, XGBoost, Pandas, Numpy
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript, Chart.js
- **Model Storage**: Joblib

## 📁 Project Structure
```text
project/
├── data/               # CSV datasets
├── models/             # Trained ML models (.pkl)
├── static/             # CSS and frontend assets
├── templates/          # HTML templates
├── app.py              # Flask server
├── generate_data.py    # Synthetic data generation script
├── train_model.py      # ML training and evaluation script
└── README.md           # Documentation
```

## 💻 Local Setup

1. **Clone the project** to your local machine.
2. **Install Dependencies**:
   ```bash
   pip install flask pandas numpy scikit-learn xgboost joblib
   ```
3. **Generate Data**:
   ```bash
   python generate_data.py
   ```
4. **Train Models**:
   ```bash
   python train_model.py
   ```
5. **Run Application**:
   ```bash
   python app.py
   ```
6. Access the dashboard at `http://127.0.0.1:5000`.

## 📊 Evaluation
The primary model (XGBoost) achieved an R² score of ~0.96 on the synthetic dataset, demonstrating strong predictive capabilities.
=======
# House-price-prediction
House Price Prediction System

Description

House Price Prediction System - A Python and Flask based web application that predicts real estate prices, recommends similar properties, detects overpriced or underpriced houses, and provides insights for better decision-making.

---

Features

- Predict house prices based on user inputs
- Recommend similar properties using KNN algorithm
- Detect overpriced and underpriced properties (Anomaly Detection)
- Analyze property data and provide insights
- Admin dashboard for managing property data
- User authentication (Signup/Login system)

---

Technologies Used

- Python
- Flask
- MongoDB
- Scikit-learn
- Pandas
- NumPy
- HTML
- CSS
- JavaScript

---

Project Screenshots

## 🖥️ Web Application Interface

### 🏠 Home Page

The Home Page serves as the central navigation hub of the application, providing an overview of the system and its key functionalities.
It offers intuitive access to modules such as price prediction, market analysis, and recommendations, ensuring a seamless user experience.
![home_page]_(home_page.png)
---

### 🔐 Login Page

The Login Page enables secure authentication for registered users.
It ensures that only authorized users can access personalized features and system functionalities, maintaining data privacy and integrity.

---

### 📝 Signup Page

The Signup Page allows new users to register by providing essential credentials.
It is designed for a smooth onboarding process with proper input validation and user-friendly interaction.

---

### 🛠️ Admin Dashboard

The Admin Dashboard provides centralized control over the application.
It allows administrators to manage datasets, monitor user activity, and maintain system performance, ensuring efficient operation of the platform.

---

### 💰 Price Estimator

The Price Estimator is the core component of the application.
Users can input various property attributes such as location, number of rooms, area, and other relevant features to obtain predicted house prices.

The predictions are generated using trained machine learning models, ensuring accurate and data-driven outputs.

---

### 📊 Market Insights

The Market Insights module presents analytical visualizations and trends derived from housing datasets.

It helps users:

* Understand pricing patterns
* Analyze feature correlations
* Identify market trends

This enhances decision-making for buyers, sellers, and analysts.

---

### 🤝 Recommendation System

The Recommendation System provides intelligent suggestions based on user input and model predictions.

It enhances user engagement by:

* Suggesting similar properties
* Providing optimized pricing insights
* Delivering personalized recommendations

---

## ✨ Key Features of the Application

* End-to-end machine learning pipeline integration
* User-friendly web interface
* Secure authentication system
* Real-time price prediction capability
* Data-driven market analysis
* Intelligent recommendation engine

---


Installation

1. Clone the repository:

git clone https://github.com/your-username/House-price-prediction.git
cd House-price-prediction

2. Install dependencies:

pip install -r requirements.txt

3. Start MongoDB locally:

mongod

4. Run the application:

python app.py

5. Open in browser:

http://127.0.0.1:5000/

---

API Endpoints

- "/predict" → Predict house price
- "/recommend" → Get property recommendations
- "/detect_anomalies" → Detect overpriced/underpriced properties
- "/insights" → Get analytical insights

---

Future Improvements

- Deploy the application on cloud (AWS / Render)
- Improve UI with modern frameworks (React)
- Add real-time property data integration
- Enhance explainable AI features
- Add mobile-friendly design

---

Author

Soumya Reddy
B.Tech Computer Science Engineering

---
>>>>>>> f7287631e4faedf8ccd9bf34e9424ee31cae9d82
