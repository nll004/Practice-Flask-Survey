from crypt import methods
from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import survey_collection

app = Flask(__name__)
app.config['SECRET_KEY'] = "shhh"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

response_list = []
survey_started = None

@app.route('/')
def survey_selection_page():
    '''Allows you to select a survey and send your to survey start '''

    response_list.clear()

    return render_template('home.html', surveys=survey_collection)

@app.route('/start/')
def start_survey():
    '''Start of survey'''

    # Get the selected survey and save it globally
    global survey_started
    survey_started = request.args.get('survey')

    title = survey_collection[survey_started].title
    instructions = survey_collection[survey_started].instructions

    return render_template('start.html', title= title, info= instructions)

@app.route("/answer", methods=["POST"])
def handle_answer():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['reply']

    # add this response to the session
    response_list.append(choice)
    session["responses"] = response_list

    if (len(response_list) == len(survey_collection[survey_started].questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(response_list)}")


@app.route('/questions/<int:num>/')
def questions(num):
    '''Ask question and save result'''

    # Trying to access questions out of order.
    if (len(response_list) != num):
        flash(f"Invalid question id: {num}.")
        return redirect(f"/questions/{len(response_list)}")

    # passing questions and answer selections to template
    answer = survey_collection[survey_started].questions[num].choices
    question = survey_collection[survey_started].questions[num].question

    return render_template('questions.html', id= num, question= question, answer=answer)

@app.route('/complete')
def survey_end():
    '''Save responses and the finished survey in cookies'''

    session["responses"] = response_list
    session['finished'] = survey_started

    return render_template('/complete.html')
