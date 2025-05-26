# app.py (Flask backend)
from flask import Flask, request, render_template
import requests
import time

app = Flask(__name__)

# Replace with your actual API key from URLScan.io
URLSCAN_API_KEY = '01970d1f-5464-722d-a5fb-23279a90985e'

URLSCAN_SCAN_ENDPOINT = 'https://urlscan.io/api/v1/scan/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    url = request.form['url']

    headers = {
        'API-Key': URLSCAN_API_KEY,
        'Content-Type': 'application/json'
    }

    data = {
        'url': url,
        'public': 'on'
    }

    try:
        scan_response = requests.post(URLSCAN_SCAN_ENDPOINT, headers=headers, json=data)

        if scan_response.status_code != 200:
            return f"Failed to submit URL: {scan_response.text}"

        scan_data = scan_response.json()
        result_api_url = scan_data.get('api')

        # Wait for scan to complete (5-10 seconds recommended)
        time.sleep(7)

        result_response = requests.get(result_api_url)
        result_data = result_response.json()

        verdict = result_data.get('verdicts', {})
        malicious = verdict.get('overall', {}).get('malicious', False)

        if malicious:
            message = "⚠️ This URL is flagged as malicious/phishing!"
        else:
            message = "✅ This URL appears safe based on current scan."

        return render_template('result.html', message=message)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
