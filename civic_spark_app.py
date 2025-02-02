import os
from dataclasses import dataclass
from typing import List, Dict
import google.generativeai as genai
import re
import dotenv

dotenv.load_dotenv()

@dataclass
class Idea:
    description: str
    country: str
    city: str
    user_age: int
    refined_details: List[str] = None
    global_examples: List[str] = None
    local_feasibility: Dict[str, str] = None
    relevant_breakthroughs: List[str] = None
    full_solution: str = None

class CivicSparkApp:
    def __init__(self, api_key):
        self.ideas = []
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def input_idea(self, description: str, country: str, city: str, user_age: int) -> Idea:
        new_idea = Idea(description, country, city, user_age)
        self.ideas.append(new_idea)
        return new_idea

    def extract_list_from_response(self, response_text):
        match = re.search(r'```(?:python)?\s*([\s\S]*?)\s*```', response_text)
        content = match.group(1) if match else response_text
        items = re.findall(r'"([^"]*)"', content)
        return items if items else []

    def extract_dict_from_response(self, response_text):
        content = re.sub(r'```(?:python)?\s*([\s\S]*?)\s*```', r'\1', response_text).strip()
        pairs = re.findall(r'"?([^":\n]+)"?\s*:\s*"([^"]+)"', content)
        result = {}
        for key, value in pairs:
            key = key.strip()
            value = value.strip()
            result[key] = value
        return result
    
    def extract_response_text(self, response):
        if isinstance(response, str):
            return response
        elif hasattr(response, 'parts') and len(response.parts) > 0:
            return response.parts[0].text
        else:
            return str(response)

    def get_refining_questions(self, idea: Idea) -> List[str]:
        age_group = "young" if idea.user_age < 18 else "adult"
        prompt = f"""
        Given the following civic idea for {idea.city}, {idea.country} from a {age_group} person aged {idea.user_age}: "{idea.description}"
        
        Please generate 4 probing questions to help refine this idea. 
        Tailor the questions to be appropriate for a {age_group} aged {idea.user_age}.
        Consider local context, resources, and challenges specific to {idea.country}.
        The questions should cover:
        - Problem definition in the local context
        - Stakeholders and beneficiaries in {idea.city}
        - Required resources considering {idea.country}'s economic situation
        - Potential challenges specific to {idea.country}
        
        Format the response as a Python list of strings.
        """
        
        response = self.model.generate_content(prompt)
        
        if isinstance(response, str):
            response_text = response
        elif hasattr(response, 'parts') and len(response.parts) > 0:
            response_text = response.parts[0].text
        else:
            response_text = str(response)
        
        return self.extract_list_from_response(response_text)

    def add_refined_details(self, idea: Idea, answers: List[str]) -> None:
        idea.refined_details = answers

    def provide_global_examples(self, idea: Idea) -> None:
        prompt = f"""
        Given the following civic idea for {idea.city}, {idea.country}:
        
        Idea: {idea.description}
        
        Refined Details:
        {idea.refined_details}
        
        Please provide 3 relevant examples of similar initiatives from around the world,
        preferably including examples from countries with similar economic conditions to {idea.country}.
        Briefly explain how each example relates to the given idea and its potential applicability to {idea.country}.
        
        Format the response as a Python list of strings.
        """
        
        response = self.model.generate_content(prompt)
        response_text = self.extract_response_text(response)
        idea.global_examples = self.extract_list_from_response(response_text)

    def assess_local_feasibility(self, idea: Idea) -> None:
        prompt = f"""
        Given the following civic idea for {idea.city}, {idea.country}:
        
        Idea: {idea.description}
        
        Refined Details:
        {idea.refined_details}
        
        Global Examples:
        {idea.global_examples}
        
        Please assess the feasibility of implementing this idea in {idea.city}, {idea.country}.
        Consider the following aspects:
        1. Economic feasibility
        2. Resource availability
        3. Local regulations and policies
        4. Cultural context
        5. Potential local partnerships
        
        For each aspect, provide a brief assessment and a feasibility score from 1 (very challenging) to 5 (highly feasible).
        
        Format the response as a series of key-value pairs, like this:
        "Economic feasibility": "Assessment... Score: X/5"
        "Resource availability": "Assessment... Score: X/5"
        ... and so on for each aspect.
        """
        
        response = self.model.generate_content(prompt)
        response_text = self.extract_response_text(response)
        idea.local_feasibility = self.extract_dict_from_response(response_text)

    def fetch_relevant_breakthroughs(self, idea: Idea) -> None:
        prompt = f"""
        Given the civic idea for {idea.city}, {idea.country}: "{idea.description}"

        Please identify and summarize 3 recent (within the last 2 years) breakthrough scientific research papers or groundbreaking technologies that are most relevant to this idea. Consider:
        1. How the research/technology relates to the civic problem
        2. Its potential impact on the proposed solution
        3. Its feasibility for implementation in {idea.country}, considering local resources and constraints

        Format the response as a Python list of strings, where each string contains the title of the research/technology and a brief summary of its relevance and potential impact.
        """

        response = self.model.generate_content(prompt)
        response_text = self.extract_response_text(response)
        idea.relevant_breakthroughs = self.extract_list_from_response(response_text)

    def provide_full_solution(self, idea: Idea) -> None:
        prompt = f"""
        Based on the civic idea for {idea.city}, {idea.country}, provided by a {idea.user_age}-year-old:

        Idea: {idea.description}

        Refined Details:
        {idea.refined_details}

        Global Examples:
        {idea.global_examples}

        Local Feasibility:
        {idea.local_feasibility}

        Relevant Breakthroughs:
        {idea.relevant_breakthroughs}

        Please provide a comprehensive solution that:
        1. Addresses the original idea
        2. Incorporates insights from the refined details
        3. Adapts relevant aspects from global examples
        4. Considers the local feasibility assessment
        5. Integrates applicable breakthroughs from recent research and technologies
        6. Is appropriate for implementation by someone aged {idea.user_age}

        Format the response as a detailed paragraph, clearly explaining how the recent breakthroughs can be leveraged to enhance the solution.
        """

        response = self.model.generate_content(prompt)
        idea.full_solution = self.extract_response_text(response)

    def process_idea(self, description: str, country: str, city: str, user_age: int) -> Idea:
        idea = self.input_idea(description, country, city, user_age)
        self.refine_idea(idea)
        self.provide_global_examples(idea)
        self.assess_local_feasibility(idea)
        self.fetch_relevant_breakthroughs(idea)
        self.provide_full_solution(idea)
        return idea
