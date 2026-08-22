from flask import Flask, request, redirect, session
from markupsafe import escape

app = Flask(__name__)

# ============================================================
# SECRET KEY
# ============================================================

app.secret_key = "placement_readiness_secret_key_2026"


# ============================================================
# USER ACCOUNTS
# ============================================================

users = {
    "AROKIYAUMA": "2425"
}


# ============================================================
# ADMIN ACCOUNT
# ============================================================

admin = {
    "username": "admin",
    "password": "admin123"
}


# ============================================================
# STUDENT ANALYTICS DATA
# ============================================================

student_results = {}

login_count = {}

previous_scores = {}


# ============================================================
# COMMON CSS
# ============================================================

def page_style():

    return """
    <style>

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: #f4f6fb;
        color: #222;
    }

    .header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        text-align: center;
        padding: 28px;
    }

    .container {
        width: 92%;
        max-width: 1200px;
        margin: 30px auto;
    }

    .card {
        background: white;
        padding: 25px;
        margin-bottom: 22px;
        border-radius: 18px;
        box-shadow: 0 5px 18px rgba(0,0,0,0.08);
    }

    .cards {
        display: grid;
        grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
    }

    .value {
        font-size: 32px;
        font-weight: bold;
        color: #667eea;
    }

    .button {
        display: inline-block;
        border: none;
        padding: 14px 22px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        text-decoration: none;
        border-radius: 10px;
        font-size: 16px;
        cursor: pointer;
        font-weight: bold;
    }

    .button:hover {
        opacity: 0.9;
    }

    .danger-button {
        background: #dc3545;
    }

    input[type="text"],
    input[type="password"],
    input[type="number"],
    select {
        width: 100%;
        padding: 14px;
        margin-top: 12px;
        border: 1px solid #ddd;
        border-radius: 10px;
        font-size: 15px;
    }

    textarea {
        width: 100%;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #ddd;
        font-family: Arial;
        font-size: 15px;
    }

    .question {
        background: white;
        padding: 22px;
        margin-bottom: 18px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    .option {
        display: block;
        padding: 12px;
        margin: 8px 0;
        background: #f5f6fa;
        border-radius: 9px;
        cursor: pointer;
    }

    .option:hover {
        background: #e9ebf8;
    }

    .center {
        text-align: center;
    }

    .strong {
        background: #d9f7e5;
        color: #168544;
    }

    .good {
        background: #fff3cd;
        color: #946200;
    }

    .weak {
        background: #ffe0e0;
        color: #c62828;
    }

    .status {
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }

    .focus {
        background: linear-gradient(135deg, #fff3cd, #ffe7a3);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }

    .info-box {
        background: #eef1ff;
        padding: 18px;
        border-radius: 12px;
        margin-top: 12px;
    }

    .warning-box {
        background: #ffe0e0;
        padding: 18px;
        border-radius: 12px;
        margin-top: 12px;
    }

    .success-box {
        background: #d9f7e5;
        padding: 18px;
        border-radius: 12px;
        margin-top: 12px;
    }

    .bar {
        background: #e9e9e9;
        height: 25px;
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 20px;
    }

    .fill {
        height: 25px;
        border-radius: 15px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        text-align: center;
        line-height: 25px;
        font-size: 13px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }

    th,
    td {
        padding: 13px;
        text-align: left;
        border-bottom: 1px solid #eee;
    }

    th {
        background: #f1f3fa;
    }

    .admin-nav {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 25px;
    }

    .small-button {
        padding: 8px 13px;
        font-size: 13px;
    }

    .student-card {
        border-left: 5px solid #667eea;
    }

    @media(max-width:600px) {

        .container {
            width: 95%;
        }

        table {
            font-size: 13px;
        }

        th,
        td {
            padding: 8px;
        }

    }

    </style>
    """


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_skill_status(score):

    if score >= 80:
        return "Strong"

    elif score >= 60:
        return "Good"

    return "Needs Improvement"


def status_class(status):

    if status == "Strong":
        return "strong"

    if status == "Good":
        return "good"

    return "weak"


def get_risk(overall):

    if overall < 50:
        return "🔴 High Risk"

    elif overall < 70:
        return "🟡 Medium Risk"

    return "🟢 Low Risk"


def get_career(aptitude, technical, communication):

    if technical >= 80 and aptitude >= 60:

        return (
            "Junior Software Developer",
            "Python, SQL, Programming, Problem Solving",
            "Python Developer, Software Developer, Junior Data Analyst"
        )

    elif technical >= 70 and communication >= 70:

        return (
            "Data Analyst",
            "Python, SQL, Power BI, Data Visualization",
            "Data Analyst, BI Analyst, Reporting Analyst"
        )

    elif communication >= 80:

        return (
            "Business Analyst",
            "Communication, Excel, Business Analysis",
            "Business Analyst, Customer Support Analyst"
        )

    else:

        return (
            "Placement Preparation",
            "Aptitude, Technical Skills, Communication",
            "Trainee, Junior Analyst, Graduate Trainee"
        )


