# CivicSpark App

CivicSpark is an innovative web application that helps users develop and refine civic ideas. It uses AI to provide insights, examples, and feasibility assessments for urban improvement projects.

## Files

- `app.py`: Flask application server
- `civic_spark_app.py`: Core logic for processing civic ideas
- `html_report.py`: Generates HTML reports for civic ideas
- `index.html`: Main HTML template for the web interface
- `styles.css`: CSS styles for the web interface
- `script.js`: Client-side JavaScript for user interactions

## Setup

1. Clone this repository
2. Run `setup.sh` to install dependencies and set up the environment
3. Set your Gemini API key in the `.env` file
4. Run `python app.py` to start the server

## Usage

1. Open the app in your web browser
2. Enter your civic idea and follow the prompts
3. Receive AI-generated insights and assessments
4. Generate and download a detailed report of your idea

## Requirements

- Python 3.7+
- Flask
- google-generativeai
- python-dotenv

## License

This project is licensed under the MIT License.
