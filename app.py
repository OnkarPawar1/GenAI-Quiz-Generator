from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from gemini_api.question_generator import generate_question, question_cache

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

# Dictionary to store user answers
user_answers = {}

@app.route('/', methods=['GET'])
def startup():
    return render_template('startup.html')

@app.route('/start-quiz', methods=['POST'])
def start_quiz():
    session['exam'] = request.form['exam']
    session['subject'] = request.form['subject']
    session['previous_year'] = 'previous_year' in request.form
    # Clear the question cache when starting a new quiz
    question_cache.clear()
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'exam' not in session or 'subject' not in session:
        return redirect(url_for('startup'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'submit_answer':
            question_id = int(request.form.get('question_id'))
            answer = request.form.get('answer')
            try:
                # Get the current question from cache
                question = generate_question(question_id, session['exam'], session['subject'], session['previous_year'])
                is_correct = answer == question['correct_answer']
                # Save the answer
                if answer:
                    user_answers[question_id] = {'answer': answer, 'is_correct': is_correct}
                return jsonify({
                    'status': 'success', 
                    'answered': list(user_answers.keys()),
                    'is_correct': is_correct,
                    'explanation': question['explanation'],
                    'source': question.get('source', '')
                })
            except Exception as e:
                print(f"Error processing answer: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        elif action == 'get_question':
            question_id = int(request.form.get('question_id'))
            try:
                question = generate_question(question_id, session['exam'], session['subject'], session['previous_year'])
                user_answer = user_answers.get(question_id, {}).get('answer', '')
                return jsonify({**question, 'user_answer': user_answer})
            except Exception as e:
                print(f"Error generating question: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
    return render_template('index.html', total_questions=40)

if __name__ == '__main__':
    app.run(debug=True)
