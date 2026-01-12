"""
Test script to verify the fraud detection system
"""
import requests
import json

API_URL = "http://localhost:5000"

def test_health():
    """Test API health endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_single_prediction():
    """Test single prediction endpoint"""
    print("\n🔍 Testing Single Prediction Endpoint...")
    
    test_data = {
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
    
    try:
        response = requests.post(f"{API_URL}/predict", json=test_data)
        print(f"✅ Status: {response.status_code}")
        result = response.json()
        print(f"   Prediction: {result['message']}")
        print(f"   Fraud Probability: {result['fraud_probability']*100:.2f}%")
        print(f"   Legitimate Probability: {result['legitimate_probability']*100:.2f}%")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n🔍 Testing Batch Prediction Endpoint...")
    
    test_data = [
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
        },
        {
            "Transaction_Type": "Bank Transfer",
            "Payment_Gateway": "Other",
            "Transaction_City": "Mumbai",
            "Transaction_State": "Maharashtra",
            "Transaction_Status": "Completed",
            "Device_OS": "iOS",
            "Transaction_Frequency": 2,
            "Transaction_Amount_Deviation": -50.0,
            "Days_Since_Last_Transaction": 15,
            "Merchant_Category": "Other",
            "Transaction_Channel": "Online",
            "amount": 5000.00
        }
    ]
    
    try:
        response = requests.post(f"{API_URL}/predict-batch", json=test_data)
        print(f"✅ Status: {response.status_code}")
        result = response.json()
        print(f"   Total Transactions: {result['total']}")
        print(f"   Predictions: {result['predictions']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("="*50)
    print("Fraud Detection System - Test Suite")
    print("="*50)
    
    print(f"\n📡 API URL: {API_URL}")
    print("⚠️  Make sure Flask backend is running!")
    print("="*50)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Single Prediction", test_single_prediction()))
    results.append(("Batch Prediction", test_batch_prediction()))
    
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! System is ready.")
    else:
        print("\n⚠️  Some tests failed. Check your setup.")

if __name__ == "__main__":
    main()
