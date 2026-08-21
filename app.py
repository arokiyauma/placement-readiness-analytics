from flask import Flask, request, redirect

app = Flask(__name__)

# ============================================================
# USER ACCOUNTS
# ============================================================

users = {
    "AROKIYAUMA": "2425"
}

# ============================================================
# LATEST ASSESSMENT RESULT
# ============================================================

assessment_result = {
    "student": "Student",
    "aptitude": 0,
    "technical": 0,
    "communication": 0,
    "overall": 0,
    "aptitude_status": "",
    "technical_status": "",
    "communication_status": "",
    "recommended_focus": "",
    "career_path": "",
    "recommended_skills": "",
    "suitable_roles": ""
}


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
        max-width: 1100px;
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

    input[type="text"],
    input[type="password"] {
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

    @media(max-width:600px) {
        .container {
            width: 95%;
        }
    }

    </style>
    """


# ============================================================
# LOGIN PAGE
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
            <p>AI-Based Student Placement Assessment System</p>
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

                </div>

            </div>

        </div>

    </body>
    </html>
    """


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["POST"])
def do_login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username] == password:
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
# CREATE ACCOUNT
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

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

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>Student Search</title>

    """ + page_style() + """

    </head>

    <body>

        <div class="header">

            <h1>🎓 Placement Readiness Analytics</h1>

            <p>Student Search</p>

        </div>

        <div class="container">

            <div class="card"
                 style="max-width:600px;margin:60px auto;">

                <div class="center">

                    <h2>👤 Find Student</h2>

                    <p>
                        Enter the student's name
                        to begin the assessment.
                    </p>

                </div>

                <form action="/assessment" method="GET">

                    <input
                        type="text"
                        name="student"
                        placeholder="Enter Student Name"
                        required
                    >

                    <br><br>

                    <button
                        class="button"
                        type="submit"
                        style="width:100%;"
                    >
                        📝 Take Assessment
                    </button>

                </form>

            </div>

        </div>

    </body>

    </html>
    """


# ============================================================
# ASSESSMENT
# ============================================================

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    questions = [

        ("q1",
         "1. If 20% of a number is 50, what is the number?",
         ["200", "250", "300", "150"], "250"),

        ("q2",
         "2. What is 15 + 25?",
         ["30", "35", "40", "45"], "40"),

        ("q3",
         "3. What is 12 × 5?",
         ["50", "60", "70", "80"], "60"),

        ("q4",
         "4. What is 100 ÷ 4?",
         ["20", "25", "30", "40"], "25"),

        ("q5",
         "5. What is 25% of 200?",
         ["25", "40", "50", "60"], "50"),

        ("q6",
         "6. If 5 pens cost ₹50, what is one pen?",
         ["₹5", "₹10", "₹15", "₹20"], "₹10"),

        ("q7",
         "7. What is the next number: 2, 4, 6, 8, ?",
         ["9", "10", "11", "12"], "10"),

        ("q8",
         "8. What is 10% of 500?",
         ["25", "40", "50", "60"], "50"),

        ("q9",
         "9. A car travels 60 km in 1 hour. How far in 3 hours?",
         ["120 km", "150 km", "180 km", "200 km"], "180 km"),

        ("q10",
         "10. What is 7²?",
         ["14", "21", "49", "56"], "49"),

        ("q11",
         "11. Which language is commonly used for data analysis?",
         ["Python", "HTML", "CSS", "XML"], "Python"),

        ("q12",
         "12. Which Python library is used for data manipulation?",
         ["Pandas", "Flask", "Tkinter", "Requests"], "Pandas"),

        ("q13",
         "13. Which language is used to query databases?",
         ["SQL", "HTML", "CSS", "XML"], "SQL"),

        ("q14",
         "14. Which Python library is used for numerical calculations?",
         ["NumPy", "Flask", "Django", "Requests"], "NumPy"),

        ("q15",
         "15. Which tool is commonly used for data visualization?",
         ["Power BI", "Notepad", "Paint", "Calculator"], "Power BI"),

        ("q16",
         "16. What does SQL stand for?",
         [
             "Structured Query Language",
             "Simple Query Language",
             "System Query Language",
             "Standard Question Language"
         ],
         "Structured Query Language"),

        ("q17",
         "17. Which Python data structure uses key-value pairs?",
         ["List", "Tuple", "Dictionary", "Set"],
         "Dictionary"),

        ("q18",
         "18. Which keyword defines a function in Python?",
         ["function", "def", "fun", "define"], "def"),

        ("q19",
         "19. Which one is a Python data type?",
         ["Integer", "Website", "Browser", "Server"],
         "Integer"),

        ("q20",
         "20. What does CSV stand for?",
         [
             "Comma-Separated Values",
             "Computer Stored Values",
             "Common System Values",
             "Column Stored Variables"
         ],
         "Comma-Separated Values"),

        ("q21",
         "21. Choose the grammatically correct sentence.",
         [
             "She go to college.",
             "She goes to college.",
             "She going college.",
             "She gone college."
         ],
         "She goes to college."),

        ("q22",
         "22. Choose the correct word: I ___ a student.",
         ["am", "is", "are", "be"], "am"),

        ("q23",
         "23. Choose the correct sentence.",
         [
             "He have a car.",
             "He has a car.",
             "He having a car.",
             "He had have a car."
         ],
         "He has a car."),

        ("q24",
         "24. What is the opposite of Strong?",
         ["Powerful", "Weak", "Brave", "Hard"], "Weak"),

        ("q25",
         "25. What is the synonym of Happy?",
         ["Sad", "Angry", "Joyful", "Tired"], "Joyful"),

        ("q26",
         "26. Choose the correct sentence.",
         [
             "They is playing.",
             "They are playing.",
             "They am playing.",
             "They be playing."
         ],
         "They are playing."),

        ("q27",
         "27. Choose the correct word: She ___ English very well.",
         ["speak", "speaks", "speaking", "spoken"], "speaks"),

        ("q28",
         "28. What is the opposite of Early?",
         ["Fast", "Late", "Quick", "Soon"], "Late"),

        ("q29",
         "29. Choose the correct sentence.",
         [
             "I have completed my work.",
             "I has completed my work.",
             "I completing my work.",
             "I completed have work."
         ],
         "I have completed my work."),

        ("q30",
         "30. What is the synonym of Begin?",
         ["End", "Start", "Stop", "Finish"], "Start")
    ]

    # ========================================================
    # CHECK ANSWERS
    # ========================================================

    if request.method == "POST":

        student = request.form.get("student", "Student")

        aptitude_correct = 0
        technical_correct = 0
        communication_correct = 0

        for i in range(0, 10):

            q_id, question, options, answer = questions[i]

            if request.form.get(q_id) == answer:
                aptitude_correct += 1

        for i in range(10, 20):

            q_id, question, options, answer = questions[i]

            if request.form.get(q_id) == answer:
                technical_correct += 1

        for i in range(20, 30):

            q_id, question, options, answer = questions[i]

            if request.form.get(q_id) == answer:
                communication_correct += 1

        aptitude = aptitude_correct * 10
        technical = technical_correct * 10
        communication = communication_correct * 10

        def get_skill_status(score):

            if score >= 80:
                return "Strong"

            elif score >= 60:
                return "Good"

            return "Needs Improvement"

        aptitude_status = get_skill_status(aptitude)
        technical_status = get_skill_status(technical)
        communication_status = get_skill_status(communication)

        skills = {
            "Aptitude": aptitude,
            "Technical": technical,
            "Communication": communication
        }

        recommended_focus = min(skills, key=skills.get)

        overall = (
            aptitude +
            technical +
            communication
        ) / 3

        if technical >= 80 and aptitude >= 60:

            career_path = "Junior Software Developer"

            recommended_skills = (
                "Python, SQL, Programming, Problem Solving"
            )

            suitable_roles = (
                "Python Developer, Software Developer, "
                "Junior Data Analyst"
            )

        elif technical >= 70 and communication >= 70:

            career_path = "Data Analyst"

            recommended_skills = (
                "Python, SQL, Power BI, Data Visualization"
            )

            suitable_roles = (
                "Data Analyst, BI Analyst, Reporting Analyst"
            )

        elif communication >= 80:

            career_path = "Business Analyst"

            recommended_skills = (
                "Communication, Excel, Business Analysis"
            )

            suitable_roles = (
                "Business Analyst, Customer Support Analyst"
            )

        else:

            career_path = "Placement Preparation"

            recommended_skills = (
                "Aptitude, Technical Skills, Communication"
            )

            suitable_roles = (
                "Trainee, Junior Analyst, Graduate Trainee"
            )

        assessment_result["student"] = student
        assessment_result["aptitude"] = aptitude
        assessment_result["technical"] = technical
        assessment_result["communication"] = communication
        assessment_result["overall"] = overall

        assessment_result["aptitude_status"] = aptitude_status
        assessment_result["technical_status"] = technical_status
        assessment_result["communication_status"] = communication_status

        assessment_result["recommended_focus"] = recommended_focus

        assessment_result["career_path"] = career_path
        assessment_result["recommended_skills"] = recommended_skills
        assessment_result["suitable_roles"] = suitable_roles

        return redirect("/dashboard")

    # ========================================================
    # DISPLAY QUESTIONS
    # ========================================================

    student = request.args.get("student", "Student")

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
            Student: <b>{student}</b>
        </p>

    </div>

    <div class="container">

        <form method="POST" action="/assessment">

            <input
                type="hidden"
                name="student"
                value="{student}"
            >

    """

    for index, (q_id, question, options, answer) in enumerate(questions):

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
                    value="{option}"
                    required
                >

                {option}

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
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    student = assessment_result["student"]

    aptitude = assessment_result["aptitude"]
    technical = assessment_result["technical"]
    communication = assessment_result["communication"]
    overall = assessment_result["overall"]

    aptitude_status = assessment_result["aptitude_status"]
    technical_status = assessment_result["technical_status"]
    communication_status = assessment_result["communication_status"]

    recommended_focus = assessment_result["recommended_focus"]

    career_path = assessment_result["career_path"]
    recommended_skills = assessment_result["recommended_skills"]
    suitable_roles = assessment_result["suitable_roles"]

    def status_class(status):

        if status == "Strong":
            return "strong"

        if status == "Good":
            return "good"

        return "weak"

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

        <p>Student Performance Analytics</p>

    </div>

    <div class="container">

        <div class="card">

            <h2>👤 {student}</h2>

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

            <p><b>Academic Performance</b></p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:81%;"
                >
                    81%
                </div>

            </div>

            <p><b>Aptitude</b></p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:{aptitude}%;"
                >
                    {aptitude}%
                </div>

            </div>

            <p><b>Technical</b></p>

            <div class="bar">

                <div
                    class="fill"
                    style="width:{technical}%;"
                >
                    {technical}%
                </div>

            </div>

            <p><b>Communication</b></p>

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

                Improve: {recommended_focus}

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

            <div class="status strong">

                READY FOR PLACEMENT ANALYSIS

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
                href="/assessment?student={student}"
            >
                🔄 Take Assessment Again
            </a>

        </div>

    </div>

    </body>

    </html>
    """


# ============================================================
# PLACEMENT SIMULATOR
# ============================================================

@app.route("/simulator", methods=["GET", "POST"])
def simulator():

    if request.method == "POST":

        answer1 = request.form.get("answer1")
        answer2 = request.form.get("answer2")
        answer3 = request.form.get("answer3")

        score = 0

        if answer1 and len(answer1.strip()) > 20:
            score += 1

        if answer2 and len(answer2.strip()) > 20:
            score += 1

        if answer3 and len(answer3.strip()) > 20:
            score += 1

        percentage = int((score / 3) * 100)

        if percentage >= 80:

            message = (
                "Excellent! You show strong interview readiness."
            )

        elif percentage >= 50:

            message = (
                "Good start! Improve your answers with more detail."
            )

        else:

            message = (
                "Needs Improvement. Practice interview communication."
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

                <h2>Interview Readiness Score</h2>

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

        <p>Practice your interview skills</p>

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
    app.run(debug=True)