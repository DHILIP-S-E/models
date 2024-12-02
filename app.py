from flask import Flask, render_template, request
import requests
import base64

# Initialize the Flask app
app = Flask(__name__)

# Hugging Face API URL and Authentication for the image model
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

# Home Page - Add a new section for the image generation
@app.route('/', methods=['GET', 'POST'])
def home():
    image = None
    if request.method == 'POST':
        prompt = request.form['prompt']  # Get the input from the user
        if prompt:
            payload = {"inputs": prompt}
            image_bytes = query(payload)
            if image_bytes:
                image = base64.b64encode(image_bytes).decode('utf-8')  # Convert the image to base64
            else:
                print("Failed to retrieve image.")
    return render_template('index.html', image=image)

# Other routes for your models (you can leave them as they are)
@app.route('/text', methods=['GET', 'POST'])
def text_model():
    # Your existing text model logic
    return render_template('text_model.html')

@app.route('/image', methods=['GET', 'POST'])
def image_model():
    # Your existing image model logic
    return render_template('image_model.html')

@app.route('/audio', methods=['GET', 'POST'])
def audio_model():
    # Your existing audio model logic
    return render_template('audio_model.html')

if __name__ == '__main__':
    app.run(debug=True)
