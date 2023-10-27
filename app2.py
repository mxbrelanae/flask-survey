from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey as survey
response = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "shhh-its-a-secret"



@app.route("/")
def show_start():
    """Choose a survey."""
    return render_template("start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session. """
    session[response] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Saves user responses and redirects user to next question."""

    # get choice
    choice = request.form['answer']

    # add to responses
    responses = session[response]
    responses.append(choice)
    session[response] = responses
   
 

    if (len(responses) == len(survey.questions)):
        # User has answered all the questions
        return redirect("/finished")

    else:
        return redirect(f"/questions/{len(responses)}")



@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display the current question."""
    responses = session.get(response)
    
    if (responses is None):
        # User id trying to get to questions before start.
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # User has answered all the questions! Thank them.
        return redirect("/finished")

    if (len(responses) != qid):
        # User is trying to answer questions out of order.
        flash(f"Question id: {qid} not found.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("questions.html", question_num=qid, question=question)




@app.route("/finished")
def finish():
    """Survey finished"""
    return render_template("finish.html")
