import os
from dataclasses import dataclass
from typing import List
import google.generativeai as genai
import re
import dotenv

dotenv.load_dotenv()

@dataclass
class Idea:
    description: str
    refined_details: List[str] = None
    global_examples: List[str] = None

class CivicSparkApp:
    def __init__(self, api_key):
        self.ideas = []
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def input_idea(self, description: str) -> Idea:
        new_idea = Idea(description)
        self.ideas.append(new_idea)
        return new_idea

    def extract_list_from_response(self, response_text):
        # Extract content between triple backticks
        match = re.search(r'```(?:python)?\s*([\s\S]*?)\s*```', response_text)
        if match:
            content = match.group(1)
        else:
            content = response_text

        # Find all list items
        items = re.findall(r'"([^"]*)"', content)
        return items if items else []

    def refine_idea(self, idea: Idea) -> None:
        prompt = f"""
        Given the following civic idea: "{idea.description}"
        
        Please generate 4 probing questions to help refine this idea. 
        The questions should cover different aspects such as:
        - Problem definition
        - Stakeholders and beneficiaries
        - Required resources
        - Potential challenges
        
        Format the response as a Python list of strings.
        """
        
        response = self.model.generate_content(prompt)
        questions = self.extract_list_from_response(response.text)
        
        idea.refined_details = []
        for question in questions:
            print(f"AI: {question}")
            answer = input("User: ")
            idea.refined_details.append(f"Q: {question}\nA: {answer}")

    def provide_global_examples(self, idea: Idea) -> None:
        prompt = f"""
        Given the following civic idea and its refined details:
        
        Idea: {idea.description}
        
        Refined Details:
        {idea.refined_details}
        
        Please provide 3 relevant examples of similar initiatives or solutions 
        from around the world. Each example should be from a different country 
        or city and briefly explain how it relates to the given idea.
        
        Format the response as a Python list of strings.
        """
        
        response = self.model.generate_content(prompt)
        idea.global_examples = self.extract_list_from_response(response.text)

    def process_idea(self, description: str) -> Idea:
        idea = self.input_idea(description)
        self.refine_idea(idea)
        self.provide_global_examples(idea)
        return idea

# Usage example
if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")

    app = CivicSparkApp(api_key)
    
    user_input = input("Please describe your civic idea: ")
    processed_idea = app.process_idea(user_input)
    
    print("\nRefined Idea Details:")
    for detail in processed_idea.refined_details:
        print(detail)
    
    print("\nGlobal Examples:")
    for example in processed_idea.global_examples:
        print(example)
