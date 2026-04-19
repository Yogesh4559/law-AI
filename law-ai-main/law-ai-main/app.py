from flask import Flask, render_template, request, jsonify, send_file

import google.generativeai as genai
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

# Secure API Key Configuration (Use environment variables)
API_KEY = "AIzaSyCtQADcmYCAkHwxLv3xzqcoZytFkyg8XSM"

# Initialize Google AI Model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Setup Logging for Debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.route("/")
def home():
    """Render the homepage."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_response():
    """Handle legal guidance generation request."""
    try:
        data = request.get_json()

        country = data.get("country", "").strip()
        situation = data.get("situation", "").strip()

        # Input validation
        if not country or not situation:
            return jsonify({"error": "Both 'country' and 'situation' are required."}), 400

        logging.info(f"Received request for country: {country} | Situation: {situation}")

        # Construct Enhanced Prompt
        prompt = f"""
        You are a highly experienced legal expert specializing in {country}'s laws.
        A user is facing the following legal situation:

        **Scenario:** {situation}

        Provide a professional legal response that includes:
        - **Relevant laws and regulations**
        - **Possible penalties and legal consequences**
        - **Steps the user should take**
        - **Legal rights they should be aware of**
        - **Any necessary legal actions or recommendations**

        Ensure that the response is **detailed, legally accurate, and user-friendly.**  
        Keep it **clear and well-structured**.
        """

        # Generate AI Response
        response = model.generate_content(prompt)

        if not response or not response.text.strip():
            raise ValueError("AI returned an empty response.")

        logging.info("✅ AI Response successfully generated.")

        return jsonify({"response": response.text.strip()})

    except Exception as e:
        logging.error(f"❌ Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500

@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.json
        response_text = data.get("response", "")

        if not response_text:
            return jsonify({"error": "No response text provided"}), 400

        # Save response as a file
        file_path = "response.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response_text)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
