"""
Flask Backend API for Fraud Detection
"""
from flask import Flask, request, jsonify, render_template_string
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load the trained model and feature names
try:
    model = joblib.load('fraud_detection_model.pkl')
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

try:
    feature_names = joblib.load('feature_names.pkl')
    print(f"✅ Feature names loaded: {feature_names}")
except Exception as e:
    print(f"❌ Error loading feature names: {e}")
    feature_names = []

# Try to load encoders, if they exist
try:
    encoders = joblib.load('label_encoders.pkl')
    print("✅ Encoders loaded successfully")
except Exception as e:
    print(f"⚠️  Encoders not found, using mappings instead: {e}")
    encoders = {}

# Define categorical columns
CATEGORICAL_COLS = [
    'Transaction_Type', 'Payment_Gateway', 'Transaction_City', 'Transaction_State',
    'Transaction_Status', 'Device_OS', 'Merchant_Category', 'Transaction_Channel'
]

NUMERIC_COLS = [
    'Transaction_Frequency', 'Transaction_Amount_Deviation',
    'Days_Since_Last_Transaction', 'amount'
]

# Mapping dictionaries for encoding (based on training data)
TRANSACTION_TYPE_MAP = {'Bank Transfer': 0, 'Investment': 1, 'Subscription': 2, 'Other': 3, 'Purchase': 4, 'Refund': 5}
PAYMENT_GATEWAY_MAP = {'SamplePay': 0, 'Other': 1, 'UPI Pay': 2, 'Dummy Bank': 3, 'Alpha Bank': 4, 'Sigma Bank': 5}
TRANSACTION_STATUS_MAP = {'Completed': 0, 'Pending': 1, 'Failed': 2}
DEVICE_OS_MAP = {'Android': 0, 'iOS': 1, 'MacOS': 2, 'Windows': 3, 'Linux': 4}
TRANSACTION_CHANNEL_MAP = {'In-store': 0, 'Mobile': 1, 'Online': 2}

