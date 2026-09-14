
from flask import Flask, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "careconnect.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():

    conn = get_db()

    # ---------------- RESIDENTS ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS residents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            gender TEXT NOT NULL,
            room TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    """)

    # ---------------- ROOMS ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT NOT NULL,
            capacity TEXT NOT NULL
        )
    """)

    # ---------------- DOCTORS ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            hospital TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    """)

    # ---------------- HOSPITALS ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hospitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    """)

    # ---------------- MEDICINES ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL,
            medicine TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL,
            date_time TEXT NOT NULL
        )
    """)

    # ---------------- HEALTH ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL,
            temperature TEXT NOT NULL,
            bp TEXT NOT NULL,
            pulse TEXT NOT NULL,
            oxygen TEXT NOT NULL,
            weight TEXT NOT NULL,
            condition TEXT NOT NULL,
            doctor TEXT NOT NULL,
            date_time TEXT NOT NULL
        )
    """)

    # ---------------- VISITORS ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor TEXT NOT NULL,
            resident TEXT NOT NULL,
            relation TEXT NOT NULL,
            contact TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            purpose TEXT NOT NULL
        )
    """)

    # ---------------- CARETAKERS ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS caretakers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            duty_time TEXT NOT NULL,
            duties TEXT NOT NULL
        )
    """)

    # ---------------- MEALS ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL,
            breakfast TEXT NOT NULL,
            lunch TEXT NOT NULL,
            dinner TEXT NOT NULL,
            water TEXT NOT NULL,
            notes TEXT NOT NULL,
            date_time TEXT NOT NULL
        )
    """)

    # ---------------- DAILY CARE ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dailycare (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL,
            food TEXT NOT NULL,
            water TEXT NOT NULL,
            activity TEXT NOT NULL,
            condition TEXT NOT NULL,
            date_time TEXT NOT NULL
        )
    """)

    # ---------------- APPOINTMENTS ----------------
    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL,
            doctor TEXT NOT NULL,
            hospital TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # =====================================================
    # EMERGENCY TABLE
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL,
            room TEXT NOT NULL,
            problem TEXT NOT NULL,
            date_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# LOGIN
