# AI-Powered Quiz Generator

## Overview
This project is an AI-powered quiz generator that creates customized quizzes based on user preferences. It uses Google's Gemini API to generate questions dynamically, allowing users to practice for various exams and subjects.

## Features
- Customizable quiz setup (exam type, subject, and option for previous year questions)
- Dynamic question generation using Google's Gemini AI
- Interactive quiz interface with real-time feedback
- Question navigation with color-coded status indicators
- Support for multiple-choice questions
- Detailed explanations for correct and incorrect answers
- Option to use questions from previous year exam papers

![image](https://github.com/user-attachments/assets/558074b0-bc90-450d-8ef9-f8f7496959c3)

![image](https://github.com/user-attachments/assets/4a21423e-91c5-4b1c-b2b0-4e732579fde2)

## Technologies Used
- Backend: Python with Flask
- Frontend: HTML, CSS, JavaScript (jQuery)
- AI: Google Gemini API

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/your-username/ai-powered-quiz-generator.git
   cd ai-powered-quiz-generator
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Google Gemini API key:
   - Create a file named `config.py` in the project root
   - Add your API key to the file:
     ```python
     GOOGLE_API_KEY = "your_api_key_here"
     ```

### Running the Application
1. Start the Flask server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

## Usage Guide

1. **Quiz Setup**
   - On the startup page, enter the exam you're preparing for (e.g., UPSC, GATE)
   - Specify the subject you want to focus on
   - Check the box if you want questions from previous year papers
   - Click "Start Quiz" to begin

2. **Taking the Quiz**
   - Read each question carefully
   - Select your answer from the provided options
   - Use the navigation buttons to move between questions
   - Click "Save & Next" to submit your answer and move to the next question
   - Use "Mark for Review" if you want to come back to a question later
   - The question navigator on the right shows your progress:
     - Red: Current question
     - Green: Correctly answered
     - Red: Incorrectly answered
     - Blue: Visited but not answered
     - Yellow: Marked for review

3. **Reviewing Answers**
   - After answering, you'll see immediate feedback
   - Read the explanation provided for each question
   - For previous year questions, the source (year and exam) will be displayed

4. **Completing the Quiz**
   - Click "Submit" when you've finished all questions
   - Review your overall performance

## Customization
- To add more fallback questions, edit the `fallback_question` function in `gemini_api/question_generator.py`
- Modify the UI by editing `templates/index.html` and `templates/startup.html`

## Troubleshooting
- If questions aren't generating, check your API key and internet connection
- For persistent issues, review the console output for error messages

## Contributing
Contributions to improve the project are welcome. Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License
MIT License

## Acknowledgments
- Google Gemini API for powering the question generation
- Flask community for the web framework
- All contributors and users of this project
