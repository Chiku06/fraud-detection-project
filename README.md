# Fraud Detection Project - Deployment Guide

## 📋 Project Overview
This is a complete fraud detection system with a machine learning backend and interactive web frontend.

**Model Performance:**
- Accuracy: 95.38%
- Precision (Fraud Detection): 88%
- Recall (Fraud Detection): 94%

## 📁 Project Structure
```
fruad dectection project/
├── Fraud_Detection_Project.ipynb      # Jupyter notebook with model training
├── Copy of Sample_DATA.csv             # Training dataset
├── fraud_detection_model.pkl           # Trained model (auto-generated)
├── label_encoders.pkl                  # Label encoders (auto-generated)
├── feature_names.pkl                   # Feature names (auto-generated)
├── app.py                              # Flask backend API
├── streamlit_app.py                    # Streamlit frontend
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Backend API
Open a terminal/PowerShell and run:
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 3: Run the Frontend (In a new terminal)
Open another terminal/PowerShell in the same directory:
```bash
streamlit run streamlit_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 🎯 Using the Application

### Single Transaction Prediction
1. Go to the **"Single Prediction"** tab
2. Enter transaction details:
   - Transaction Type (dropdown)
   - Payment Gateway
   - City and State
   - Transaction Amount
   - Device OS and other details
3. Click **"Analyze Transaction"**
4. View the result: FRAUD or LEGITIMATE with probability scores

### Batch Prediction
1. Go to the **"Batch Prediction"** tab
2. Upload a CSV file with multiple transactions
3. Click **"Analyze All Transactions"**
4. Download the results with fraud predictions

### Model Information
- View model accuracy, precision, and recall
- See the confusion matrix
- Review all features used in the model

## 📊 API Endpoints

### Single Prediction
**POST** `/predict`

Request:
```json
{
    "Transaction_Type": "Purchase",
    "Payment_Gateway": "SamplePay",
    "Transaction_City": "New Delhi",
    "Transaction_State": "Delhi",
    "Transaction_Status": "Completed",
    "Device_OS": "Android",
    "Transaction_Frequency": 5,
    "Transaction_Amount_Deviation": 10.5,
    "Days_Since_Last_Transaction": 3,
    "Merchant_Category": "Purchases",
    "Transaction_Channel": "Mobile",
    "amount": 250.00
}
```

Response:
```json
{
    "prediction": 0,
    "fraud_probability": 0.15,
    "legitimate_probability": 0.85,
    "status": "success",
    "message": "Legitimate Transaction"
}
```

### Batch Prediction
**POST** `/predict-batch`

Request: Array of transaction objects (same format as single prediction)

Response: Array of predictions

### Health Check
**GET** `/health`

Response:
```json
{
    "status": "OK",
    "model_accuracy": 0.9538
}
```

## 🔧 Configuration

### Change API Port
Edit `app.py` (last line):
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### Change Streamlit Port
Run with custom port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 📝 Input Features Reference

### Categorical Features
- **Transaction_Type**: Bank Transfer, Investment, Subscription, Other, Purchase, Refund
- **Payment_Gateway**: SamplePay, Other, UPI Pay, Dummy Bank, Alpha Bank, Sigma Bank
- **Transaction_Status**: Completed, Pending, Failed
- **Device_OS**: Windows, MacOS, Android, iOS, Linux
- **Merchant_Category**: Brand Vouchers and OTT, Home delivery, Utilities, Purchases, Other, More Services, Financial services and Taxes, Investment
- **Transaction_Channel**: In-store, Mobile, Online
- **Transaction_City**: Major cities in India
- **Transaction_State**: Indian states

### Numerical Features
- **Transaction_Frequency**: 0-100 (count of transactions)
- **Transaction_Amount_Deviation**: -100.0 to 100.0 (percentage deviation)
- **Days_Since_Last_Transaction**: 0-365 (days)
- **amount**: 0.0-10000.0 (transaction amount in dollars)

## 🐛 Troubleshooting

### Issue: "Connection refused" when running Streamlit
**Solution**: Make sure Flask backend is running first in another terminal

### Issue: "ModuleNotFoundError"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: CSV upload fails
**Solution**: Ensure CSV has all required columns matching the input features

### Issue: Port already in use
**Solution**:
- Flask: Change port in `app.py`
- Streamlit: Use `--server.port` flag

## 📈 Model Retraining

To retrain the model with new data:

1. Replace `Copy of Sample_DATA.csv` with your new data
2. Open `Fraud_Detection_Project.ipynb` in Jupyter
3. Run all cells in sequence
4. Restart the Flask backend

## 🔐 Security Notes

- Never expose API keys or sensitive data in production
- Use HTTPS in production deployment
- Implement authentication for production use
- Validate all inputs on the server side
- Monitor API usage and set rate limits

## 📦 Deployment Options

### Local Network
```bash
python app.py  # Backend accessible at your-ip:5000
streamlit run streamlit_app.py  # Accessible at your-ip:8501
```

### Cloud Deployment (Heroku, AWS, Google Cloud)
1. Update `app.py` to use environment variables for ports
2. Create `Procfile`:
```
web: gunicorn app:app
web: streamlit run streamlit_app.py --server.port=$PORT
```
3. Deploy using cloud platform instructions

### Docker Containerization
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 📞 Support

For issues or questions:
1. Check the logs (backend terminal and Streamlit logs)
2. Verify all dependencies are installed
3. Ensure data format matches expected schema
4. Review API error messages

## 📄 License
This project is for educational purposes.

## ✅ Checklist Before Production

- [ ] Test with diverse transaction data
- [ ] Implement proper logging
- [ ] Add authentication to API
- [ ] Set up monitoring and alerts
- [ ] Configure HTTPS/SSL
- [ ] Set up database for predictions log
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Document API usage
- [ ] Set up automated backups

---

**Created**: January 2024  
**Last Updated**: January 2024  
**Status**: Ready for Deployment
