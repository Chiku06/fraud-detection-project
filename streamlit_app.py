"""
Streamlit Frontend for Fraud Detection
"""
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .fraud-alert {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #d32f2f;
    }
    .legitimate {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #388e3c;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🔍 Fraud Detection System")
st.markdown("---")
st.markdown("""
    **Welcome to the Fraud Detection System!** This application uses advanced machine learning
    to detect fraudulent transactions with 95.38% accuracy.
""")

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
api_url = st.sidebar.text_input(
    "API Endpoint",
    value="http://localhost:5000",
    help="URL of the Flask backend API"
)

# Define feature options based on training data
TRANSACTION_TYPES = [
    'Bank Transfer', 'Investment', 'Subscription', 'Other', 'Purchase', 'Refund'
]
PAYMENT_GATEWAYS = [
    'SamplePay', 'Other', 'UPI Pay', 'Dummy Bank', 'Alpha Bank', 'Sigma Bank'
]
TRANSACTION_CITIES = [
    'New Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata',
    'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Durgapur', 'Rajpur Sonarpur'
]
TRANSACTION_STATES = [
    'Himachal Pradesh', 'Chhattisgarh', 'West Bengal', 'Assam', 'Andhra Pradesh',
    'Karnataka', 'Tamil Nadu', 'Maharashtra', 'Uttar Pradesh', 'Rajasthan'
]
TRANSACTION_STATUS = ['Completed', 'Pending', 'Failed']
DEVICE_OS = ['Windows', 'MacOS', 'Android', 'iOS', 'Linux']
MERCHANT_CATEGORIES = [
    'Brand Vouchers and OTT', 'Home delivery', 'Utilities', 'Purchases',
    'Other', 'More Services', 'Financial services and Taxes', 'Investment'
]
TRANSACTION_CHANNELS = ['In-store', 'Mobile', 'Online']

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Single Prediction",
    "📊 Batch Prediction",
    "📈 Model Info",
    "❓ Help"
])

