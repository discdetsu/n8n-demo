#!/usr/bin/env python3
"""
Test script for the Medical AI Prediction API
"""

import requests
import json
import base64

def test_predict_endpoint():
    """Test the /predict endpoint"""
    url = "http://localhost:50011/predict"
    
    # Test with sample.png
    try:
        with open('sample.png', 'rb') as img_file:
            files = {'image': ('sample.png', img_file, 'image/png')}
            
            print("Testing /predict endpoint...")
            response = requests.post(url, files=files)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print("\n=== PREDICTION RESPONSE ===")
                print(json.dumps(data, indent=2))
                
                # Check if heatmap image is included
                if data.get('heatmap_image'):
                    print(f"\nHeatmap image included (base64 length: {len(data['heatmap_image'])})")
                    
                    # Optionally save the heatmap image
                    save_heatmap = input("\nSave heatmap image to 'output_heatmap.png'? (y/n): ")
                    if save_heatmap.lower() == 'y':
                        img_data = base64.b64decode(data['heatmap_image'])
                        with open('output_heatmap.png', 'wb') as f:
                            f.write(img_data)
                        print("Heatmap saved as 'output_heatmap.png'")
                        
            else:
                print(f"Error: {response.text}")
                
    except FileNotFoundError:
        print("Error: sample.png not found!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")

def test_health_endpoint():
    """Test the /health endpoint"""
    url = "http://localhost:50011/health"
    
    try:
        print("\nTesting /health endpoint...")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing health endpoint: {e}")

def test_root_endpoint():
    """Test the root endpoint"""
    url = "http://localhost:50011/"
    
    try:
        print("\nTesting root endpoint...")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error testing root endpoint: {e}")

if __name__ == "__main__":
    print("Medical AI Prediction API Test Script")
    print("====================================")
    
    # Test all endpoints
    test_root_endpoint()
    test_health_endpoint()
    test_predict_endpoint()
    
    print("\nTest completed!") 