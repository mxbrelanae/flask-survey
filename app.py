from flask import Flask, render_template, request, redirect, flash
from surveys import satisfaction_survey as survey
response = []

app = Flask(__name__)
app.config['SECRET_KEY'] = "shhh-its-a-secret"



@app.route("/")
def show_start():
    """Choose a survey."""
    return render_template("start.html", survey=survey)


@app.route("/begin")
def start_survey():
    """Clear the session. """
    return redirect("/questions/0")




@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display the current question."""
   
    if (response is None):
        # User id trying to get to questions before start.
        return redirect("/")

    if (len(response) == len(survey.questions)):
        # User has answered all the questions! Thank them.
        return redirect("/finished")

    if (len(response) != qid):
        # User is trying to answer questions out of order.
        flash(f"Question id: {qid} not found.")
        return redirect(f"/questions/{len(response)}")

    question = survey.questions[qid]
    return render_template("questions.html", question_num=qid, question=question)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Saves user responses and redirects user to next question."""

    # get choice
    choice = request.form['answer']

    # add to responses
    
    response.append(choice)
 

    if (len(response) == len(survey.questions)):
        # User has answered all the questions
        return redirect("/finished")

    else:
        return redirect(f"/questions/{len(response)}")


@app.route("/finished")
def finish():
    """Survey finished"""
    return render_template("finish.html")
