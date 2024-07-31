import google.generativeai as genai
from jinja2 import Template
import json

import dotenv
import os
dotenv.load_dotenv()    

api_key = os.environ.get("GEMINI_API_KEY")

import re

def get_creative_design(idea_data, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Given the following civic idea:
    {idea_data}

    give full modern idea designs without images, and propose the idea in a beutiful way,
    with modern way style, design it in a modern style article that looks attractive

    Provide your suggestions in a structured format.
    """
    response = model.generate_content(prompt)
    
    # Extract information from the response text
    response_text = response.text
    
    # design_suggestions = {
    #     "color_scheme": extract_colors(response_text),
    #     "fonts": extract_fonts(response_text),
    #     "layout_style": extract_layout_style(response_text),
    #     "image_prompts": extract_image_prompts(response_text),
    #     "other_elements": extract_other_elements(response_text)
    # }
    
    return response.text

def extract_colors(text):
    return re.findall(r'#[0-9A-Fa-f]{6}', text)

def extract_fonts(text):
    return re.findall(r'(?:Font|Heading|Body):\s*([^,\n]+)', text)

def extract_layout_style(text):
    layout_match = re.search(r'Layout Style:(.*?)(?:\n\n|\Z)', text, re.DOTALL)
    return layout_match.group(1).strip() if layout_match else "Grid-based layout"

def extract_image_prompts(text):
    image_section = re.search(r'Image Prompts:(.*?)(?:\n\n|\Z)', text, re.DOTALL)
    if image_section:
        return re.findall(r'\*\s*(.*?)(?:\n|$)', image_section.group(1))
    return []

def extract_other_elements(text):
    elements_section = re.search(r'Additional Design Elements:(.*?)(?:\n\n|\Z)', text, re.DOTALL)
    if elements_section:
        return re.findall(r'\*\s*(.*?)(?:\n|$)', elements_section.group(1))
    return []

 
def generate_html_report(image_prompts, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    code this html page full along with a map pointing the location, use leaflet js for map,
    and I don't want images for now put some placeholders,  design it in a modern style article that looks attractive
    and just return only the code without anything else
    {image_prompts}

    """
    response = model.generate_content(prompt)
    return response.text  # This will be parsed as JSON in the calling function

# def generate_html_report(idea_data, design_suggestions, image_links):
#     template = Template("""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Civic Idea Report</title>
#         <style>
#             /* CSS styles based on design_suggestions will be inserted here */
#         </style>
#     </head>
#     <body>
#         <h1>Civic Idea Report</h1>
#         <section id="description">
#             <h2>Description</h2>
#             <p>{{ idea_data.description }}</p>
#         </section>
#         <section id="location">
#             <h2>Location</h2>
#             <p>{{ idea_data.city }}, {{ idea_data.country }}</p>
#         </section>
#         <!-- More sections for other idea details -->
#         <!-- Image placeholders will be inserted here -->
#     </body>
#     </html>
#     """)
    
#     return template.render(idea_data=idea_data, design_suggestions=design_suggestions, image_links=image_links)

# idea_data = """**Example 1: Bus Rapid Transit (BRT) System in Jakarta, Indonesia**\n\nJakarta, like Bangalore, faces similar challenges of a rapidly growing population and traffic congestion. The BRT system in Jakarta is a dedicated bus lane network that provides a fast and efficient public transport option. This reduces traffic congestion and provides a more reliable mode of transportation for commuters. This system could be adapted to Bangalore by developing dedicated bus lanes on key corridors, improving bus infrastructure, and promoting BRT as a viable alternative to private vehicles.
# **Example 2: Cycle Sharing Program in Mexico City, Mexico**\n\nMexico City, like Bangalore, is a city with a high population density and traffic issues. The Ecobici program in Mexico City has been successful in promoting cycling as an alternative mode of transport. This program provides affordable bicycle rentals at various locations throughout the city, encouraging residents to choose cycling for short-distance commutes. A similar program in Bangalore could promote cycling, reduce traffic congestion, and improve air quality.
# **Example 3: Traffic Management System in Singapore**\n\nSingapore, a city-state with a similar economic development level to India, has a highly efficient traffic management system. They utilize a combination of technology, infrastructure improvements, and pricing mechanisms to optimize traffic flow. This includes intelligent traffic lights, congestion pricing, and real-time traffic information. Implementing a similar system in Bangalore, with a focus on leveraging technology and data analytics, could significantly improve traffic flow and reduce congestion.
# Real-Time Traffic Signal Optimization Using Reinforcement Learning
# This research explores using AI algorithms to dynamically optimize traffic signal timing based on real-time traffic data. By constantly adapting to changing conditions, it can help reduce congestion and improve traffic flow. This technology can be highly impactful in Bangalore, but its implementation might require substantial investment in sensor infrastructure and data processing capabilities.
# Autonomous Vehicle Technology and Its Potential for Urban Transportation
# Self-driving vehicles have the potential to significantly reduce traffic congestion by optimizing vehicle flow and eliminating human error. While still in its early stages, this technology could be a long-term solution for Bangalore's traffic woes. However, the high cost of development and the need for robust infrastructure and regulations might pose significant challenges for immediate implementation.
# Hyperloop: A High-Speed Transportation System for Urban Areas
# The Hyperloop concept offers a potential solution for high-speed inter-city travel, reducing the need for road travel and potentially easing congestion in Bangalore. However, the technology is still in its early stages of development and requires extensive infrastructure investment. While feasible in the long term, its implementation in Bangalore would require significant government support and collaboration with private entities.
# Here's the full solution for your idea:
# Bangalore's traffic woes, stemming from a rapidly growing population and lack of efficient public transport, are a significant issue. To address this, we can implement a multi-pronged approach, borrowing inspiration from global successes and leveraging emerging technologies. First, implementing a Bus Rapid Transit (BRT) system along key corridors, as seen in Jakarta, will provide a dedicated lane for fast and reliable public transportation. Second, promoting cycling as in Mexico City through a well-structured cycle sharing program will encourage short-distance commutes. Third, integrating intelligent traffic management systems with real-time data analytics, similar to Singapore's model, will optimize traffic flow. Fourth, investing in research and development of real-time traffic signal optimization using Reinforcement Learning will enable dynamic signal adjustments, reducing congestion. Although the required infrastructure and data processing might be expensive, the potential benefits for traffic flow are substantial. Finally, while autonomous vehicle technology is in its early stages, its potential to optimize vehicle flow and reduce human error is significant. Investing in research and development of this technology, alongside robust infrastructure and regulations, will provide a long-term solution. This holistic approach, combining practical measures with innovative technologies, will effectively address Bangalore's traffic challenges and create a more efficient and sustainable urban environment."""

# design_suggestions = get_creative_design(idea_data, api_key)
# image_links = generate_html_report(design_suggestions, api_key)
# # html_report = generate_html_report(idea_data, design_suggestions, image_links)
# print(image_links)