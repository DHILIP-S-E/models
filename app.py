from flask import Flask, request, render_template
import requests
import base64

app = Flask(__name__)

# Hugging Face API URL and Authentication
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": "Bearer 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"}

# Function to query Hugging Face API and fetch the image
def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises HTTPError for bad responses
        if response.content:
            return response.content  # Return the content of the response
        else:
            print("No content received.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    image = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        if prompt:
            payload = {"inputs": prompt}
            image_bytes = query(payload)
            if image_bytes:
                image = base64.b64encode(image_bytes).decode('utf-8')
            else:
                print("Failed to retrieve image.")
    return render_template('index.html', image=image)

if __name__ == '__main__':
    app.run(debug=True)