def get_questions():

    return [

        # ====================================================
        # APTITUDE
        # ====================================================

        (
            "q1",
            "1. If 20% of a number is 50, what is the number?",
            ["200", "250", "300", "150"],
            "250"
        ),

        (
            "q2",
            "2. What is 15 + 25?",
            ["30", "35", "40", "45"],
            "40"
        ),

        (
            "q3",
            "3. What is 12 × 5?",
            ["50", "60", "70", "80"],
            "60"
        ),

        (
            "q4",
            "4. What is 100 ÷ 4?",
            ["20", "25", "30", "40"],
            "25"
        ),

        (
            "q5",
            "5. What is 25% of 200?",
            ["25", "40", "50", "60"],
            "50"
        ),

        (
            "q6",
            "6. If 5 pens cost ₹50, what is one pen?",
            ["₹5", "₹10", "₹15", "₹20"],
            "₹10"
        ),

        (
            "q7",
            "7. What is the next number: 2, 4, 6, 8, ?",
            ["9", "10", "11", "12"],
            "10"
        ),

        (
            "q8",
            "8. What is 10% of 500?",
            ["25", "40", "50", "60"],
            "50"
        ),

        (
            "q9",
            "9. A car travels 60 km in 1 hour. How far in 3 hours?",
            ["120 km", "150 km", "180 km", "200 km"],
            "180 km"
        ),

        (
            "q10",
            "10. What is 7²?",
            ["14", "21", "49", "56"],
            "49"
        ),

        # ====================================================
        # TECHNICAL
        # ====================================================

        (
            "q11",
            "11. Which language is commonly used for data analysis?",
            ["Python", "HTML", "CSS", "XML"],
            "Python"
        ),

        (
            "q12",
            "12. Which Python library is used for data manipulation?",
            ["Pandas", "Flask", "Tkinter", "Requests"],
            "Pandas"
        ),

        (
            "q13",
            "13. Which language is used to query databases?",
            ["SQL", "HTML", "CSS", "XML"],
            "SQL"
        ),

        (
            "q14",
            "14. Which Python library is used for numerical calculations?",
            ["NumPy", "Flask", "Django", "Requests"],
            "NumPy"
        ),

        (
            "q15",
            "15. Which tool is commonly used for data visualization?",
            ["Power BI", "Notepad", "Paint", "Calculator"],
            "Power BI"
        ),

        (
            "q16",
            "16. What does SQL stand for?",
            [
                "Structured Query Language",
                "Simple Query Language",
                "System Query Language",
                "Standard Question Language"
            ],
            "Structured Query Language"
        ),

        (
            "q17",
            "17. Which Python data structure uses key-value pairs?",
            ["List", "Tuple", "Dictionary", "Set"],
            "Dictionary"
        ),

        (
            "q18",
            "18. Which keyword defines a function in Python?",
            ["function", "def", "fun", "define"],
            "def"
        ),

        (
            "q19",
            "19. Which one is a Python data type?",
            ["Integer", "Website", "Browser", "Server"],
            "Integer"
        ),

        (
            "q20",
            "20. What does CSV stand for?",
            [
                "Comma-Separated Values",
                "Computer Stored Values",
                "Common System Values",
                "Column Stored Variables"
            ],
            "Comma-Separated Values"
        ),

        # ====================================================
        # COMMUNICATION
        # ====================================================

        (
            "q21",
            "21. Choose the grammatically correct sentence.",
            [
                "She go to college.",
                "She goes to college.",
                "She going college.",
                "She gone college."
            ],
            "She goes to college."
        ),

        (
            "q22",
            "22. Choose the correct word: I ___ a student.",
            ["am", "is", "are", "be"],
            "am"
        ),

        (
            "q23",
            "23. Choose the correct sentence.",
            [
                "He have a car.",
                "He has a car.",
                "He having a car.",
                "He had have a car."
            ],
            "He has a car."
        ),

        (
            "q24",
            "24. What is the opposite of Strong?",
            ["Powerful", "Weak", "Brave", "Hard"],
            "Weak"
        ),

        (
            "q25",
            "25. What is the synonym of Happy?",
            ["Sad", "Angry", "Joyful", "Tired"],
            "Joyful"
        ),

        (
            "q26",
            "26. Choose the correct sentence.",
            [
                "They is playing.",
                "They are playing.",
                "They am playing.",
                "They be playing."
            ],
            "They are playing."
        ),

        (
            "q27",
            "27. Choose the correct word: She ___ English very well.",
            ["speak", "speaks", "speaking", "spoken"],
            "speaks"
        ),

        (
            "q28",
            "28. What is the opposite of Early?",
            ["Fast", "Late", "Quick", "Soon"],
            "Late"
        ),

        (
            "q29",
            "29. Choose the correct sentence.",
            [
                "I have completed my work.",
                "I has completed my work.",
                "I completing my work.",
                "I completed have work."
            ],
            "I have completed my work."
        ),

        (
            "q30",
            "30. What is the synonym of Begin?",
            ["End", "Start", "Stop", "Finish"],
            "Start"
        )
    ]


# ============================================================
# STUDENT LOGIN PAGE
# ============================================================

@app.route("/")
def login():

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>Placement Readiness Analytics</title>

    """ + page_style() + """

    </head>

    <body>

        <div class="header">

            <h1>🎓 Placement Readiness Analytics</h1>

            <p>
                AI-Based Student Placement Assessment System
            </p>

        </div>

        <div class="container">

            <div class="card"
                 style="max-width:500px;margin:60px auto;">

                <div class="center">

                    <h2>🔐 Student Login</h2>

                    <p>
                        Enter your credentials to continue.
                    </p>

                </div>

                <form action="/login" method="POST">

                    <input
                        type="text"
                        name="username"
                        placeholder="Username"
                        required
                    >

                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        required
                    >

                    <br><br>

                    <button
                        class="button"
                        type="submit"
                        style="width:100%;"
                    >
                        Login
                    </button>

                </form>

                <br>

                <div class="center">

                    <p>Don't have an account?</p>

                    <a
                        class="button"
                        href="/register"
                    >
                        📝 Create Account
                    </a>

                    <br><br>

                    <a href="/admin">
                        🔐 Admin Portal
                    </a>

                </div>

            </div>

        </div>

    </body>

    </html>
    """


# ============================================================
# STUDENT LOGIN
# ============================================================

@app.route("/login", methods=["POST"])
def do_login():

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if username in users and users[username] == password:

        session.clear()

        session["student_logged_in"] = True
        session["student_username"] = username

        login_count[username] = login_count.get(username, 0) + 1

        return redirect("/search")

    return """
    <div style="
        text-align:center;
        font-family:Arial;
        margin-top:100px;
    ">

        <h2>❌ Invalid Username or Password</h2>

        <a href="/">Try Again</a>

    </div>
    """


# ============================================================
# STUDENT LOGOUT
# ============================================================

@app.route("/logout")
def student_logout():

    session.clear()

    return redirect("/")


# ============================================================
# CREATE ACCOUNT
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:

            return """
            <div style="
                text-align:center;
                font-family:Arial;
                margin-top:100px;
            ">

                <h2>❌ Please enter username and password.</h2>

                <a href="/register">Try Again</a>

            </div>
            """

        if username.lower() == "admin":

            return """
            <div style="
                text-align:center;
                font-family:Arial;
                margin-top:100px;
            ">

                <h2>❌ This username is reserved.</h2>

                <a href="/register">Try Again</a>

            </div>
            """

        if username in users:

            return """
            <div style="
                text-align:center;
                font-family:Arial;
                margin-top:100px;
            ">

                <h2>❌ Username Already Exists</h2>

                <a href="/register">
                    Try Again
                </a>

            </div>
            """

        users[username] = password
        login_count[username] = 0

        return """
        <div style="
            text-align:center;
            font-family:Arial;
            margin-top:100px;
        ">

            <h2>✅ Account Created Successfully!</h2>

            <p>
                You can now login using your new account.
            </p>

            <a href="/">
                Go to Login
            </a>

        </div>
        """

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>Create Account</title>

    """ + page_style() + """

    </head>

    <body>

        <div class="header">

            <h1>🎓 Placement Readiness Analytics</h1>

            <p>Create your student account</p>

        </div>

        <div class="container">

            <div class="card"
                 style="max-width:500px;margin:60px auto;">

                <div class="center">

                    <h2>📝 Create Account</h2>

                    <p>
                        Register as a student
                    </p>

                </div>

                <form action="/register" method="POST">

                    <input
                        type="text"
                        name="username"
                        placeholder="Create Username"
                        required
                    >

                    <input
                        type="password"
                        name="password"
                        placeholder="Create Password"
                        required
                    >

                    <br><br>

                    <button
                        class="button"
                        type="submit"
                        style="width:100%;"
                    >
                        Create Account
                    </button>

                </form>

                <br>

                <div class="center">

                    <a href="/">
                        ← Back to Login
                    </a>

                </div>

            </div>

        </div>

    </body>

    </html>
    """


