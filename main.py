from flask import *
from SQLAgent import *

app = Flask("Kahoot")
app.secret_key = "123"
#agent = SQLAgent.SQLAgent("test.db")
#agent.create_tables()
#agent.populate_data()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rules")
def rules():
    return render_template("rules.html")

@app.route('/quizzes')
def quizzes():
    agent = SQLAgent("test.db")
    quizzes = agent.get_all_quizzes()

    agent.db.close()
    return render_template('quizzes.html', quizzes=quizzes)

@app.route('/quizzes/<int:quizz_id>')
def start_quiz(quizz_id):
    agent = SQLAgent("test.db")
    rows = agent.get_questions_for_quizz(quizz_id)
    session['questions'] = [dict(row) for row in rows]
    agent.db.close()
    session['current_question'] = 0
    session['correct_answers'] = 0
    return redirect(url_for('quiz_question', quizz_id=quizz_id))

@app.route('/quizzes/<int:quizz_id>/question')
def quiz_question(quizz_id):
    agent = SQLAgent("test.db")
    question_index = session['current_question']
    questions = session['questions']

    if question_index >= len(questions):
        return redirect(url_for('result', quizz_id=quizz_id))

    question = questions[question_index]
    answers = agent.get_answer_for_question(question['question_id'])

    return render_template('question.html', question=question, options=answers, quizz_id=quizz_id)


@app.route("/quizzes/<int:quizz_id>/answer", methods=["POST"])
def answer_func(quizz_id):
    agent = SQLAgent("test.db")
    question_index = session["current_question"]
    selected_answer = request.form.get("answer")
    print(selected_answer)
    question = session["questions"][question_index]
    correct_answers = agent.get_answer_for_question(question["question_id"])
    agent.db.close()

    for ans in correct_answers:
        if ans["content"] == selected_answer and ans["is_right"]:
            session["correct_answers"] += 1
            break

    session["current_question"] += 1

    if session["current_question"] >= len(session["questions"]):
        return redirect(url_for("result", quizz_id=quizz_id))
    else:
        return redirect(url_for("quiz_question", quizz_id=quizz_id))



@app.route("/quizzes/<int:quizz_id>/result")
def result(quizz_id):
    correct = session['correct_answers']
    total = len(session['questions'])
    return render_template("result.html", correct=correct, total=total)

app.run(debug=True)