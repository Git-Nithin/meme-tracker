
import os
import random
import json
import requests
from flask import Flask, jsonify
from flask_cors import CORS
import google.generativeai as genai  # Correct import for Google Gemini
from dotenv import load_dotenv
import tweepy
from web3 import Web3

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Configure the Google Gemini API with the API key
genai.configure(api_key=GEMINI_API_KEY)  # Use the configuration to set the API key

# Set up the generation configuration for the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the GenerativeModel
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",  # Model you want to use
    generation_config=generation_config
)

# For realtime data below twitter api and web3 setup to intereact with blockchain wallets need to be done 
# # Twitter API Setup (Use mock data if needed)
# TWITTER_BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"
# client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

# # Web3 Setup (Mock On-Chain Data)
# INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
# web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Dummy wallet data (Replace with real blockchain API calls)
WALLETS = ["0xabc...", "0xdef...", "0xghi..."]
TRENDING_TOKENS = ["$BTC", "$ETH", "$DOGE", "$SOL", "$ADA", "$AVAX", "$LTC"]

def analyze_onchain_data():
    """ Fetch live market data from Gemini API """
    token = random.choice(TRENDING_TOKENS).strip('$').lower()
    url = f"https://api.gemini.com/v1/pubticker/{token}usd"

    try:
        response = requests.get(url)

        data = response.json()

        if response.status_code == 200 and 'last' in data:
            price = data['last']  # Latest price of the token
            volume = data.get('volume', 'N/A')  # Get volume, or "N/A" if missing
            return {
                "token": f"${token}",
                "price": price,
                "volume": volume
            }
        else:
            print(f"Error from API: {data.get('message', 'Unknown error')}")
            return {
                "token": f"${token}",
                "price": "Unavailable",
                "volume": "Unavailable"
            }
    except Exception as e:
        print(f"Exception occurred: {e}")
        return {
            "token": "$BTC",
            "price": "Unavailable",
            "volume": "Unavailable"
        }
    

# Function to Analyze dummy Social Media Data
def analyze_social_data():
    """ Simulate Twitter influencer mentions """
    influencers = ["@ansem", "@SmartWhaleTrader", "@elonmusk"]
    token = random.choice(TRENDING_TOKENS)
    influencer = random.choice(influencers)
    
    return {
        "token": token,
        "influencer": influencer,
        "mentions": random.randint(10, 50)
    }

# AI-Generated Tweets Using Google Gemini API
def generate_tweets(onchain_data, social_data):
    """ Use Google Gemini to generate tweets """
    prompt = f"""
    Generate an engaging tweet with emojis about trending token {onchain_data['token']}:
    - The price of {onchain_data['token']} is {onchain_data['price']}.
    - The 24-hour volume is {onchain_data['volume']}.
    - Influencer {social_data['influencer']} mentioned {social_data['token']} {social_data['mentions']} times.
    - Make it engaging using emojis.
    """
    
    # Start a chat session using the model
    chat_session = model.start_chat(
        history=[]  # Empty history to start fresh
    )

    # Send the message (prompt) to the model
    response = chat_session.send_message(prompt)

    # Extract the generated text from the response
    generated_tweet = response.text
    
    print(generated_tweet)
        
    return generated_tweet


# Generate Tweets API
@app.route("/generate-tweets", methods=["GET"])
def get_tweets():
    onchain_data = analyze_onchain_data()  # Fetch live data from Gemini
    social_data = analyze_social_data()    # Simulate social media data
    
    tweets = [generate_tweets(onchain_data, social_data) for _ in range(5)]
    
    return jsonify({
        "tweets": tweets,  # List of generated tweets
        "onchain_data": onchain_data,  # On-chain data
        "social_data": social_data  # Social media data
    })


if __name__ == "__main__":
    app.run(debug=True)
