from flask import *
from SQLAgent import *

app = Flask("Kahoot")
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

app.run(debug=True)