from flask import (
    Flask,
    session,
    escape,
    render_template,
    request,
    url_for,
    redirect,
    flash,
)
import data

app = Flask(__name__)
app.secret_key = "iqwr87fgbwisfv0w/akjc^"


@app.route("/")
def index():
    user = None
    if "username" in session:
        user = escape(session["username"])
    return render_template("index.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in data.users.keys():
            if data.verify_password(password, data.users[username]):
                session["username"] = request.form["username"]
                return redirect(url_for("index"))
            else:
                flash("Wrong username or password")
        else:
            flash("Wrong username or password")
    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("index"))


current_question = 0
results = 0


@app.route("/test", methods=["GET", "POST"])
def test():
    if "username" not in session:
        return redirect(url_for("index"))

    global current_question
    global results

    questions = list(data.questions.keys())

    if request.method == "POST":
        answer = request.form["answer"]
        current_question += 1
        
        if str(answer) == "True":
            results += 1

    if current_question == len(questions):
        return redirect("/result")

    question = questions[current_question]
    answers = []

    for v in data.questions[question]:
        answers.append(
            {
                "question": v,
                "value": data.questions[question][v],
            }
        )

    return render_template("test.html", question=question, answers=answers)


@app.route("/result")
def result():
    if "username" not in session:
        return redirect(url_for("index"))

    return render_template("result.html", results=results)


if __name__ == "__main__":
    app.run()
