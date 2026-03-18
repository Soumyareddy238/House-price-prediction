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

Home Page

This is the landing page of the House Price Prediction System.
Users can enter property details and navigate to different features.

"Home Page" (home_page.png)

---

Prediction Page

This page allows users to input property details such as area, location, BHK, and other features.
The system predicts the house price and detects whether it is normal, overpriced, or underpriced.

"Prediction Page" (prediction_page.png)

---

Recommendation Page

This page provides similar property recommendations based on user input using the KNN algorithm.

"Recommendation Page" (recommendation_page.png)

---

Insights Dashboard

Displays analytical insights such as:

- Average price by location
- Average price by property type
- Scatter data for visualization

"Insights Page" (insights_page.png)

---

Admin Dashboard

Admin panel to manage the system:

- Add new properties
- Edit existing properties
- Delete properties
- View total properties and users

"Admin Dashboard" (admin_dashboard.png)

---

Login Page

Allows users and admin to securely login into the system.

"Login Page" (login_page.png)

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
