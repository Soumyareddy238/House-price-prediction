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