# City mapping (sample - you can expand this)
CITIES = ['Durgapur', 'Rajpur Sonarpur', 'New Delhi', 'Bharatpur', 'Sagar', 'Bhiwani', 
          'Bidhannagar', 'Asansol', 'Kakinada', 'Mumbai', 'Bangalore', 'Hyderabad', 
          'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
CITY_MAP = {city: idx for idx, city in enumerate(CITIES)}

# State mapping (sample)
STATES = ['Chhattisgarh', 'Himachal Pradesh', 'Mizoram', 'Assam', 'Andhra Pradesh', 
          'Maharashtra', 'West Bengal', 'Telangana', 'Karnataka', 'Tamil Nadu',
          'Uttar Pradesh', 'Rajasthan', 'Delhi', 'Gujarat']
STATE_MAP = {state: idx for idx, state in enumerate(STATES)}

# Merchant category mapping
MERCHANT_MAP = {'Brand Vouchers and OTT': 0, 'Home delivery': 1, 'Utilities': 2, 
                'Purchases': 3, 'Other': 4, 'More Services': 5, 
                'Financial services and Taxes': 6, 'Investment': 7}

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return jsonify({
            "message": "Use POST with JSON to access this endpoint"
        })

    data = request.get_json()
    return jsonify({"received": data})


def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fraud Detection API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .endpoint { background: #f9f9f9; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }
            .method { font-weight: bold; color: #007bff; }
            code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
            .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Fraud Detection API</h1>
            <p><strong>Version:</strong> 1.0</p>
            <p><strong>Status:</strong> ✅ Running</p>
            
            <div class="info">
                <h3>Available Endpoints:</h3>
                <div class="endpoint">
                    <div class="method">GET</div>
                    <code>/health</code> - Health check
                </div>
                <div class="endpoint">
                    <div class="method">POST</div>
                    <code>/predict</code> - Single transaction prediction
                </div>
                <div class="endpoint">
                    <div class="method">POST</div>
                    <code>/predict-batch</code> - Batch transaction predictions
                </div>
            </div>
            
            <div style="margin-top: 30px; padding: 20px; background: #f0f0f0; border-radius: 5px;">
                <h3>📊 Model Performance</h3>
                <p><strong>Accuracy:</strong> 95.38%</p>
                <p><strong>Precision (Fraud):</strong> 88%</p>
                <p><strong>Recall (Fraud):</strong> 94%</p>
            </div>
            
            <div style="margin-top: 20px; text-align: center; color: #666; font-size: 12px;">
                <p>Fraud Detection System | Machine Learning Model</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'model_accuracy': 0.9538})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = CATEGORICAL_COLS + NUMERIC_COLS
        if not all(field in data for field in required_fields):
            missing = [f for f in required_fields if f not in data]
            return jsonify({
                'error': f'Missing fields: {missing}',
                'status': 'failed'
            }), 400
        
        # Prepare input dataframe with all features
        input_dict = {}
        
        # Encode categorical variables using mappings
        try:
            input_dict['Transaction_Type'] = TRANSACTION_TYPE_MAP.get(data['Transaction_Type'], 3)
            input_dict['Payment_Gateway'] = PAYMENT_GATEWAY_MAP.get(data['Payment_Gateway'], 0)
            input_dict['Transaction_City'] = CITY_MAP.get(data['Transaction_City'], 0)
            input_dict['Transaction_State'] = STATE_MAP.get(data['Transaction_State'], 0)
            input_dict['Transaction_Status'] = TRANSACTION_STATUS_MAP.get(data['Transaction_Status'], 0)
            input_dict['Device_OS'] = DEVICE_OS_MAP.get(data['Device_OS'], 0)
            input_dict['Merchant_Category'] = MERCHANT_MAP.get(data['Merchant_Category'], 4)
            input_dict['Transaction_Channel'] = TRANSACTION_CHANNEL_MAP.get(data['Transaction_Channel'], 0)
            
            # Add numeric variables
            input_dict['Transaction_Frequency'] = float(data['Transaction_Frequency'])
            input_dict['Transaction_Amount_Deviation'] = float(data['Transaction_Amount_Deviation'])
            input_dict['Days_Since_Last_Transaction'] = float(data['Days_Since_Last_Transaction'])
            input_dict['amount'] = float(data['amount'])
            
        except Exception as e:
            return jsonify({
                'error': f'Data type error: {str(e)}',
                'status': 'failed'
            }), 400
        
        # Create dataframe
        input_data = pd.DataFrame([input_dict])
        
        # Select only required features in correct order
        input_data = input_data[feature_names]
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
        
        return jsonify({
            'prediction': int(prediction),
            'fraud_probability': float(probability[1]),
            'legitimate_probability': float(probability[0]),
            'status': 'success',
            'message': 'Fraudulent Transaction' if prediction == 1 else 'Legitimate Transaction'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500

@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    try:
        data_list = request.get_json()
        
        if not isinstance(data_list, list):
            return jsonify({
                'error': 'Expected a list of transactions',
                'status': 'failed'
            }), 400
        
        results = []
        for data in data_list:
            try:
                # Prepare input dictionary
                input_dict = {}
                
                # Encode categorical variables
                input_dict['Transaction_Type'] = TRANSACTION_TYPE_MAP.get(data.get('Transaction_Type', 'Other'), 3)
                input_dict['Payment_Gateway'] = PAYMENT_GATEWAY_MAP.get(data.get('Payment_Gateway', 'Other'), 0)
                input_dict['Transaction_City'] = CITY_MAP.get(data.get('Transaction_City', 'New Delhi'), 0)
                input_dict['Transaction_State'] = STATE_MAP.get(data.get('Transaction_State', 'Delhi'), 0)
                input_dict['Transaction_Status'] = TRANSACTION_STATUS_MAP.get(data.get('Transaction_Status', 'Completed'), 0)
                input_dict['Device_OS'] = DEVICE_OS_MAP.get(data.get('Device_OS', 'Android'), 0)
                input_dict['Merchant_Category'] = MERCHANT_MAP.get(data.get('Merchant_Category', 'Other'), 4)
                input_dict['Transaction_Channel'] = TRANSACTION_CHANNEL_MAP.get(data.get('Transaction_Channel', 'Online'), 0)
                
                # Add numeric variables
                input_dict['Transaction_Frequency'] = float(data.get('Transaction_Frequency', 0))
                input_dict['Transaction_Amount_Deviation'] = float(data.get('Transaction_Amount_Deviation', 0))
                input_dict['Days_Since_Last_Transaction'] = float(data.get('Days_Since_Last_Transaction', 0))
                input_dict['amount'] = float(data.get('amount', 0))
                
                # Create dataframe
                input_data = pd.DataFrame([input_dict])
                
                # Select only required features
                input_data = input_data[feature_names]
                
                # Make prediction
                prediction = model.predict(input_data)[0]
                probability = model.predict_proba(input_data)[0]
                
                results.append({
                    'prediction': int(prediction),
                    'fraud_probability': float(probability[1]),
                    'legitimate_probability': float(probability[0]),
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'error': str(e),
                    'status': 'failed'
                })
        
        return jsonify({
            'predictions': results,
            'total': len(results),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
