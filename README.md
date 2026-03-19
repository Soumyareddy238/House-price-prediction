👇

🏠 Smart Real Estate Price Prediction & Recommendation System
📌 Description

The Smart Real Estate Price Prediction System is a full-stack web application built using Python and Flask.
It leverages machine learning models to accurately predict house prices, recommend similar properties, detect anomalies in pricing, and provide market insights for better decision-making.

🚀 Features

💰 Price Prediction: Predict house prices based on location, area, BHK, and other features using XGBoost

🤖 Recommendations: Suggest similar properties using K-Nearest Neighbors (KNN)

⚠️ Anomaly Detection: Identify overpriced and underpriced properties using Isolation Forest

📊 Market Insights: Visualize housing trends and data patterns

🔐 Authentication System: Secure Login & Signup functionality

🛠️ Admin Dashboard: Manage users and property data

🛠️ Technologies Used

Backend: Python, Flask

Machine Learning: Scikit-learn, XGBoost, Pandas, NumPy

Database: MongoDB

Frontend: HTML, CSS, JavaScript

Visualization: Chart.js

📸 Project Screenshots

⚠️ Make sure all images are inside a folder named screenshots in your repo.

🏠 Home Page

Landing page providing navigation to all major modules of the system.

<img src="screenshots/Home_Page.Png" width="800"/>
🔐 Login Page

Secure authentication page for existing users.

<img src="screenshots/Login_Page.Png" width="800"/>
📝 Signup Page

User registration page for creating new accounts.

<img src="screenshots/Signup_Page.Png" width="800"/>
🛠️ Admin Dashboard

Central control panel for managing users and data.

<img src="screenshots/Admin_Page.Png" width="800"/>
💰 Price Estimator

Core module where users input property details to get predicted prices.

<img src="screenshots/Price_Estimator_Page.Png" width="800"/>
📊 Market Insights

Displays charts and trends for better understanding of housing data.

<img src="screenshots/Market_Insights_Page.Png1" width="800"/>
<img src="screenshots/Market_Insights_Page.Png2" width="800"/>
🤖 Recommendation System

Provides similar property suggestions based on user input.

<img src="screenshots/Recommendation_Page.Png" width="800"/>
📁 Project Structure
project/
├── data/               
├── models/             
├── static/             
├── templates/          
├── screenshots/        # Store all images here
├── app.py              
├── train_model.py      
├── generate_data.py    
└── README.md           
💻 How to Run

Install Python

Install dependencies

pip install flask pandas numpy scikit-learn xgboost joblib pymongo

Run the application

python app.py

Open in browser

http://127.0.0.1:5000/
📊 Model Performance

XGBoost model achieves high accuracy on housing datasets

Efficient handling of feature-based predictions

Reliable recommendation and anomaly detection system

🔮 Future Improvements

🌐 Deploy on AWS / Render

📱 Mobile responsive UI

🔗 Real-time property API integration

🧠 Explainable AI (feature importance visualization)

📄 Export reports (PDF/Excel)

👨‍💻 Author

Soumya Reddy
B.Tech Computer Science Engineering