# ============================================================
# STUDENT SEARCH
# ============================================================

@app.route("/search")
def search():

    if not session.get("student_logged_in"):
        return redirect("/")

    username = session.get("student_username", "Student")

    return f"""
    <!DOCTYPE html>
    <html>

    <head>

        <title>Student Search</title>

        {page_style()}

    </head>

    <body>

        <div class="header">

            <h1>🎓 Placement Readiness Analytics</h1>

            <p>Student Assessment</p>

        </div>

        <div class="container">

            <div class="card"
                 style="max-width:600px;margin:60px auto;">

                <div class="center">

                    <h2>👤 Welcome, {escape(username)}</h2>

                    <p>
                        Your account is ready for the placement
                        assessment.
                    </p>

                </div>

                <div class="info-box">

                    <b>Student:</b> {escape(username)}

                </div>

                <br>

                <div class="center">

                    <a
                        class="button"
                        href="/assessment?student={escape(username)}"
                    >
                        📝 Start Assessment
                    </a>

                    <br><br>

                    <a href="/dashboard">
                        📊 View My Dashboard
                    </a>

                    <br><br>

                    <a href="/logout">
                        🚪 Logout
                    </a>

                </div>

            </div>

        </div>

    </body>

    </html>
    """


# ============================================================
# STUDENT ASSESSMENT
# ============================================================

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    if not session.get("student_logged_in"):
        return redirect("/")

    questions = get_questions()

    # ========================================================
    # SUBMIT ASSESSMENT
    # ========================================================

    if request.method == "POST":

        student = session.get(
            "student_username",
            "Student"
        )

        aptitude_correct = 0
        technical_correct = 0
        communication_correct = 0

        # -------------------------------
        # Aptitude
        # -------------------------------

        for i in range(0, 10):

            q_id, question, options, answer = questions[i]

            if request.form.get(q_id) == answer:

                aptitude_correct += 1

        # -------------------------------
        # Technical
        # -------------------------------

        for i in range(10, 20):

            q_id, question, options, answer = questions[i]

            if request.form.get(q_id) == answer:

                technical_correct += 1

        # -------------------------------
        # Communication
        # -------------------------------

        for i in range(20, 30):

            q_id, question, options, answer = questions[i]

            if request.form.get(q_id) == answer:

                communication_correct += 1

        aptitude = aptitude_correct * 10
        technical = technical_correct * 10
        communication = communication_correct * 10

        aptitude_status = get_skill_status(aptitude)
        technical_status = get_skill_status(technical)
        communication_status = get_skill_status(communication)

        skills = {
            "Aptitude": aptitude,
            "Technical": technical,
            "Communication": communication
        }

        recommended_focus = min(
            skills,
            key=skills.get
        )

        overall = (
            aptitude +
            technical +
            communication
        ) / 3

        (
            career_path,
            recommended_skills,
            suitable_roles
        ) = get_career(
            aptitude,
            technical,
            communication
        )

        # ====================================================
        # SAVE PREVIOUS SCORE
        # ====================================================

        old_score = student_results.get(
            student,
            {}
        ).get(
            "overall",
            0
        )

        previous_scores[student] = old_score

        # ====================================================
        # SAVE RESULT
        # ====================================================

        student_results[student] = {

            "student": student,

            "aptitude": aptitude,

            "technical": technical,

            "communication": communication,

            "overall": overall,

            "aptitude_status": aptitude_status,

            "technical_status": technical_status,

            "communication_status": communication_status,

            "recommended_focus": recommended_focus,

            "career_path": career_path,

            "recommended_skills": recommended_skills,

            "suitable_roles": suitable_roles,

            "assessment_completed": True

        }

        session["current_student"] = student

        return redirect("/dashboard")

    # ========================================================
    # DISPLAY QUESTIONS
    # ========================================================

    student = session.get(
        "student_username",
        "Student"
    )

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Student Assessment</title>

        {page_style()}

    </head>

    <body>

    <div class="header">

        <h1>📝 Student Placement Assessment</h1>

        <p>
            Student:
            <b>{escape(student)}</b>
        </p>

    </div>

    <div class="container">

        <div class="info-box">

            <b>Important:</b>

            Answer all 30 questions.
            Each section contains 10 questions.

        </div>

        <br>

        <form method="POST" action="/assessment">
    """

    for index, (
        q_id,
        question,
        options,
        answer
    ) in enumerate(questions):

        if index == 0:

            html += """
            <div class="card">

                <h2>🧮 Aptitude — 10 Questions</h2>

                <p>
                    Test your numerical and logical ability.
                </p>

            </div>
            """

        if index == 10:

            html += """
            <div class="card">

                <h2>💻 Technical — 10 Questions</h2>

                <p>
                    Test your technical knowledge.
                </p>

            </div>
            """

        if index == 20:

            html += """
            <div class="card">

                <h2>🗣️ Communication — 10 Questions</h2>

                <p>
                    Test your English and communication skills.
                </p>

            </div>
            """

        html += f"""
        <div class="question">

            <h3>{question}</h3>
        """

        for option in options:

            html += f"""
            <label class="option">

                <input
                    type="radio"
                    name="{q_id}"
                    value="{escape(option)}"
                    required
                >

                {escape(option)}

            </label>
            """

        html += """
        </div>
        """

    html += """

            <button
                class="button"
                type="submit"
                style="width:100%;"
            >
                🚀 Submit Assessment
            </button>

        </form>

    </div>

    </body>

    </html>
    """

    return html


# ============================================================
# STUDENT DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if not session.get("student_logged_in"):
        return redirect("/")

    student = session.get(
        "student_username",
        "Student"
    )

    if student not in student_results:

        return redirect("/search")

    result = student_results[student]

    aptitude = result["aptitude"]
    technical = result["technical"]
    communication = result["communication"]
    overall = result["overall"]

    aptitude_status = result["aptitude_status"]
    technical_status = result["technical_status"]
    communication_status = result["communication_status"]

    recommended_focus = result["recommended_focus"]

    career_path = result["career_path"]
    recommended_skills = result["recommended_skills"]
    suitable_roles = result["suitable_roles"]

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Placement Dashboard</title>

        {page_style()}

    </head>

    <body>

    <div class="header">

        <h1>📊 Placement Readiness Dashboard</h1>

        <p>
            Student Performance Analytics
        </p>

    </div>

    <div class="container">

        <div class="admin-nav">

            <a
                class="button"
                href="/search"
            >
                🏠 Home
            </a>

            <a
                class="button"
                href="/simulator"
            >
                🚀 Interview Simulator
            </a>

            <a
                class="button"
                href="/logout"
            >
                🚪 Logout
            </a>

        </div>

        <div class="card">

            <h2>👤 {escape(student)}</h2>

            <p>
                B.Sc Computer Science with Data Analytics
            </p>

        </div>

        <div class="cards">

            <div class="card">

                <h3>🧮 Aptitude</h3>

                <div class="value">
                    {aptitude}%
                </div>

                <div class="status {status_class(aptitude_status)}">
                    {aptitude_status}
                </div>

            </div>

            <div class="card">

                <h3>💻 Technical</h3>

                <div class="value">
                    {technical}%
                </div>

                <div class="status {status_class(technical_status)}">
                    {technical_status}
                </div>

            </div>

            <div class="card">

                <h3>🗣️ Communication</h3>

                <div class="value">
                    {communication}%
                </div>

                <div class="status {status_class(communication_status)}">
                    {communication_status}
                </div>

            </div>

            <div class="card">

                <h3>🎯 Overall Readiness</h3>

                <div class="value">
                    {overall:.0f}%
                </div>

            </div>

        </div>

        <div class="card">

            <h2>📈 Performance Analysis</h2>

            <p>
                <b>Academic Performance</b>
            </p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:81%;"
                >
                    81%
                </div>

            </div>

            <p>
                <b>Aptitude</b>
            </p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:{aptitude}%;"
                >
                    {aptitude}%
                </div>

            </div>

            <p>
                <b>Technical</b>
            </p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:{technical}%;"
                >
                    {technical}%
                </div>

            </div>

            <p>
                <b>Communication</b>
            </p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:{communication}%;"
                >
                    {communication}%
                </div>

            </div>

        </div>

        <div class="card">

            <h2>🎯 Skill Gap Analysis</h2>

            <div class="cards">

                <div>

                    <h3>🧮 Aptitude</h3>

                    <div class="status {status_class(aptitude_status)}">
                        {aptitude_status}
                    </div>

                </div>

                <div>

                    <h3>💻 Technical</h3>

                    <div class="status {status_class(technical_status)}">
                        {technical_status}
                    </div>

                </div>

                <div>

                    <h3>🗣️ Communication</h3>

                    <div class="status {status_class(communication_status)}">
                        {communication_status}
                    </div>

                </div>

            </div>

        </div>

        <div class="card">

            <h2>🎯 Recommended Focus</h2>

            <div class="focus">

                Improve:
                {recommended_focus}

            </div>

        </div>

        <div class="card">

            <h2>💼 Career Recommendation</h2>

            <div class="info-box">

                <h3>🚀 Recommended Career Path</h3>

                <p>
                    <b>{career_path}</b>
                </p>

            </div>

            <div class="info-box">

                <h3>🛠️ Recommended Skills</h3>

                <p>
                    {recommended_skills}
                </p>

            </div>

            <div class="info-box">

                <h3>👔 Suitable Roles</h3>

                <p>
                    {suitable_roles}
                </p>

            </div>

        </div>

        <div class="card">

            <h2>🎓 Placement Readiness</h2>

            <div class="status {status_class(get_skill_status(overall))}">

                {get_skill_status(overall)}

            </div>

        </div>

        <div class="card center">

            <h2>🚀 Placement Simulator</h2>

            <p>
                Test your readiness with a simulated
                placement interview.
            </p>

            <a
                class="button"
                href="/simulator"
            >
                🚀 Start Placement Simulator
            </a>

        </div>

        <div class="card center">

            <a
                class="button"
                href="/assessment"
            >
                🔄 Take Assessment Again
            </a>

        </div>

    </div>

    </body>

    </html>
    """


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if (
            username == admin["username"]
            and password == admin["password"]
        ):

            session.clear()

            session["admin_logged_in"] = True

            return redirect("/admin/dashboard")

        return """
        <div style="
            text-align:center;
            font-family:Arial;
            margin-top:100px;
        ">

            <h2>❌ Invalid Admin Username or Password</h2>

            <a href="/admin">
                Try Again
            </a>

        </div>
        """

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Admin Login</title>

    """ + page_style() + """

    </head>

    <body>

        <div class="header">

            <h1>🎓 Placement Readiness Analytics</h1>

            <p>Administrator Portal</p>

        </div>

        <div class="container">

            <div class="card"
                 style="max-width:500px;margin:60px auto;">

                <div class="center">

                    <h2>🔐 Admin Login</h2>

                    <p>
                        Authorized administrators only
                    </p>

                </div>

                <form action="/admin" method="POST">

                    <input
                        type="text"
                        name="username"
                        placeholder="Admin Username"
                        required
                    >

                    <input
                        type="password"
                        name="password"
                        placeholder="Admin Password"
                        required
                    >

                    <br><br>

                    <button
                        class="button"
                        type="submit"
                        style="width:100%;"
                    >
                        🔐 Admin Login
                    </button>

                </form>

                <br>

                <div class="center">

                    <a href="/">
                        ← Student Login
                    </a>

                </div>

            </div>

        </div>

    </body>

    </html>
    """


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect("/admin")

    total_students = len(users)

    students_logged_in = sum(
        1
        for username in users
        if login_count.get(username, 0) > 0
    )

    assessments_completed = len(student_results)

    if assessments_completed > 0:

        average_readiness = sum(
            result["overall"]
            for result in student_results.values()
        ) / assessments_completed

    else:

        average_readiness = 0

    placement_ready = sum(
        1
        for result in student_results.values()
        if result["overall"] >= 70
    )

    at_risk = sum(
        1
        for result in student_results.values()
        if result["overall"] < 50
    )

    # ========================================================
    # TOP STUDENTS
    # ========================================================

    top_students = sorted(
        student_results.values(),
        key=lambda x: x["overall"],
        reverse=True
    )[:10]

    # ========================================================
    # LOW SCORE STUDENTS
    # ========================================================

    low_students = sorted(
        student_results.values(),
        key=lambda x: x["overall"]
    )[:10]

    # ========================================================
    # SKILL GAP COUNTS
    # ========================================================

    aptitude_weak = sum(
        1
        for result in student_results.values()
        if result["aptitude"] < 60
    )

    technical_weak = sum(
        1
        for result in student_results.values()
        if result["technical"] < 60
    )

    communication_weak = sum(
        1
        for result in student_results.values()
        if result["communication"] < 60
    )

    # ========================================================
    # IMPROVEMENT RANKING
    # ========================================================

    improvements = []

    for student, result in student_results.items():

        old_score = previous_scores.get(
            student,
            0
        )

        improvement = (
            result["overall"] -
            old_score
        )

        improvements.append({

            "student": student,

            "old": old_score,

            "new": result["overall"],

            "improvement": improvement

        })

    improvements.sort(
        key=lambda x: x["improvement"],
        reverse=True
    )

    # ========================================================
    # DASHBOARD
    # ========================================================

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Admin Command Center</title>

        {page_style()}

    </head>

    <body>

    <div class="header">

        <h1>📊 Admin Command Center</h1>

        <p>
            Intelligent Placement Readiness Analytics
        </p>

    </div>

    <div class="container">

        <div class="admin-nav">

            <a class="button"
               href="/admin/dashboard">
                📊 Dashboard
            </a>

            <a class="button"
               href="/admin/students">
                👥 All Students
            </a>

            <a class="button"
               href="/admin/what-if">
                🧪 What-If Simulator
            </a>

            <a class="button"
               href="/admin/logout">
                🚪 Logout
            </a>

        </div>

        <!-- ==================================================
             SUMMARY CARDS
        =================================================== -->

        <div class="cards">

            <div class="card center">

                <h3>👥 Total Students</h3>

                <div class="value">
                    {total_students}
                </div>

            </div>

            <div class="card center">

                <h3>🔐 Students Logged In</h3>

                <div class="value">
                    {students_logged_in}
                </div>

            </div>

            <div class="card center">

                <h3>📝 Assessments Completed</h3>

                <div class="value">
                    {assessments_completed}
                </div>

            </div>

            <div class="card center">

                <h3>🎯 Average Readiness</h3>

                <div class="value">
                    {average_readiness:.0f}%
                </div>

            </div>

            <div class="card center">

                <h3>🏆 Placement Ready</h3>

                <div class="value">
                    {placement_ready}
                </div>

            </div>

            <div class="card center">

                <h3>🚨 At Risk</h3>

                <div class="value">
                    {at_risk}
                </div>

            </div>

        </div>


        <!-- ==================================================
             ALL STUDENTS QUICK VIEW
        =================================================== -->

        <div class="card">

            <h2>👥 Student Management</h2>

            <p>
                View registered students and open their
                individual placement analytics.
            </p>

            <a
                class="button"
                href="/admin/students"
            >
                👥 View All Students
            </a>

        </div>


        <!-- ==================================================
             TOP STUDENTS
        =================================================== -->

        <div class="card">

            <h2>🏆 Top Students</h2>
    """

    if top_students:

        html += """
            <table>

                <tr>

                    <th>Rank</th>
                    <th>Student</th>
                    <th>Aptitude</th>
                    <th>Technical</th>
                    <th>Communication</th>
                    <th>Overall</th>
                    <th>Action</th>

                </tr>
        """

        for rank, student in enumerate(
            top_students,
            1
        ):

            name = escape(
                student["student"]
            )

            html += f"""
                <tr>

                    <td>🏆 {rank}</td>

                    <td>{name}</td>

                    <td>
                        {student["aptitude"]}%
                    </td>

                    <td>
                        {student["technical"]}%
                    </td>

                    <td>
                        {student["communication"]}%
                    </td>

                    <td>
                        <b>
                            {student["overall"]:.0f}%
                        </b>
                    </td>

                    <td>

                        <a
                            class="button small-button"
                            href="/admin/student/{name}"
                        >
                            View
                        </a>

                    </td>

                </tr>
            """

        html += """
            </table>
        """

    else:

        html += """
            <div class="info-box">

                No assessments completed yet.

            </div>
        """

    html += """
        </div>


        <!-- ==================================================
             LOW SCORE STUDENTS
        =================================================== -->

        <div class="card">

            <h2>📉 Low-Score Students</h2>
    """

    if low_students:

        html += """
            <table>

                <tr>

                    <th>Student</th>
                    <th>Overall</th>
                    <th>Weakest Area</th>
                    <th>Risk</th>
                    <th>Action</th>

                </tr>
        """

        for student in low_students:

            name = escape(
                student["student"]
            )

            risk = get_risk(
                student["overall"]
            )

            html += f"""
                <tr>

                    <td>{name}</td>

                    <td>
                        <b>
                            {student["overall"]:.0f}%
                        </b>
                    </td>

                    <td>
                        {student["recommended_focus"]}
                    </td>

                    <td>
                        {risk}
                    </td>

                    <td>

                        <a
                            class="button small-button"
                            href="/admin/student/{name}"
                        >
                            View
                        </a>

                    </td>

                </tr>
            """

        html += """
            </table>
        """

    else:

        html += """
            <div class="info-box">

                No student assessment data available.

            </div>
        """

    html += f"""

        </div>


        <!-- ==================================================
             SKILL GAP ANALYTICS
        =================================================== -->

        <div class="card">

            <h2>🧩 Skill Gap Analytics</h2>

            <div class="cards">

                <div class="card center">

                    <h3>🧮 Aptitude Gap</h3>

                    <div class="value">
                        {aptitude_weak}
                    </div>

                    <p>
                        students need improvement
                    </p>

                </div>

                <div class="card center">

                    <h3>💻 Technical Gap</h3>

                    <div class="value">
                        {technical_weak}
                    </div>

                    <p>
                        students need improvement
                    </p>

                </div>

                <div class="card center">

                    <h3>🗣️ Communication Gap</h3>

                    <div class="value">
                        {communication_weak}
                    </div>

                    <p>
                        students need improvement
                    </p>

                </div>

            </div>

        </div>


        <!-- ==================================================
             EARLY WARNING
        =================================================== -->

        <div class="card">

            <h2>🚨 Early-Warning System</h2>

            <p>
                Students below 50% readiness are automatically
                classified as high-risk students.
            </p>
    """

    if at_risk > 0:

        html += """
            <div class="warning-box">

                <b>⚠️ Immediate Attention Required</b>

                <p>
                    Some students have significantly low
                    placement readiness.
                </p>

            </div>
        """

    else:

        html += """
            <div class="success-box">

                ✅ No high-risk students detected.

            </div>
        """

    html += """
        </div>


        <!-- ==================================================
             IMPROVEMENT RANKING
        =================================================== -->

        <div class="card">

            <h2>📈 Improvement Ranking</h2>

            <p>
                Students are ranked according to their
                improvement between assessments.
            </p>
    """

    if improvements:

        html += """
            <table>

                <tr>

                    <th>Rank</th>
                    <th>Student</th>
                    <th>Previous</th>
                    <th>Current</th>
                    <th>Improvement</th>

                </tr>
        """

        for rank, item in enumerate(
            improvements[:10],
            1
        ):

            html += f"""
                <tr>

                    <td>{rank}</td>

                    <td>
                        {escape(item["student"])}
                    </td>

                    <td>
                        {item["old"]:.0f}%
                    </td>

                    <td>
                        {item["new"]:.0f}%
                    </td>

                    <td>
                        <b>
                            {item["improvement"]:+.0f}%
                        </b>
                    </td>

                </tr>
            """

        html += """
            </table>
        """

    else:

        html += """
            <div class="info-box">

                Improvement data will appear after
                assessments.

            </div>
        """

    html += """

        </div>


        <!-- ==================================================
             INTELLIGENT INTERVENTION
        =================================================== -->

        <div class="card">

            <h2>🔮 Intelligent Intervention</h2>

            <p>
                The system identifies the weakest area
                and recommends an intervention.
            </p>

            <div class="info-box">

                <b>Example:</b>

                <p>
                    If Aptitude is the weakest area,
                    recommend aptitude practice,
                    numerical reasoning tests and
                    mock placement tests.
                </p>

            </div>

        </div>

    </div>

    </body>

    </html>
    """

    return html


