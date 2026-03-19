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

## 📸 Application Screenshots

### 🏠 Home Page
![Home Page](screenshots/home_page.png)
The Home Page serves as the central navigation hub of the application, providing an overview of features and easy access to different modules.

---

### 🔐 Login Page
![Login Page](screenshots/login.png)
Secure authentication interface allowing registered users to access the system safely.

---

### 📝 Signup Page
![Signup Page](screenshots/signup.png)
User-friendly registration page enabling new users to create an account with proper validation.

---

### 🛠️ Admin Dashboard
![Admin Dashboard](screenshots/admin.png)
Administrative panel to manage datasets, monitor users, and control system operations.

---

### 💰 Price Estimator
![Price Estimator](screenshots/price_estimator.png)
Core module where users input property details to get accurate house price predictions using machine learning models.

---

### 📊 Market Insights
![Market Insights](screenshots/market_insights.png)
Displays data visualizations and trends to help users understand housing market behavior.

---

### 🤖 Recommendation System
![Recommendation System](screenshots/recommendation.png)
Suggests similar properties and optimized pricing insights based on user inputs and predictions.
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