# =========================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            return redirect("/dashboard")

        return """
        <h2>❌ Invalid username or password</h2>
        <a href="/">⬅ Try Again</a>
        """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CareConnect Login</title>
    </head>

    <body>

        <h1>🏠 CARECONNECT</h1>
        <h2>NEST CARE HOME</h2>

        <form method="POST">

            Username:<br>
            <input type="text" name="username" required>
            <br><br>

            Password:<br>
            <input type="password" name="password" required>
            <br><br>

            <button type="submit">🔐 Login</button>

        </form>

    </body>
    </html>
    """


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    return """
    <!DOCTYPE html>
    <html>

    <head>
        <title>CareConnect Dashboard</title>
    </head>

    <body>

        <h1>🏠 CARECONNECT</h1>
        <h2>NEST CARE HOME • Smart Care Management</h2>

        <hr>

        <h2>📋 Management</h2>

        <a href="/residents">
            <button>👨‍🦳 Residents</button>
        </a>

        <a href="/rooms">
            <button>🚪 Rooms</button>
        </a>

        <a href="/doctors">
            <button>👨‍⚕️ Doctors</button>
        </a>

        <a href="/hospitals">
            <button>🏥 Hospitals</button>
        </a>

        <hr>

        <h2>❤️ Health & Care</h2>

        <a href="/health">
            <button>❤️ Health</button>
        </a>

        <a href="/medicines">
            <button>💊 Medicines</button>
        </a>

        <a href="/meals">
            <button>🍽️ Meals</button>
        </a>

        <a href="/dailycare">
            <button>🧑‍⚕️ Daily Care</button>
        </a>

        <hr>

        <h2>👥 People</h2>

        <a href="/visitors">
            <button>👥 Visitors</button>
        </a>

        <a href="/caretakers">
            <button>🧑‍⚕️ Caretakers</button>
        </a>

        <hr>

        <h2>📅 Management</h2>

        <a href="/appointments">
            <button>📅 Appointments</button>
        </a>

        <a href="/emergency">
            <button>🚨 Emergency</button>
        </a>

        <hr>

        <a href="/">
            <button>🚪 Logout</button>
        </a>

    </body>
    </html>
    """


# =========================================================
# RESIDENTS
# =========================================================

@app.route("/residents", methods=["GET", "POST"])
def residents():

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        room = request.form["room"]
        contact = request.form["contact"]

        conn.execute("""
            INSERT INTO residents
            (name, age, gender, room, contact)
            VALUES (?, ?, ?, ?, ?)
        """, (name, age, gender, room, contact))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM residents ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>👨‍🦳 Residents</h1>

    <form method="POST">

        Name:<br>
        <input name="name" required><br><br>

        Age:<br>
        <input name="age" required><br><br>

        Gender:<br>
        <input name="gender" required><br><br>

        Room:<br>
        <input name="room" required><br><br>

        Contact:<br>
        <input name="contact" required><br><br>

        <button type="submit">➕ Add Resident</button>

    </form>

    <hr>

    <h2>Resident List</h2>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Age</th>
        <th>Gender</th>
        <th>Room</th>
        <th>Contact</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['name']}</td>
            <td>{row['age']}</td>
            <td>{row['gender']}</td>
            <td>{row['room']}</td>
            <td>{row['contact']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# ROOMS
# =========================================================

@app.route("/rooms", methods=["GET", "POST"])
def rooms():

    conn = get_db()

    if request.method == "POST":

        room = request.form["room"]
        capacity = request.form["capacity"]

        conn.execute("""
            INSERT INTO rooms
            (room, capacity)
            VALUES (?, ?)
        """, (room, capacity))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM rooms ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>🚪 Rooms</h1>

    <form method="POST">

        Room Number:<br>
        <input name="room" required><br><br>

        Capacity:<br>
        <input name="capacity" required><br><br>

        <button type="submit">➕ Add Room</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Room</th>
        <th>Capacity</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['room']}</td>
            <td>{row['capacity']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# DOCTORS
# =========================================================

@app.route("/doctors", methods=["GET", "POST"])
def doctors():

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        specialization = request.form["specialization"]
        hospital = request.form["hospital"]
        contact = request.form["contact"]

        conn.execute("""
            INSERT INTO doctors
            (name, specialization, hospital, contact)
            VALUES (?, ?, ?, ?)
        """, (name, specialization, hospital, contact))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM doctors ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>👨‍⚕️ Doctors</h1>

    <form method="POST">

        Doctor Name:<br>
        <input name="name" required><br><br>

        Specialization:<br>
        <input name="specialization" required><br><br>

        Hospital:<br>
        <input name="hospital" required><br><br>

        Contact:<br>
        <input name="contact" required><br><br>

        <button type="submit">➕ Add Doctor</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Specialization</th>
        <th>Hospital</th>
        <th>Contact</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['name']}</td>
            <td>{row['specialization']}</td>
            <td>{row['hospital']}</td>
            <td>{row['contact']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# HOSPITALS
# =========================================================

@app.route("/hospitals", methods=["GET", "POST"])
def hospitals():

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        address = request.form["address"]
        contact = request.form["contact"]

        conn.execute("""
            INSERT INTO hospitals
            (name, address, contact)
            VALUES (?, ?, ?)
        """, (name, address, contact))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM hospitals ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>🏥 Hospitals</h1>

    <form method="POST">

        Hospital Name:<br>
        <input name="name" required><br><br>

        Address:<br>
        <input name="address" required><br><br>

        Contact:<br>
        <input name="contact" required><br><br>

        <button type="submit">➕ Add Hospital</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Address</th>
        <th>Contact</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['name']}</td>
            <td>{row['address']}</td>
            <td>{row['contact']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# MEDICINES
# =========================================================

@app.route("/medicines", methods=["GET", "POST"])
def medicines():

    conn = get_db()

    if request.method == "POST":

        resident = request.form["resident"]
        medicine = request.form["medicine"]
        time = request.form["time"]
        status = request.form["status"]

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn.execute("""
            INSERT INTO medicines
            (resident, medicine, time, status, date_time)
            VALUES (?, ?, ?, ?, ?)
        """, (resident, medicine, time, status, date_time))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM medicines ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>💊 Medicines</h1>

    <form method="POST">

        Resident:<br>
        <input name="resident" required><br><br>

        Medicine:<br>
        <input name="medicine" required><br><br>

        Time:<br>
        <input name="time" required><br><br>

        Status:<br>
        <input name="status" required><br><br>

        <button type="submit">💊 Add Medicine</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Resident</th>
        <th>Medicine</th>
        <th>Time</th>
        <th>Status</th>
        <th>Date & Time</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['resident']}</td>
            <td>{row['medicine']}</td>
            <td>{row['time']}</td>
            <td>{row['status']}</td>
            <td>{row['date_time']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# HEALTH
# =========================================================

@app.route("/health", methods=["GET", "POST"])
def health():

    conn = get_db()

    if request.method == "POST":

        resident = request.form["resident"]
        temperature = request.form["temperature"]
        bp = request.form["bp"]
        pulse = request.form["pulse"]
        oxygen = request.form["oxygen"]
        weight = request.form["weight"]
        condition = request.form["condition"]
        doctor = request.form["doctor"]

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn.execute("""
            INSERT INTO health
            (resident, temperature, bp, pulse, oxygen,
             weight, condition, doctor, date_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            resident,
            temperature,
            bp,
            pulse,
            oxygen,
            weight,
            condition,
            doctor,
            date_time
        ))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM health ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>❤️ Health Records</h1>

    <form method="POST">

        Resident:<br>
        <input name="resident" required><br><br>

        Temperature:<br>
        <input name="temperature" required><br><br>

        Blood Pressure:<br>
        <input name="bp" required><br><br>

        Pulse:<br>
        <input name="pulse" required><br><br>

        Oxygen:<br>
        <input name="oxygen" required><br><br>

        Weight:<br>
        <input name="weight" required><br><br>

        Condition:<br>
        <input name="condition" required><br><br>

        Doctor:<br>
        <input name="doctor" required><br><br>

        <button type="submit">➕ Add Health Record</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Resident</th>
        <th>Temperature</th>
        <th>BP</th>
        <th>Pulse</th>
        <th>Oxygen</th>
        <th>Weight</th>
        <th>Condition</th>
        <th>Doctor</th>
        <th>Date & Time</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['resident']}</td>
            <td>{row['temperature']}</td>
            <td>{row['bp']}</td>
            <td>{row['pulse']}</td>
            <td>{row['oxygen']}</td>
            <td>{row['weight']}</td>
            <td>{row['condition']}</td>
            <td>{row['doctor']}</td>
            <td>{row['date_time']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# VISITORS
# =========================================================

@app.route("/visitors", methods=["GET", "POST"])
def visitors():

    conn = get_db()

    if request.method == "POST":

        visitor = request.form["visitor"]
        resident = request.form["resident"]
        relation = request.form["relation"]
        contact = request.form["contact"]
        date = request.form["date"]
        time = request.form["time"]
        purpose = request.form["purpose"]

        conn.execute("""
            INSERT INTO visitors
            (visitor, resident, relation, contact, date, time, purpose)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            visitor,
            resident,
            relation,
            contact,
            date,
            time,
            purpose
        ))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM visitors ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>👥 Visitors</h1>

    <form method="POST">

        Visitor Name:<br>
        <input name="visitor" required><br><br>

        Resident:<br>
        <input name="resident" required><br><br>

        Relation:<br>
        <input name="relation" required><br><br>

        Contact:<br>
        <input name="contact" required><br><br>

        Date:<br>
        <input type="date" name="date" required><br><br>

        Time:<br>
        <input type="time" name="time" required><br><br>

        Purpose:<br>
        <input name="purpose" required><br><br>

        <button type="submit">➕ Add Visitor</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Visitor</th>
        <th>Resident</th>
        <th>Relation</th>
        <th>Contact</th>
        <th>Date</th>
        <th>Time</th>
        <th>Purpose</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['visitor']}</td>
            <td>{row['resident']}</td>
            <td>{row['relation']}</td>
            <td>{row['contact']}</td>
            <td>{row['date']}</td>
            <td>{row['time']}</td>
            <td>{row['purpose']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# CARETAKERS
# =========================================================

@app.route("/caretakers", methods=["GET", "POST"])
def caretakers():

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        contact = request.form["contact"]
        duty_time = request.form["duty_time"]
        duties = request.form["duties"]

        conn.execute("""
            INSERT INTO caretakers
            (name, contact, duty_time, duties)
            VALUES (?, ?, ?, ?)
        """, (name, contact, duty_time, duties))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM caretakers ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>🧑‍⚕️ Caretakers</h1>

    <form method="POST">

        Name:<br>
        <input name="name" required><br><br>

        Contact:<br>
        <input name="contact" required><br><br>

        Duty Time:<br>
        <input name="duty_time" required><br><br>

        Duties:<br>
        <input name="duties" required><br><br>

        <button type="submit">➕ Add Caretaker</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Contact</th>
        <th>Duty Time</th>
        <th>Duties</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['name']}</td>
            <td>{row['contact']}</td>
            <td>{row['duty_time']}</td>
            <td>{row['duties']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# MEALS
# =========================================================

@app.route("/meals", methods=["GET", "POST"])
def meals():

    conn = get_db()

    if request.method == "POST":

        resident = request.form["resident"]
        breakfast = request.form["breakfast"]
        lunch = request.form["lunch"]
        dinner = request.form["dinner"]
        water = request.form["water"]
        notes = request.form["notes"]

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn.execute("""
            INSERT INTO meals
            (resident, breakfast, lunch, dinner, water, notes, date_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            resident,
            breakfast,
            lunch,
            dinner,
            water,
            notes,
            date_time
        ))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM meals ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>🍽️ Meals</h1>

    <form method="POST">

        Resident:<br>
        <input name="resident" required><br><br>

        Breakfast:<br>
        <input name="breakfast" required><br><br>

        Lunch:<br>
        <input name="lunch" required><br><br>

        Dinner:<br>
        <input name="dinner" required><br><br>

        Water:<br>
        <input name="water" required><br><br>

        Notes:<br>
        <input name="notes" required><br><br>

        <button type="submit">➕ Add Meal Record</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Resident</th>
        <th>Breakfast</th>
        <th>Lunch</th>
        <th>Dinner</th>
        <th>Water</th>
        <th>Notes</th>
        <th>Date & Time</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['resident']}</td>
            <td>{row['breakfast']}</td>
            <td>{row['lunch']}</td>
            <td>{row['dinner']}</td>
            <td>{row['water']}</td>
            <td>{row['notes']}</td>
            <td>{row['date_time']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# DAILY CARE
# =========================================================

@app.route("/dailycare", methods=["GET", "POST"])
def dailycare():

    conn = get_db()

    if request.method == "POST":

        resident = request.form["resident"]
        food = request.form["food"]
        water = request.form["water"]
        activity = request.form["activity"]
        condition = request.form["condition"]

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn.execute("""
            INSERT INTO dailycare
            (resident, food, water, activity, condition, date_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            resident,
            food,
            water,
            activity,
            condition,
            date_time
        ))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM dailycare ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>🧑‍⚕️ Daily Care</h1>

    <form method="POST">

        Resident:<br>
        <input name="resident" required><br><br>

        Food:<br>
        <input name="food" required><br><br>

        Water:<br>
        <input name="water" required><br><br>

        Activity:<br>
        <input name="activity" required><br><br>

        Condition:<br>
        <input name="condition" required><br><br>

        <button type="submit">➕ Add Daily Care</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Resident</th>
        <th>Food</th>
        <th>Water</th>
        <th>Activity</th>
        <th>Condition</th>
        <th>Date & Time</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['resident']}</td>
            <td>{row['food']}</td>
            <td>{row['water']}</td>
            <td>{row['activity']}</td>
            <td>{row['condition']}</td>
            <td>{row['date_time']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# APPOINTMENTS
# =========================================================

@app.route("/appointments", methods=["GET", "POST"])
def appointments():

    conn = get_db()

    if request.method == "POST":

        resident = request.form["resident"]
        doctor = request.form["doctor"]
        hospital = request.form["hospital"]
        date = request.form["date"]
        time = request.form["time"]
        reason = request.form["reason"]
        status = request.form["status"]

        conn.execute("""
            INSERT INTO appointments
            (resident, doctor, hospital, date, time, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            resident,
            doctor,
            hospital,
            date,
            time,
            reason,
            status
        ))

        conn.commit()

    rows = conn.execute(
        "SELECT * FROM appointments ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = """
    <h1>📅 Appointments</h1>

    <form method="POST">

        Resident:<br>
        <input name="resident" required><br><br>

        Doctor:<br>
        <input name="doctor" required><br><br>

        Hospital:<br>
        <input name="hospital" required><br><br>

        Date:<br>
        <input type="date" name="date" required><br><br>

        Time:<br>
        <input type="time" name="time" required><br><br>

        Reason:<br>
        <input name="reason" required><br><br>

        Status:<br>
        <input name="status" value="Scheduled" required><br><br>

        <button type="submit">📅 Add Appointment</button>

    </form>

    <hr>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Resident</th>
        <th>Doctor</th>
        <th>Hospital</th>
        <th>Date</th>
        <th>Time</th>
        <th>Reason</th>
        <th>Status</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['resident']}</td>
            <td>{row['doctor']}</td>
            <td>{row['hospital']}</td>
            <td>{row['date']}</td>
            <td>{row['time']}</td>
            <td>{row['reason']}</td>
            <td>{row['status']}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>
    """

    return html


# =========================================================
# 🚨 EMERGENCY
# =========================================================

@app.route("/emergency", methods=["GET", "POST"])
def emergency():

    conn = get_db()

    # ---------- SAVE EMERGENCY ----------
    if request.method == "POST":

        resident = request.form["resident"]
        room = request.form["room"]
        problem = request.form["problem"]

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn.execute("""
            INSERT INTO emergencies
            (resident, room, problem, date_time)
            VALUES (?, ?, ?, ?)
        """, (
            resident,
            room,
            problem,
            date_time
        ))

        conn.commit()

    # ---------- GET RECORDS ----------
    rows = conn.execute("""
        SELECT * FROM emergencies
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    html = """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Emergency Records</title>
    </head>

    <body>

    <h1>🚨 Emergency Records</h1>

    <h2>Record New Emergency</h2>

    <form method="POST">

        Resident Name:<br>
        <input
            type="text"
            name="resident"
            placeholder="Enter resident name"
            required
        >
        <br><br>

        Room:<br>
        <input
            type="text"
            name="room"
            placeholder="Enter room number"
            required
        >
        <br><br>

        Emergency Problem:<br>
        <input
            type="text"
            name="problem"
            placeholder="Enter emergency problem"
            required
        >
        <br><br>

        <button type="submit">
            🚨 Record Emergency
        </button>

    </form>

    <hr>

    <h2>🚨 Emergency History</h2>

    <table border="1" cellpadding="8">

    <tr>
        <th>ID</th>
        <th>Resident</th>
        <th>Room</th>
        <th>Problem</th>
        <th>Date & Time</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row['id']}</td>
            <td>{row['resident']}</td>
            <td>{row['room']}</td>
            <td>{row['problem']}</td>
            <td>{row['date_time']}</td>
        </tr>
        """

    html += """
    </table>

    <br><br>

    <a href="/dashboard">
        <button>⬅ Dashboard</button>
    </a>

    </body>
    </html>
    """

    return html


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)