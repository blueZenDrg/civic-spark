#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install flask google-generativeai python-dotenv

# Create .env file for API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

echo "Setup complete. Remember to add your Gemini API key to the .env file."
