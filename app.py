from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "shhh"

debug = DebugToolbarExtension(app)

response_list = []

@app.route('/')
def funct():
    ''' Render survery start page '''

    response_list.clear()

    title = surveys['satisfaction'].title
    instructions = surveys['satisfaction'].instructions

    return render_template('start.html', title= title, info= instructions)


@app.route('/questions/<num>')
def questions(num):
    '''Ask question and save result'''

    num = len(response_list)
    question = surveys['satisfaction'].questions[num].question
    answer = surveys['satisfaction'].questions[num].choices


    # get answers from form
    get_ans = request.form.get('survey_form')

    # store answers in list
    response_list.append(get_ans)

    if (len(response_list) == len(surveys['satisfaction'].questions)):
        # They've answered all the questions! Thank them.
        redirect('/complete')
        return render_template("complete.html")

    else:
        return render_template('questions.html', id= num, question= question, answer=answer)