# Tab 1: Single Prediction
with tab1:
    st.header("Single Transaction Analysis")
    st.markdown("Enter transaction details to check if it's fraudulent or legitimate.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Information")
        transaction_type = st.selectbox(
            "Transaction Type",
            TRANSACTION_TYPES,
            help="Type of transaction"
        )
        payment_gateway = st.selectbox(
            "Payment Gateway",
            PAYMENT_GATEWAYS,
            help="Payment method used"
        )
        transaction_city = st.selectbox(
            "City",
            TRANSACTION_CITIES,
            help="Location of transaction"
        )
        transaction_state = st.selectbox(
            "State",
            TRANSACTION_STATES,
            help="State where transaction occurred"
        )
    
    with col2:
        st.subheader("Additional Details")
        transaction_status = st.selectbox(
            "Transaction Status",
            TRANSACTION_STATUS,
            help="Final status of transaction"
        )
        device_os = st.selectbox(
            "Device OS",
            DEVICE_OS,
            help="Operating system used"
        )
        merchant_category = st.selectbox(
            "Merchant Category",
            MERCHANT_CATEGORIES,
            help="Type of merchant"
        )
        transaction_channel = st.selectbox(
            "Transaction Channel",
            TRANSACTION_CHANNELS,
            help="Channel of transaction"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Numerical Features")
        transaction_frequency = st.number_input(
            "Transaction Frequency",
            min_value=0,
            max_value=100,
            value=5,
            help="Number of transactions in this period"
        )
        transaction_amount_deviation = st.number_input(
            "Amount Deviation (%)",
            min_value=-100.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            help="Deviation from average amount"
        )
    
    with col4:
        st.subheader("Amount Information")
        days_since_last = st.number_input(
            "Days Since Last Transaction",
            min_value=0,
            max_value=365,
            value=5,
            help="Number of days since last transaction"
        )
        transaction_amount = st.number_input(
            "Transaction Amount (₹)",
            min_value=0.0,
            max_value=10000.0,
            value=100.0,
            step=0.01,
            help="Amount of transaction"
        )
    
    # Prediction button
    if st.button("🔍 Analyze Transaction", key="single_predict", use_container_width=True):
        with st.spinner("Analyzing transaction..."):
            try:
                payload = {
                    "Transaction_Type": transaction_type,
                    "Payment_Gateway": payment_gateway,
                    "Transaction_City": transaction_city,
                    "Transaction_State": transaction_state,
                    "Transaction_Status": transaction_status,
                    "Device_OS": device_os,
                    "Transaction_Frequency": int(transaction_frequency),
                    "Transaction_Amount_Deviation": float(transaction_amount_deviation),
                    "Days_Since_Last_Transaction": int(days_since_last),
                    "Merchant_Category": merchant_category,
                    "Transaction_Channel": transaction_channel,
                    "amount": float(transaction_amount)
                }
                
                response = requests.post(f"{api_url}/predict", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown("---")
                    st.subheader("📊 Prediction Result")
                    
                    col_pred1, col_pred2, col_pred3 = st.columns(3)
                    
                    is_fraud = result['prediction'] == 1
                    fraud_prob = result['fraud_probability'] * 100
                    
                    with col_pred1:
                        st.metric(
                            "Fraud Probability",
                            f"{fraud_prob:.2f}%",
                            delta=None
                        )
                    
                    with col_pred2:
                        st.metric(
                            "Legitimate Probability",
                            f"{result['legitimate_probability']*100:.2f}%",
                            delta=None
                        )
                    
                    with col_pred3:
                        status_text = "🚨 FRAUD" if is_fraud else "✅ LEGITIMATE"
                        st.metric("Status", status_text)
                    
                    st.markdown("---")
                    
                    if is_fraud:
                        st.markdown("""
                        <div class="fraud-alert">
                            <h3>⚠️ ALERT: Fraudulent Transaction Detected!</h3>
                            <p>This transaction has been flagged as fraudulent. Please verify with the customer immediately.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="legitimate">
                            <h3>✅ Transaction Appears Legitimate</h3>
                            <p>This transaction has been verified and appears to be legitimate.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Transaction summary
                    st.subheader("Transaction Summary")
                    summary_df = pd.DataFrame({
                        "Field": [
                            "Transaction Type", "Amount", "Payment Gateway",
                            "City", "State", "Status"
                        ],
                        "Value": [
                            transaction_type,
                            f"₹{transaction_amount:.2f}",
                            payment_gateway,
                            transaction_city,
                            transaction_state,
                            transaction_status
                        ]
                    })
                    st.dataframe(summary_df, use_container_width=True, hide_index=True)
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.write(response.json())
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure the Flask backend is running at: " + api_url)

# Tab 2: Batch Prediction
with tab2:
    st.header("Batch Transaction Analysis")
    st.markdown("Upload a CSV file with multiple transactions for analysis.")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="CSV file with transaction data"
    )
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head(), use_container_width=True)
        
        if st.button("🔍 Analyze All Transactions", use_container_width=True):
            with st.spinner("Processing transactions..."):
                try:
                    # Convert dataframe to list of dictionaries
                    transactions = df.to_dict('records')
                    
                    response = requests.post(f"{api_url}/predict-batch", json=transactions)
                    
                    if response.status_code == 200:
                        results = response.json()
                        predictions = results['predictions']
                        
                        # Add predictions to original dataframe
                        pred_df = pd.DataFrame(predictions)
                        result_df = pd.concat([df, pred_df], axis=1)
                        
                        st.success(f"✅ Analyzed {results['total']} transactions")
                        
                        # Summary statistics
                        col_stat1, col_stat2, col_stat3 = st.columns(3)
                        
                        fraud_count = sum(1 for p in predictions if p.get('prediction') == 1)
                        legitimate_count = results['total'] - fraud_count
                        
                        with col_stat1:
                            st.metric("Total Transactions", results['total'])
                        with col_stat2:
                            st.metric("Fraudulent", fraud_count)
                        with col_stat3:
                            st.metric("Legitimate", legitimate_count)
                        
                        st.markdown("---")
                        st.subheader("Detailed Results")
                        st.dataframe(result_df, use_container_width=True)
                        
                        # Download results
                        csv = result_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name=f"fraud_detection_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    else:
                        st.error(f"API Error: {response.status_code}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Tab 3: Model Information
with tab3:
    st.header("📈 Model Information")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.subheader("Model Performance")
        st.metric("Accuracy", "95.38%")
        st.metric("Precision (Fraud)", "88%")
        st.metric("Recall (Fraud)", "94%")
    
    with col_info2:
        st.subheader("Model Details")
        st.write("""
        - **Algorithm**: Random Forest Classifier
        - **Estimators**: 200
        - **Training Data**: 647 transactions
        - **Test Data**: 130 transactions
        """)
    
    st.markdown("---")
    st.subheader("Confusion Matrix")
    cm_data = {
        "Predicted Legitimate": [95, 4],
        "Predicted Fraud": [2, 29]
    }
    cm_df = pd.DataFrame(cm_data, index=["Actually Legitimate", "Actually Fraud"])
    st.dataframe(cm_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Features Used")
    features = [
        "Transaction Type",
        "Payment Gateway",
        "Transaction City",
        "Transaction State",
        "Transaction Status",
        "Device OS",
        "Transaction Frequency",
        "Merchant Category",
        "Transaction Channel",
        "Transaction Amount Deviation",
        "Days Since Last Transaction",
        "Transaction Amount"
    ]
    
    col_feat1, col_feat2 = st.columns(2)
    with col_feat1:
        for feat in features[:6]:
            st.write(f"✓ {feat}")
    with col_feat2:
        for feat in features[6:]:
            st.write(f"✓ {feat}")

# Tab 4: Help
with tab4:
    st.header("❓ Help & Documentation")
    
    st.subheader("How to Use")
    st.markdown("""
    1. **Single Prediction Tab**: Enter transaction details and click "Analyze Transaction"
    2. **Batch Prediction Tab**: Upload a CSV file with multiple transactions
    3. **Model Info Tab**: View model performance metrics and features
    
    ### Input Requirements
    - **Transaction Type**: Select from predefined types
    - **Payment Gateway**: Select payment method
    - **Location**: City and State
    - **Amount**: Enter transaction amount in dollars
    - **Other Details**: Device OS, merchant category, etc.
    
    ### Interpretation
    - **Fraud Probability**: Likelihood the transaction is fraudulent (0-100%)
    - **Status**: Final determination (FRAUD or LEGITIMATE)
    - **Confidence**: Based on probability scores
    """)
    
    st.subheader("API Endpoints")
    st.markdown("""
    - `GET /` - API information
    - `GET /health` - Health check
    - `POST /predict` - Single prediction
    - `POST /predict-batch` - Batch predictions
    """)
    
    st.subheader("Troubleshooting")
    st.markdown("""
    **Issue**: "Connection refused" error
    - **Solution**: Make sure Flask backend is running with `python app.py`
    
    **Issue**: "Invalid feature values"
    - **Solution**: Ensure all input values are within expected ranges
    
    **Issue**: Batch prediction fails
    - **Solution**: Verify CSV file has all required columns
    """)
    
    st.subheader("Contact & Support")
    st.info("""
    For issues or questions:
    - Check the backend logs: `python app.py`
    - Verify API endpoint is correct in sidebar
    - Review input data format
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Fraud Detection System v1.0 | Powered by Machine Learning</p>
    <p style='font-size: 0.8em; color: gray;'>© 2024 All rights reserved</p>
</div>
""", unsafe_allow_html=True)
