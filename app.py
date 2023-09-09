from flask import Flask, render_template, url_for,request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "beepbop2"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home():
    return render_template('home.html', survey = satisfaction_survey)

@app.route('/questions/<int:question_id>')
def show_question(question_id):
    if 0 <= question_id < len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[question_id]
        return render_template('questions.html', survey = satisfaction_survey, question=question, question_id=question_id)
    else:
        # Handle the case when an invalid question_id is provided
        return "Invalid question ID", 404

@app.route('/submit_response/<int:question_id>', methods=['POST'])
def submit_response(question_id):
    answer = request.form.get('answer')
    responses.append(answer)

    if question_id < len(satisfaction_survey.questions) - 1:
        # Redirect to the next question
        return redirect(url_for('show_question', question_id=question_id + 1))
    else:
        # Handle the case when all questions are answered (end of survey)
        return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return "Thank you for completing the survey!"

app.debug = True

if __name__ == '__main__':
    app.run()