# ============================================================
# ADMIN - ALL STUDENTS
# ============================================================

@app.route("/admin/students")
def admin_students():

    if not session.get("admin_logged_in"):
        return redirect("/admin")

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>All Students</title>

        {page_style()}

    </head>

    <body>

    <div class="header">

        <h1>👥 All Students</h1>

        <p>
            Student Management & Placement Analytics
        </p>

    </div>

    <div class="container">

        <div class="admin-nav">

            <a
                class="button"
                href="/admin/dashboard"
            >
                ← Dashboard
            </a>

            <a
                class="button"
                href="/admin/what-if"
            >
                🧪 What-If Simulator
            </a>

            <a
                class="button"
                href="/admin/logout"
            >
                🚪 Logout
            </a>

        </div>

        <div class="card">

            <h2>
                📋 Registered Students
            </h2>

            <p>
                Select a student to view complete analytics.
            </p>

            <table>

                <tr>

                    <th>#</th>

                    <th>Student</th>

                    <th>Login Status</th>

                    <th>Assessment</th>

                    <th>Overall</th>

                    <th>Risk</th>

                    <th>Action</th>

                </tr>
    """

    if users:

        for index, username in enumerate(
            users,
            1
        ):

            logged = (
                "🟢 Logged In"
                if login_count.get(username, 0) > 0
                else "⚪ Not Logged In"
            )

            if username in student_results:

                result = student_results[username]

                assessment_status = "✅ Completed"

                overall = (
                    f"{result['overall']:.0f}%"
                )

                risk = get_risk(
                    result["overall"]
                )

            else:

                assessment_status = "⏳ Pending"

                overall = "—"

                risk = "—"

            safe_name = escape(username)

            html += f"""
                <tr>

                    <td>{index}</td>

                    <td>
                        <b>{safe_name}</b>
                    </td>

                    <td>
                        {logged}
                    </td>

                    <td>
                        {assessment_status}
                    </td>

                    <td>
                        <b>{overall}</b>
                    </td>

                    <td>
                        {risk}
                    </td>

                    <td>

                        <a
                            class="button small-button"
                            href="/admin/student/{safe_name}"
                        >
                            👁️ View
                        </a>

                    </td>

                </tr>
            """

    html += """

            </table>

        </div>

    </div>

    </body>

    </html>
    """

    return html


# ============================================================
# ADMIN - VIEW INDIVIDUAL STUDENT
# ============================================================

@app.route("/admin/student/<student>")
def admin_view_student(student):

    if not session.get("admin_logged_in"):
        return redirect("/admin")

    if student not in users:

        return """
        <div style="
            text-align:center;
            font-family:Arial;
            margin-top:100px;
        ">

            <h2>❌ Student Not Found</h2>

            <a href="/admin/students">
                Back to Students
            </a>

        </div>
        """

    # ========================================================
    # NO ASSESSMENT YET
    # ========================================================

    if student not in student_results:

        return f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>Student Details</title>

            {page_style()}

        </head>

        <body>

        <div class="header">

            <h1>👤 Student Details</h1>

            <p>
                Student Analytics
            </p>

        </div>

        <div class="container">

            <div class="admin-nav">

                <a
                    class="button"
                    href="/admin/students"
                >
                    ← All Students
                </a>

                <a
                    class="button"
                    href="/admin/dashboard"
                >
                    📊 Dashboard
                </a>

            </div>

            <div class="card center">

                <h2>
                    👤 {escape(student)}
                </h2>

                <div class="info-box">

                    <h3>
                        ⏳ Assessment Not Completed
                    </h3>

                    <p>
                        This student has registered but has
                        not completed the placement assessment.
                    </p>

                </div>

            </div>

        </div>

        </body>

        </html>
        """

    # ========================================================
    # STUDENT RESULT
    # ========================================================

    result = student_results[student]

    aptitude = result["aptitude"]
    technical = result["technical"]
    communication = result["communication"]
    overall = result["overall"]

    focus = result["recommended_focus"]

    career = result["career_path"]
    skills = result["recommended_skills"]
    roles = result["suitable_roles"]

    risk = get_risk(overall)

    old_score = previous_scores.get(
        student,
        0
    )

    improvement = overall - old_score

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Student Analytics</title>

        {page_style()}

    </head>

    <body>

    <div class="header">

        <h1>👤 Student Analytics</h1>

        <p>
            Detailed Placement Readiness Report
        </p>

    </div>

    <div class="container">

        <div class="admin-nav">

            <a
                class="button"
                href="/admin/students"
            >
                ← All Students
            </a>

            <a
                class="button"
                href="/admin/dashboard"
            >
                📊 Dashboard
            </a>

            <a
                class="button"
                href="/admin/what-if"
            >
                🧪 What-If
            </a>

        </div>

        <div class="card">

            <h2>
                👤 {escape(student)}
            </h2>

            <p>
                B.Sc Computer Science with Data Analytics
            </p>

            <div class="success-box">

                <b>Assessment Status:</b>
                ✅ Completed

            </div>

        </div>


        <!-- ==================================================
             SCORE CARDS
        =================================================== -->

        <div class="cards">

            <div class="card center">

                <h3>🧮 Aptitude</h3>

                <div class="value">
                    {aptitude}%
                </div>

                <div class="status {status_class(result['aptitude_status'])}">

                    {result['aptitude_status']}

                </div>

            </div>

            <div class="card center">

                <h3>💻 Technical</h3>

                <div class="value">
                    {technical}%
                </div>

                <div class="status {status_class(result['technical_status'])}">

                    {result['technical_status']}

                </div>

            </div>

            <div class="card center">

                <h3>🗣️ Communication</h3>

                <div class="value">
                    {communication}%
                </div>

                <div class="status {status_class(result['communication_status'])}">

                    {result['communication_status']}

                </div>

            </div>

            <div class="card center">

                <h3>🎯 Overall</h3>

                <div class="value">
                    {overall:.0f}%
                </div>

                <div class="status {status_class(get_skill_status(overall))}">

                    {get_skill_status(overall)}

                </div>

            </div>

        </div>


        <!-- ==================================================
             PERFORMANCE
        =================================================== -->

        <div class="card">

            <h2>📈 Performance Analysis</h2>

            <p>
                <b>Aptitude — {aptitude}%</b>
            </p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:{aptitude}%"
                >
                    {aptitude}%
                </div>

            </div>

            <p>
                <b>Technical — {technical}%</b>
            </p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:{technical}%"
                >
                    {technical}%
                </div>

            </div>

            <p>
                <b>Communication — {communication}%</b>
            </p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:{communication}%"
                >
                    {communication}%
                </div>

            </div>

        </div>


        <!-- ==================================================
             RISK
        =================================================== -->

        <div class="card">

            <h2>🚨 Risk Analysis</h2>

            <div class="status {status_class(get_skill_status(overall))}">

                {risk}

            </div>

        </div>


        <!-- ==================================================
             SKILL GAP
        =================================================== -->

        <div class="card">

            <h2>🧩 Skill Gap Analysis</h2>

            <div class="focus">

                Main Focus:
                {focus}

            </div>

            <br>

            <table>

                <tr>

                    <th>Skill</th>

                    <th>Score</th>

                    <th>Status</th>

                </tr>

                <tr>

                    <td>🧮 Aptitude</td>

                    <td>{aptitude}%</td>

                    <td>{result['aptitude_status']}</td>

                </tr>

                <tr>

                    <td>💻 Technical</td>

                    <td>{technical}%</td>

                    <td>{result['technical_status']}</td>

                </tr>

                <tr>

                    <td>🗣️ Communication</td>

                    <td>{communication}%</td>

                    <td>{result['communication_status']}</td>

                </tr>

            </table>

        </div>


        <!-- ==================================================
             CAREER
        =================================================== -->

        <div class="card">

            <h2>💼 Career Recommendation</h2>

            <div class="info-box">

                <h3>
                    🚀 Career Path
                </h3>

                <p>
                    <b>{career}</b>
                </p>

            </div>

            <div class="info-box">

                <h3>
                    🛠️ Recommended Skills
                </h3>

                <p>
                    {skills}
                </p>

            </div>

            <div class="info-box">

                <h3>
                    👔 Suitable Roles
                </h3>

                <p>
                    {roles}
                </p>

            </div>

        </div>


        <!-- ==================================================
             IMPROVEMENT
        =================================================== -->

        <div class="card">

            <h2>📈 Improvement Analysis</h2>

            <p>
                Previous Score:
                <b>{old_score:.0f}%</b>
            </p>

            <p>
                Current Score:
                <b>{overall:.0f}%</b>
            </p>

            <p>
                Improvement:
                <b>{improvement:+.0f}%</b>
            </p>

        </div>


        <!-- ==================================================
             WHAT IF
        =================================================== -->

        <div class="card center">

            <h2>🧪 What-If Analysis</h2>

            <p>
                Simulate how improving this student's skills
                could increase placement readiness.
            </p>

            <a
                class="button"
                href="/admin/what-if"
            >
                🔮 Open What-If Simulator
            </a>

        </div>

    </div>

    </body>

    </html>
    """


# ============================================================
# ADMIN WHAT-IF SIMULATOR
# ============================================================

@app.route("/admin/what-if", methods=["GET", "POST"])
def admin_what_if():

    if not session.get("admin_logged_in"):
        return redirect("/admin")

    result_message = ""

    if request.method == "POST":

        student = request.form.get(
            "student",
            ""
        )

        try:

            new_aptitude = float(
                request.form.get(
                    "aptitude",
                    0
                )
            )

            new_technical = float(
                request.form.get(
                    "technical",
                    0
                )
            )

            new_communication = float(
                request.form.get(
                    "communication",
                    0
                )
            )

        except ValueError:

            new_aptitude = 0
            new_technical = 0
            new_communication = 0

        # Keep values between 0 and 100

        new_aptitude = max(
            0,
            min(100, new_aptitude)
        )

        new_technical = max(
            0,
            min(100, new_technical)
        )

        new_communication = max(
            0,
            min(100, new_communication)
        )

        new_overall = (
            new_aptitude +
            new_technical +
            new_communication
        ) / 3

        if new_overall >= 80:

            level = "Excellent Placement Readiness"

        elif new_overall >= 70:

            level = "Placement Ready"

        elif new_overall >= 50:

            level = "Needs Development"

        else:

            level = "High Risk"

        result_message = f"""

        <div class="success-box">

            <h2>🔮 Simulation Result</h2>

            <h3>
                {escape(student)}
            </h3>

            <p>
                Projected Aptitude:
                <b>{new_aptitude:.0f}%</b>
            </p>

            <p>
                Projected Technical:
                <b>{new_technical:.0f}%</b>
            </p>

            <p>
                Projected Communication:
                <b>{new_communication:.0f}%</b>
            </p>

            <hr>

            <h2>
                Projected Readiness:
                {new_overall:.0f}%
            </h2>

            <p>
                Classification:
                <b>{level}</b>
            </p>

        </div>

        """

    student_options = ""

    for student in users:

        selected = ""

        if request.method == "POST":

            if request.form.get("student") == student:

                selected = "selected"

        student_options += f"""
        <option
            value="{escape(student)}"
            {selected}
        >
            {escape(student)}
        </option>
        """

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>What-If Simulator</title>

        {page_style()}

    </head>

    <body>

    <div class="header">

        <h1>🧪 Placement What-If Simulator</h1>

        <p>
            Simulate how skill improvement can change
            placement readiness.
        </p>

    </div>

    <div class="container">

        <div class="admin-nav">

            <a
                class="button"
                href="/admin/dashboard"
            >
                ← Admin Dashboard
            </a>

            <a
                class="button"
                href="/admin/students"
            >
                👥 All Students
            </a>

            <a
                class="button"
                href="/admin/logout"
            >
                🚪 Logout
            </a>

        </div>

        <div class="card">

            <h2>🔮 Student Simulation</h2>

            <p>
                Select a student and enter projected scores.
            </p>

            <form method="POST">

                <label>

                    <b>Student</b>

                </label>

                <select
                    name="student"
                    required
                >

                    <option value="">
                        Select Student
                    </option>

                    {student_options}

                </select>

                <br><br>

                <label>

                    <b>Projected Aptitude</b>

                </label>

                <input
                    type="number"
                    name="aptitude"
                    min="0"
                    max="100"
                    placeholder="Example: 75"
                    required
                >

                <br>

                <label>

                    <b>Projected Technical</b>

                </label>

                <input
                    type="number"
                    name="technical"
                    min="0"
                    max="100"
                    placeholder="Example: 80"
                    required
                >

                <br>

                <label>

                    <b>Projected Communication</b>

                </label>

                <input
                    type="number"
                    name="communication"
                    min="0"
                    max="100"
                    placeholder="Example: 85"
                    required
                >

                <br><br>

                <button
                    class="button"
                    type="submit"
                    style="width:100%;"
                >
                    🔮 Calculate Projected Readiness
                </button>

            </form>

            {result_message}

        </div>

    </div>

    </body>

    </html>
    """


