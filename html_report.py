import google.generativeai as genai
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import dotenv
import os
import json

dotenv.load_dotenv()

def generate_html_report(data, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    code a html page for this {data}, structure it properly, and a map using leaflet js for pointing location to the location in the data, and use simple html for structure 
    design in a modern netflix style to look attractive, 
    Use a dark background (#141414), red accents (#e50914), and white text (#ffffff).
    Include smooth transitions and hover effects similar to Netflix's interface., only give the code except that nothing else
    """
    response = model.generate_content(prompt)
    
    html_content = response.candidates[0].content.parts[0].text
    
    html_content = html_content.replace("```html\n", "").replace("\n```", "")
    
    return html_content


def extract_text_from_response(response):
    if hasattr(response, 'text'):
        return response.text
    elif hasattr(response, 'parts'):
        return ''.join(part.text for part in response.parts if hasattr(part, 'text'))
    else:
        return str(response)


