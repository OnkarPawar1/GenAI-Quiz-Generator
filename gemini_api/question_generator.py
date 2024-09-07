import google.generativeai as genai
import os
import re
import random
from google.api_core import exceptions
from config import GOOGLE_API_KEY
# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Cache to store generated questions
question_cache = {}

def generate_question(question_number, exam, subject, previous_year=False, max_retries=3):
    cache_key = f"{exam}_{subject}_{question_number}_{previous_year}"
    
    # If the question is already in the cache, return it
    if cache_key in question_cache:
        return question_cache[cache_key]

    if previous_year:
        prompt = f"""Generate a multiple-choice question from a previous year {exam} exam paper, focusing on the subject of {subject}. 
        The question should be suitable for question number {question_number} in a quiz.
        Follow these strict guidelines:
        1. The question must be from an actual previous year paper of the {exam} exam.
        2. Provide exactly four options (A, B, C, D), each distinctly different and relevant to the question.
        3. Clearly indicate which option (A, B, C, or D) is the correct answer.
        4. Provide a detailed explanation that:
           a) Explains why the correct answer is right.
           b) Briefly explains why each of the other options is incorrect.
           c) Provides additional context or information related to the question topic.
        5. Include the year and specific exam from which the question was taken.

        Format the response EXACTLY as follows:
        QUESTION: [Your question here]
        OPTIONS:
        A) [Option A]
        B) [Option B]
        C) [Option C]
        D) [Option D]
        CORRECT ANSWER: [A, B, C, or D]
        EXPLANATION: [Your detailed explanation here]
        SOURCE: [Year and specific exam from which the question was taken, e.g., "UPSC Civil Services Exam 2018"]

        Ensure all parts of the response are consistent and factually correct."""
    else:
        prompt = f"""Generate a multiple-choice question for a {exam} exam, focusing on the subject of {subject}. 
        The question should be suitable for question number {question_number} in a quiz.
        Follow these strict guidelines:
        1. The question must be clear, concise, and directly related to the {subject} in the context of {exam}.
        2. Provide exactly four options (A, B, C, D), each distinctly different and relevant to the question.
        3. Clearly indicate which option (A, B, C, or D) is the correct answer.
        4. Provide a detailed explanation that:
           a) Explains why the correct answer is right.
           b) Briefly explains why each of the other options is incorrect.
           c) Provides additional context or information related to the question topic.

        Format the response EXACTLY as follows:
        QUESTION: [Your question here]
        OPTIONS:
        A) [Option A]
        B) [Option B]
        C) [Option C]
        D) [Option D]
        CORRECT ANSWER: [A, B, C, or D]
        EXPLANATION: [Your detailed explanation here]

        Ensure all parts of the response are consistent and factually correct."""

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            question_dict = parse_response(response.text, question_number)
            
            if verify_question(question_dict):
                # Cache the successfully generated question
                question_cache[cache_key] = question_dict
                print(f"Successfully generated question {question_number}:")
                print(f"Question: {question_dict['question']}")
                print(f"Options: {question_dict['options']}")
                print(f"Correct Answer: {question_dict['correct_answer']}")
                if 'source' in question_dict:
                    print(f"Source: {question_dict['source']}")
                return question_dict
            else:
                print(f"Attempt {attempt + 1}: Generated question failed verification.")
                print(f"Response: {response.text}")
        
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error generating question: {e}")
            print(f"Response: {response.text if 'response' in locals() else 'No response generated'}")
    
    # If all attempts fail, return and cache a fallback question
    fallback = fallback_question(question_number, exam, subject)
    question_cache[cache_key] = fallback
    return fallback

def parse_response(text, question_number):
    patterns = {
        'question': r'QUESTION:\s*(.*?)\s*OPTIONS:',
        'options': r'([A-D])\)\s*(.*?)(?=\n[A-D]\)|CORRECT ANSWER:)',
        'correct_answer': r'CORRECT ANSWER:\s*([A-D])',
        'explanation': r'EXPLANATION:\s*(.*?)(?:\nSOURCE:|$)',
        'source': r'SOURCE:\s*(.*)'
    }
    
    extracted = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            if key == 'options':
                extracted[key] = {option: text.strip() for option, text in matches}
            elif key == 'correct_answer':
                extracted[key] = matches[0]
            else:
                extracted[key] = matches[0].strip()
        elif key != 'source':  # Source is optional
            raise ValueError(f"Failed to extract {key} from the response")

    # Ensure consistency between options and correct answer
    correct_option = extracted['correct_answer']
    if correct_option not in extracted['options']:
        raise ValueError("Correct answer does not match any of the options")

    result = {
        "id": question_number,
        "question": extracted['question'],
        "options": extracted['options'],
        "correct_answer": correct_option,
        "explanation": extracted['explanation']
    }
    
    if 'source' in extracted:
        result['source'] = extracted['source']

    return result

def verify_question(question):
    required_keys = ["id", "question", "options", "correct_answer", "explanation"]
    if not all(key in question for key in required_keys):
        return False
    if not isinstance(question["options"], dict) or len(question["options"]) != 4:
        return False
    if question["correct_answer"] not in question["options"]:
        return False
    if len(question["explanation"]) < 50:  # Ensure explanation is substantial
        return False
    return True

def fallback_question(question_number, exam, subject):
    fallback_questions = [
        {
            "question": f"Which of the following is most relevant to {subject} in the context of {exam}?",
            "options": {
                "A": f"Key concept in {subject}",
                "B": f"Important figure in {subject}",
                "C": f"Significant event in {subject}",
                "D": f"Fundamental principle of {subject}"
            },
            "correct_answer": "A",
            "explanation": f"This question tests basic knowledge of {subject} as it relates to {exam}. Option A is correct as key concepts are fundamental to understanding any subject. The other options, while potentially relevant, may not be as universally applicable across all topics within {subject}."
        },
        # Add more fallback questions here...
    ]
    
    fallback = random.choice(fallback_questions)
    fallback["id"] = question_number
    return fallback

# Add more fallback questions to the list in the fallback_question function