# ============================================================
# ADMIN LOGOUT
# ============================================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect("/admin")


# ============================================================
# PLACEMENT INTERVIEW SIMULATOR
# ============================================================

@app.route("/simulator", methods=["GET", "POST"])
def simulator():

    if not session.get("student_logged_in"):
        return redirect("/")

    if request.method == "POST":

        answer1 = request.form.get(
            "answer1",
            ""
        )

        answer2 = request.form.get(
            "answer2",
            ""
        )

        answer3 = request.form.get(
            "answer3",
            ""
        )

        score = 0

        if len(answer1.strip()) >= 20:
            score += 1

        if len(answer2.strip()) >= 20:
            score += 1

        if len(answer3.strip()) >= 20:
            score += 1

        percentage = int(
            (score / 3) * 100
        )

        if percentage >= 80:

            message = (
                "Excellent! You show strong interview readiness."
            )

        elif percentage >= 50:

            message = (
                "Good start! Improve your answers "
                "with more detail."
            )

        else:

            message = (
                "Needs Improvement. Practice interview "
                "communication."
            )

        return f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>Simulator Result</title>

            {page_style()}

        </head>

        <body>

        <div class="header">

            <h1>🚀 Placement Simulator Result</h1>

        </div>

        <div class="container">

            <div class="card center">

                <h2>
                    Interview Readiness Score
                </h2>

                <div class="value">
                    {percentage}%
                </div>

                <br>

                <div class="info-box">

                    {message}

                </div>

                <br>

                <a
                    class="button"
                    href="/dashboard"
                >
                    📊 Back to Dashboard
                </a>

            </div>

        </div>

        </body>

        </html>
        """

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Placement Simulator</title>

    """ + page_style() + """

    </head>

    <body>

    <div class="header">

        <h1>🚀 Placement Simulator</h1>

        <p>
            Practice your interview skills
        </p>

    </div>

    <div class="container">

        <form method="POST">

            <div class="card">

                <h3>
                    1. Tell us about yourself.
                </h3>

                <textarea
                    name="answer1"
                    required
                    style="height:120px;"
                ></textarea>

            </div>

            <div class="card">

                <h3>
                    2. Why should we hire you?
                </h3>

                <textarea
                    name="answer2"
                    required
                    style="height:120px;"
                ></textarea>

            </div>

            <div class="card">

                <h3>
                    3. What are your career goals?
                </h3>

                <textarea
                    name="answer3"
                    required
                    style="height:120px;"
                ></textarea>

            </div>

            <button
                class="button"
                type="submit"
                style="width:100%;"
            >
                🎯 Submit Interview
            </button>

        </form>

    </div>

    </body>

    </html>
    """


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )