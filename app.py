from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

USERNAME = "admin"
PASSWORD = "1234"

stages = [
    "مقابلة الإدارة المعنية",
    "مقابلة الموارد البشرية",
    "طلب التزكية",
    "التواصل مع جهة التزكية",
    "الرفع للاعتماد",
    "العرض الوظيفي",
    "تاريخ المباشرة"
]

def get_db():
    return sqlite3.connect("database.db")

def calculate_status(data):
    if any(d == "لم يتم" for d in data):
        return "غير مقبول"
    if all(d == "تم" for d in data):
        return "مقبول"
    return "قيد التقدم"

def last_stage(data):
    for d, s in zip(data, stages):
        if d != "تم":
            return s
    return "مكتمل"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/", methods=["GET", "POST"])
def form():
    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":
        data = [request.form.get(f"m{i}", "") for i in range(1, 8)]
        status = calculate_status(data)
        last = last_stage(data)

        db = get_db()
        db.execute("""
        INSERT INTO applicants
        (name, m1, m2, m3, m4, m5, m6, m7, status, last_stage)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """, [
            request.form["name"],
            *data,
            status,
            last
        ])
        db.commit()
        db.close()

        return redirect("/dashboard")

    return render_template("form.html", stages=stages)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")

    db = get_db()
    data = db.execute("""
        SELECT id, name, status, last_stage FROM applicants
    """).fetchall()
    db.close()

    return render_template("dashboard.html", data=data)

@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("logged_in"):
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM applicants WHERE id = ?", (id,))
    db.commit()
    db.close()
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
