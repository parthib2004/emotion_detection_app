from flask import Flask, render_template, request, jsonify
import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')

app = Flask(__name__)

# Define the Hugging Face Inference API URL and headers
HF_API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
HF_API_KEY =   api_key # Replace with your API key

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# Helper function to suggest coping strategies
def suggest_coping_strategy(emotion):
    strategies = {
        'joy': [
            "That's great! Keep up the positive mood by engaging in activities that make you happy.",
            "Fantastic! Share your joy with others and continue doing what makes you smile.",
            "Wonderful! Keep celebrating the good moments and spread the positivity."
        ],
        'sadness': [
            "It's okay to feel sad. Try talking to someone, journaling, or engaging in a comforting activity.",
            "Sadness is a natural part of life. Consider reaching out to friends or finding solace in a hobby.",
            "Feeling sad is tough. Practice self-care and consider speaking to a counselor if you need more support."
        ],
        'anger': [
            "Take deep breaths and try to calm down. Consider stepping away from the situation and focusing on relaxation techniques.",
            "Anger can be challenging. Engage in activities that help you relax and consider talking to someone about it.",
            "Try to channel your anger into something productive. Reflect on what triggered it and find ways to address it calmly."
        ],
        'fear': [
            "Try grounding techniques, like focusing on your breath, to calm anxiety. Seeking support from others can help.",
            "Fear can be overwhelming. Practice mindfulness and consider speaking to someone who can offer support.",
            "Facing fears is difficult. Take small steps to address them and reach out for help if needed."
        ],
        'love': [
            "Nurture this emotion by spending time with loved ones or practicing gratitude.",
            "Love is powerful. Show appreciation to those you care about and embrace the positive feelings.",
            "Cherish the love you feel and express it to others. It's a beautiful emotion to experience."
        ],
        'surprise': [
            "Channel your surprise into something productive or exciting, like exploring a new hobby.",
            "Surprise can be invigorating. Use this energy to try something new or to delve deeper into your interests.",
            "Embrace the surprise and let it inspire you to take on new challenges or experiences."
        ]
    }
    return random.choice(strategies.get(emotion, [
        "It's important to take care of yourself. Consider speaking to a professional if you're feeling overwhelmed."
    ]))

@app.route("/")
def index():
    return render_template("index.html")

def some_emotion_detection_function(message):
    payload = {"inputs": message}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return []

@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    data = request.get_json()
    message = data['message']
    
    # Call the emotion detection function
    emotion_result = some_emotion_detection_function(message)
    
    # Debugging: Print the emotion_result to understand its structure
    print("Emotion Result:", emotion_result)
    
    if emotion_result and isinstance(emotion_result, list) and len(emotion_result) > 0:
        # Access the first element of the outer list
        first_result_list = emotion_result[0]
        
        if isinstance(first_result_list, list) and len(first_result_list) > 0:
            # Access the first element of the inner list
            first_result = first_result_list[0]
            
            # Debugging: Print the first element to understand its structure
            print("First Result:", first_result)
            
            if isinstance(first_result, dict) and 'label' in first_result:
                emotion = first_result['label'].lower()
                suggestion = suggest_coping_strategy(emotion)
                return jsonify({'emotion': emotion, 'suggestion': suggestion})
            else:
                return jsonify({'error': 'Invalid emotion result format'}), 400
        else:
            return jsonify({'error': 'Invalid emotion result format'}), 400
    else:
        return jsonify({'error': 'Invalid emotion result format'}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)