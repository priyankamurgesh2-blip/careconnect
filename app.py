
from flask import Flask, request, redirect, send_from_directory, session
from functools import wraps
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "careconnect.db")
app.secret_key = os.environ.get("SECRET_KEY", "careconnect-secret-change-this")
ADMIN_USERNAME = os.environ.get("CARECONNECT_USERNAME", "priya160206")
ADMIN_PASSWORD = os.environ.get("CARECONNECT_PASSWORD", "priyanka@nectcarehome")


@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")


@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")


@app.route("/sw.js")
def service_worker():
    return send_from_directory(".", "sw.js")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db()

    tables = [
        """
        CREATE TABLE IF NOT EXISTS residents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, age TEXT NOT NULL, gender TEXT NOT NULL,
            room TEXT NOT NULL, contact TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT NOT NULL, capacity TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, specialization TEXT NOT NULL,
            hospital TEXT NOT NULL, contact TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS hospitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, address TEXT NOT NULL, contact TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL, medicine TEXT NOT NULL,
            time TEXT NOT NULL, status TEXT NOT NULL, date_time TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL, temperature TEXT NOT NULL,
            bp TEXT NOT NULL, pulse TEXT NOT NULL, oxygen TEXT NOT NULL,
            weight TEXT NOT NULL, condition TEXT NOT NULL,
            doctor TEXT NOT NULL, date_time TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor TEXT NOT NULL, resident TEXT NOT NULL,
            relation TEXT NOT NULL, contact TEXT NOT NULL,
            date TEXT NOT NULL, time TEXT NOT NULL, purpose TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS caretakers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, contact TEXT NOT NULL,
            duty_time TEXT NOT NULL, duties TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL, breakfast TEXT NOT NULL,
            lunch TEXT NOT NULL, dinner TEXT NOT NULL,
            water TEXT NOT NULL, notes TEXT NOT NULL, date_time TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS dailycare (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL, food TEXT NOT NULL,
            water TEXT NOT NULL, activity TEXT NOT NULL,
            condition TEXT NOT NULL, date_time TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL, doctor TEXT NOT NULL,
            hospital TEXT NOT NULL, date TEXT NOT NULL, time TEXT NOT NULL,
            reason TEXT NOT NULL, status TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident TEXT NOT NULL, room TEXT NOT NULL,
            problem TEXT NOT NULL, date_time TEXT NOT NULL
        )
        """
    ]

    for table in tables:
        conn.execute(table)

    conn.commit()
    conn.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("staff_logged_in"):
            return redirect("/login")
        return view(*args, **kwargs)
    return wrapped


def e(value):
    from html import escape
    return escape("" if value is None else str(value))


def action_buttons(table_name, record_id):
    return f"""<div class="actions">
        <a href="/edit/{table_name}/{record_id}"><button type="button">✏️ Edit</button></a>
        <form method="POST" action="/delete/{table_name}/{record_id}" style="display:inline;" onsubmit="return confirm('Delete this record?');">
            <button type="submit" class="danger">🗑️ Delete</button>
        </form>
    </div>"""


def page(title, body, public=False):
    nav = ""
    if session.get("staff_logged_in"):
        nav = '<nav class="topnav"><a href="/dashboard">Dashboard</a><a href="/logout">Logout</a></nav>'
    elif public:
        nav = '<nav class="topnav"><a href="/">Home</a><a href="/login">Staff Login</a></nav>'
    return f"""
    <!DOCTYPE html><html><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#2563eb">
    <meta name="description" content="CareConnect - Smart Care Management for Nest Care Home">
    <title>{e(title)} - CareConnect</title>
    <link rel="stylesheet" href="/style.css"><link rel="manifest" href="/manifest.json">
    </head><body>{nav}{body}
    <script>if ("serviceWorker" in navigator) {{ window.addEventListener("load", function() {{ navigator.serviceWorker.register("/sw.js").catch(function(error) {{ console.log(error); }}); }}); }}</script>
    </body></html>"""


@app.route("/")
def home():
    return page("Nest Care Home", """
    <div class="public-hero">
      <div class="hero-card">
        <div class="hero-icon">🏠</div><p class="eyebrow">NEST CARE HOME</p>
        <h1>Compassionate Care.<br>Connected Management.</h1>
        <p class="hero-text">Welcome to Nest Care Home. CareConnect helps staff manage residents, health, medicines, meals, visitors, appointments and daily care in one place.</p>
        <div class="hero-buttons"><a href="/login"><button>🔐 Staff Login</button></a></div>
      </div>
      <div class="feature-grid">
        <div class="feature-card"><span>❤️</span><h3>Resident Care</h3><p>Organised resident and health information.</p></div>
        <div class="feature-card"><span>💊</span><h3>Medicine Management</h3><p>Track medicines and their status.</p></div>
        <div class="feature-card"><span>🍲</span><h3>Daily Care</h3><p>Record meals, water and activities.</p></div>
        <div class="feature-card"><span>🚨</span><h3>Emergency</h3><p>Quickly record emergency information.</p></div>
      </div>
      <div class="public-info"><h2>About Nest Care Home</h2><p>CareConnect is a digital care-management system for organising important staff records.</p><h2>Contact & Location</h2><p>Nest Care Home<br>Gowri Shankar Nagar, Vijayawada, Andhra Pradesh</p></div>
    </div>""", public=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USERNAME and request.form.get("password") == ADMIN_PASSWORD:
            session.clear()
            session["staff_logged_in"] = True
            session["staff_username"] = request.form.get("username")
            return redirect("/dashboard")
        message = '<p class="error">Invalid username or password.</p>'
    return page("Staff Login", f"""
    <div class="login-box"><div class="login-logo">🏠</div><p class="eyebrow">NEST CARE HOME</p><h1>Staff Login</h1><p>Secure access to CareConnect management.</p>{message}
    <form method="POST"><label>Username</label><input name="username" autocomplete="username" required><label>Password</label><input type="password" name="password" autocomplete="current-password" required><button type="submit">🔐 Login</button></form>
    <a href="/">← Back to website</a></div>""")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/dashboard")
@login_required
@login_required
def dashboard():
    db = get_db()
    counts = {
        "Residents": db.execute("SELECT COUNT(*) FROM residents").fetchone()[0],
        "Rooms": db.execute("SELECT COUNT(*) FROM rooms").fetchone()[0],
        "Doctors": db.execute("SELECT COUNT(*) FROM doctors").fetchone()[0],
        "Medicines": db.execute("SELECT COUNT(*) FROM medicines").fetchone()[0],
        "Appointments": db.execute("SELECT COUNT(*) FROM appointments").fetchone()[0],
        "Emergencies": db.execute("SELECT COUNT(*) FROM emergencies").fetchone()[0],
    }
    db.close()

    cards = "".join(
        f'<div class="stat-card"><h3>{name}</h3><strong>{count}</strong></div>'
        for name, count in counts.items()
    )

    return page("Dashboard", f"""
    <div class="topbar">
        <div>
            <h1>🏠 CARECONNECT</h1>
            <p>NEST CARE HOME • Smart Care Management</p>
        </div>
        <a href="/"><button>Logout</button></a>
    </div>

    <div class="stats">{cards}</div>

    <h2>Care Management</h2>
    <div class="menu-grid">
        <a href="/residents"><button>👴 Residents</button></a>
        <a href="/rooms"><button>🚪 Rooms</button></a>
        <a href="/doctors"><button>👨‍⚕️ Doctors</button></a>
        <a href="/hospitals"><button>🏥 Hospitals</button></a>
        <a href="/health"><button>❤️ Health</button></a>
        <a href="/medicines"><button>💊 Medicines</button></a>
        <a href="/visitors"><button>👥 Visitors</button></a>
        <a href="/caretakers"><button>🧑‍⚕️ Caretakers</button></a>
        <a href="/meals"><button>🍲 Meals</button></a>
        <a href="/dailycare"><button>📝 Daily Care</button></a>
        <a href="/appointments"><button>📅 Appointments</button></a>
        <a href="/history"><button>📜 History</button></a>
        <a href="/emergency"><button class="danger">🚨 Emergency</button></a>
    </div>
    """)


@app.route("/residents", methods=["GET", "POST"])
@login_required
@login_required
def residents():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO residents (name,age,gender,room,contact) VALUES (?,?,?,?,?)",
                   tuple(request.form[x] for x in ("name","age","gender","room","contact")))
        db.commit()
    rows = db.execute("SELECT * FROM residents ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(
        f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['age']}</td><td>{r['gender']}</td><td>{r['room']}</td><td>{r['contact']}</td><td>{action_buttons('residents', r['id'])}</td></tr>"
        for r in rows)
    return page("Residents", f"""
    <h1>👴 Residents</h1>
    <form method="POST">
        <label>Name</label><input name="name" required>
        <label>Age</label><input name="age" required>
        <label>Gender</label><input name="gender" required>
        <label>Room</label><input name="room" required>
        <label>Contact</label><input name="contact" required>
        <button>Add Resident</button>
    </form>
    <h2>Resident List</h2>
    <table><tr><th>ID</th><th>Name</th><th>Age</th><th>Gender</th><th>Room</th><th>Contact</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/rooms", methods=["GET", "POST"])
@login_required
@login_required
def rooms():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO rooms (room,capacity) VALUES (?,?)",
                   (request.form["room"], request.form["capacity"]))
        db.commit()
    rows = db.execute("SELECT * FROM rooms ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['room']}</td><td>{r['capacity']}</td><td>{action_buttons('rooms', r['id'])}</td></tr>" for r in rows)
    return page("Rooms", f"""
    <h1>🚪 Rooms</h1>
    <form method="POST"><label>Room Number</label><input name="room" required>
    <label>Capacity</label><input name="capacity" required><button>Add Room</button></form>
    <h2>Room List</h2><table><tr><th>ID</th><th>Room</th><th>Capacity</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/doctors", methods=["GET", "POST"])
@login_required
@login_required
def doctors():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO doctors (name,specialization,hospital,contact) VALUES (?,?,?,?)",
                   tuple(request.form[x] for x in ("name","specialization","hospital","contact")))
        db.commit()
    rows = db.execute("SELECT * FROM doctors ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['specialization']}</td><td>{r['hospital']}</td><td>{r['contact']}</td><td>{action_buttons('doctors', r['id'])}</td></tr>" for r in rows)
    return page("Doctors", f"""
    <h1>👨‍⚕️ Doctors</h1>
    <form method="POST"><label>Name</label><input name="name" required>
    <label>Specialization</label><input name="specialization" required>
    <label>Hospital</label><input name="hospital" required>
    <label>Contact</label><input name="contact" required><button>Add Doctor</button></form>
    <h2>Doctor List</h2><table><tr><th>ID</th><th>Name</th><th>Specialization</th><th>Hospital</th><th>Contact</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/hospitals", methods=["GET", "POST"])
@login_required
@login_required
def hospitals():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO hospitals (name,address,contact) VALUES (?,?,?)",
                   (request.form["name"],request.form["address"],request.form["contact"]))
        db.commit()
    rows = db.execute("SELECT * FROM hospitals ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['address']}</td><td>{r['contact']}</td><td>{action_buttons('hospitals', r['id'])}</td></tr>" for r in rows)
    return page("Hospitals", f"""
    <h1>🏥 Hospitals</h1>
    <form method="POST"><label>Name</label><input name="name" required>
    <label>Address</label><input name="address" required>
    <label>Contact</label><input name="contact" required><button>Add Hospital</button></form>
    <h2>Hospital List</h2><table><tr><th>ID</th><th>Name</th><th>Address</th><th>Contact</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/medicines", methods=["GET", "POST"])
@login_required
@login_required
def medicines():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO medicines (resident,medicine,time,status,date_time) VALUES (?,?,?,?,?)",
                   (request.form["resident"],request.form["medicine"],request.form["time"],request.form["status"],datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    rows = db.execute("SELECT * FROM medicines ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['medicine']}</td><td>{r['time']}</td><td>{r['status']}</td><td>{r['date_time']}</td><td>{action_buttons('medicines', r['id'])}</td></tr>" for r in rows)
    return page("Medicines", f"""
    <h1>💊 Medicines</h1>
    <form method="POST"><label>Resident</label><input name="resident" required>
    <label>Medicine</label><input name="medicine" required><label>Time</label><input type="time" name="time" required>
    <label>Status</label><select name="status"><option>Pending</option><option>Given</option><option>Missed</option></select>
    <button>Add Medicine</button></form><h2>Medicine Records</h2>
    <table><tr><th>ID</th><th>Resident</th><th>Medicine</th><th>Time</th><th>Status</th><th>Date/Time</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/health", methods=["GET", "POST"])
@login_required
@login_required
def health():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO health
        (resident,temperature,bp,pulse,oxygen,weight,condition,doctor,date_time)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (request.form["resident"],request.form["temperature"],request.form["bp"],request.form["pulse"],
         request.form["oxygen"],request.form["weight"],request.form["condition"],request.form["doctor"],
         datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    rows = db.execute("SELECT * FROM health ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['temperature']}</td><td>{r['bp']}</td><td>{r['pulse']}</td><td>{r['oxygen']}</td><td>{r['weight']}</td><td>{r['condition']}</td><td>{r['doctor']}</td><td>{r['date_time']}</td><td>{action_buttons('health', r['id'])}</td></tr>" for r in rows)
    return page("Health", f"""
    <h1>❤️ Health Records</h1><form method="POST">
    <label>Resident</label><input name="resident" required><label>Temperature</label><input name="temperature" required>
    <label>Blood Pressure</label><input name="bp" required><label>Pulse</label><input name="pulse" required>
    <label>Oxygen</label><input name="oxygen" required><label>Weight</label><input name="weight" required>
    <label>Condition</label><input name="condition" required><label>Doctor</label><input name="doctor" required>
    <button>Save Health Record</button></form><h2>Health List</h2>
    <table><tr><th>ID</th><th>Resident</th><th>Temp</th><th>BP</th><th>Pulse</th><th>Oxygen</th><th>Weight</th><th>Condition</th><th>Doctor</th><th>Date/Time</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/visitors", methods=["GET", "POST"])
@login_required
@login_required
def visitors():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO visitors (visitor,resident,relation,contact,date,time,purpose)
        VALUES (?,?,?,?,?,?,?)""", tuple(request.form[x] for x in ("visitor","resident","relation","contact","date","time","purpose")))
        db.commit()
    rows = db.execute("SELECT * FROM visitors ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['visitor']}</td><td>{r['resident']}</td><td>{r['relation']}</td><td>{r['contact']}</td><td>{r['date']}</td><td>{r['time']}</td><td>{r['purpose']}</td><td>{action_buttons('visitors', r['id'])}</td></tr>" for r in rows)
    return page("Visitors", f"""
    <h1>👥 Visitors</h1><form method="POST">
    <label>Visitor Name</label><input name="visitor" required><label>Resident</label><input name="resident" required>
    <label>Relation</label><input name="relation" required><label>Contact</label><input name="contact" required>
    <label>Date</label><input type="date" name="date" required><label>Time</label><input type="time" name="time" required>
    <label>Purpose</label><input name="purpose" required><button>Add Visitor</button></form>
    <h2>Visitor List</h2><table><tr><th>ID</th><th>Visitor</th><th>Resident</th><th>Relation</th><th>Contact</th><th>Date</th><th>Time</th><th>Purpose</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/caretakers", methods=["GET", "POST"])
@login_required
@login_required
def caretakers():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO caretakers (name,contact,duty_time,duties) VALUES (?,?,?,?)",
                   tuple(request.form[x] for x in ("name","contact","duty_time","duties")))
        db.commit()
    rows = db.execute("SELECT * FROM caretakers ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['contact']}</td><td>{r['duty_time']}</td><td>{r['duties']}</td><td>{action_buttons('caretakers', r['id'])}</td></tr>" for r in rows)
    return page("Caretakers", f"""
    <h1>🧑‍⚕️ Caretakers</h1><form method="POST">
    <label>Name</label><input name="name" required><label>Contact</label><input name="contact" required>
    <label>Duty Time</label><input name="duty_time" required><label>Duties</label><textarea name="duties" required></textarea>
    <button>Add Caretaker</button></form><h2>Caretaker List</h2>
    <table><tr><th>ID</th><th>Name</th><th>Contact</th><th>Duty Time</th><th>Duties</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/meals", methods=["GET", "POST"])
@login_required
@login_required
def meals():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO meals (resident,breakfast,lunch,dinner,water,notes,date_time)
        VALUES (?,?,?,?,?,?,?)""", (request.form["resident"],request.form["breakfast"],request.form["lunch"],
        request.form["dinner"],request.form["water"],request.form["notes"],datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    rows = db.execute("SELECT * FROM meals ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['breakfast']}</td><td>{r['lunch']}</td><td>{r['dinner']}</td><td>{r['water']}</td><td>{r['notes']}</td><td>{r['date_time']}</td><td>{action_buttons('meals', r['id'])}</td></tr>" for r in rows)
    return page("Meals", f"""
    <h1>🍲 Meals</h1><form method="POST"><label>Resident</label><input name="resident" required>
    <label>Breakfast</label><input name="breakfast" required><label>Lunch</label><input name="lunch" required>
    <label>Dinner</label><input name="dinner" required><label>Water</label><input name="water" required>
    <label>Notes</label><textarea name="notes" required></textarea><button>Save Meal</button></form>
    <h2>Meal Records</h2><table><tr><th>ID</th><th>Resident</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th><th>Water</th><th>Notes</th><th>Date/Time</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/dailycare", methods=["GET", "POST"])
@login_required
@login_required
def dailycare():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO dailycare (resident,food,water,activity,condition,date_time)
        VALUES (?,?,?,?,?,?)""", (request.form["resident"],request.form["food"],request.form["water"],
        request.form["activity"],request.form["condition"],datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    rows = db.execute("SELECT * FROM dailycare ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['food']}</td><td>{r['water']}</td><td>{r['activity']}</td><td>{r['condition']}</td><td>{r['date_time']}</td><td>{action_buttons('dailycare', r['id'])}</td></tr>" for r in rows)
    return page("Daily Care", f"""
    <h1>📝 Daily Care</h1><form method="POST"><label>Resident</label><input name="resident" required>
    <label>Food</label><input name="food" required><label>Water</label><input name="water" required>
    <label>Activity</label><input name="activity" required><label>Condition</label><input name="condition" required>
    <button>Save Daily Care</button></form><h2>Daily Care Records</h2>
    <table><tr><th>ID</th><th>Resident</th><th>Food</th><th>Water</th><th>Activity</th><th>Condition</th><th>Date/Time</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/appointments", methods=["GET", "POST"])
@login_required
@login_required
def appointments():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO appointments
        (resident,doctor,hospital,date,time,reason,status) VALUES (?,?,?,?,?,?,?)""",
        tuple(request.form[x] for x in ("resident","doctor","hospital","date","time","reason","status")))
        db.commit()
    rows = db.execute("SELECT * FROM appointments ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['doctor']}</td><td>{r['hospital']}</td><td>{r['date']}</td><td>{r['time']}</td><td>{r['reason']}</td><td>{r['status']}</td><td>{action_buttons('appointments', r['id'])}</td></tr>" for r in rows)
    return page("Appointments", f"""
    <h1>📅 Appointments</h1><form method="POST"><label>Resident</label><input name="resident" required>
    <label>Doctor</label><input name="doctor" required><label>Hospital</label><input name="hospital" required>
    <label>Date</label><input type="date" name="date" required><label>Time</label><input type="time" name="time" required>
    <label>Reason</label><input name="reason" required><label>Status</label>
    <select name="status"><option>Scheduled</option><option>Completed</option><option>Cancelled</option></select>
    <button>Add Appointment</button></form><h2>Appointment List</h2>
    <table><tr><th>ID</th><th>Resident</th><th>Doctor</th><th>Hospital</th><th>Date</th><th>Time</th><th>Reason</th><th>Status</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/history")
@login_required
@login_required
def history():
    db = get_db()
    history_rows = []

    # Recent records from all important care modules
    queries = [
        ("Residents", "SELECT name AS item, 'Resident added' AS action, '' AS extra, id FROM residents ORDER BY id DESC LIMIT 20"),
        ("Medicines", "SELECT medicine AS item, 'Medicine record' AS action, resident AS extra, id FROM medicines ORDER BY id DESC LIMIT 20"),
        ("Health", "SELECT resident AS item, 'Health record' AS action, condition AS extra, id FROM health ORDER BY id DESC LIMIT 20"),
        ("Visitors", "SELECT visitor AS item, 'Visitor record' AS action, resident AS extra, id FROM visitors ORDER BY id DESC LIMIT 20"),
        ("Meals", "SELECT resident AS item, 'Meal record' AS action, notes AS extra, id FROM meals ORDER BY id DESC LIMIT 20"),
        ("Daily Care", "SELECT resident AS item, 'Daily care record' AS action, condition AS extra, id FROM dailycare ORDER BY id DESC LIMIT 20"),
        ("Appointments", "SELECT resident AS item, 'Appointment' AS action, doctor AS extra, id FROM appointments ORDER BY id DESC LIMIT 20"),
        ("Emergency", "SELECT resident AS item, 'Emergency' AS action, problem AS extra, id FROM emergencies ORDER BY id DESC LIMIT 20"),
    ]

    for module, query in queries:
        for row in db.execute(query).fetchall():
            history_rows.append((row["id"], module, row["action"], row["item"], row["extra"]))

    db.close()
    history_rows.sort(key=lambda x: x[0], reverse=True)

    table = "".join(
        f"<tr><td>{i}</td><td>{module}</td><td>{action}</td><td>{item}</td><td>{extra}</td></tr>"
        for i, (record_id, module, action, item, extra) in enumerate(history_rows[:100], 1)
    )

    if not table:
        table = '<tr><td colspan="5">No history records yet.</td></tr>'

    return page("History", f"""
    <h1>📜 Care History</h1>
    <p>Recent records from CareConnect.</p>
    <table>
        <tr><th>#</th><th>Module</th><th>Action</th><th>Resident / Item</th><th>Details</th></tr>
        {table}
    </table>
    <br>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/emergency", methods=["GET", "POST"])
@login_required
@login_required
def emergency():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO emergencies (resident,room,problem,date_time)
        VALUES (?,?,?,?)""", (request.form["resident"],request.form["room"],request.form["problem"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    rows = db.execute("SELECT * FROM emergencies ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['room']}</td><td>{r['problem']}</td><td>{r['date_time']}</td><td>{action_buttons('emergencies', r['id'])}</td></tr>" for r in rows)
    return page("Emergency", f"""
    <div class="emergency-page"><h1>🚨 Emergency</h1>
    <p class="warning">Use this page to record an emergency immediately.</p>
    <form method="POST"><label>Resident</label><input name="resident" required>
    <label>Room</label><input name="room" required><label>Problem</label><textarea name="problem" required></textarea>
    <button class="danger" type="submit">🚨 Record Emergency</button></form>
    <h2>Emergency Records</h2><table><tr><th>ID</th><th>Resident</th><th>Room</th><th>Problem</th><th>Date/Time</th><th>Actions</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a></div>
    """)



TABLE_FIELDS = {
    "residents": [("name","Name","text"),("age","Age","text"),("gender","Gender","text"),("room","Room","text"),("contact","Contact","text")],
    "rooms": [("room","Room Number","text"),("capacity","Capacity","text")],
    "doctors": [("name","Name","text"),("specialization","Specialization","text"),("hospital","Hospital","text"),("contact","Contact","text")],
    "hospitals": [("name","Name","text"),("address","Address","text"),("contact","Contact","text")],
    "medicines": [("resident","Resident","text"),("medicine","Medicine","text"),("time","Time","time"),("status","Status","select:Pending,Given,Missed"),("date_time","Date/Time","text")],
    "health": [("resident","Resident","text"),("temperature","Temperature","text"),("bp","Blood Pressure","text"),("pulse","Pulse","text"),("oxygen","Oxygen","text"),("weight","Weight","text"),("condition","Condition","text"),("doctor","Doctor","text"),("date_time","Date/Time","text")],
    "visitors": [("visitor","Visitor Name","text"),("resident","Resident","text"),("relation","Relation","text"),("contact","Contact","text"),("date","Date","date"),("time","Time","time"),("purpose","Purpose","text")],
    "caretakers": [("name","Name","text"),("contact","Contact","text"),("duty_time","Duty Time","text"),("duties","Duties","textarea")],
    "meals": [("resident","Resident","text"),("breakfast","Breakfast","text"),("lunch","Lunch","text"),("dinner","Dinner","text"),("water","Water","text"),("notes","Notes","textarea"),("date_time","Date/Time","text")],
    "dailycare": [("resident","Resident","text"),("food","Food","text"),("water","Water","text"),("activity","Activity","text"),("condition","Condition","text"),("date_time","Date/Time","text")],
    "appointments": [("resident","Resident","text"),("doctor","Doctor","text"),("hospital","Hospital","text"),("date","Date","date"),("time","Time","time"),("reason","Reason","text"),("status","Status","select:Scheduled,Completed,Cancelled")],
    "emergencies": [("resident","Resident","text"),("room","Room","text"),("problem","Problem","textarea"),("date_time","Date/Time","text")]
}
MODULE_PATH = {"emergencies":"emergency"}

@app.route("/edit/<table_name>/<int:record_id>", methods=["GET","POST"])
@login_required
def edit_record(table_name, record_id):
    if table_name not in TABLE_FIELDS:
        return "Invalid table", 400
    db = get_db()
    row = db.execute(f"SELECT * FROM {table_name} WHERE id=?", (record_id,)).fetchone()
    if row is None:
        db.close()
        return "Record not found", 404
    if request.method == "POST":
        fields = [x[0] for x in TABLE_FIELDS[table_name]]
        values = [request.form.get(f, "").strip() for f in fields]
        db.execute(f"UPDATE {table_name} SET {', '.join(f+'=?' for f in fields)} WHERE id=?", values + [record_id])
        db.commit()
        db.close()
        return redirect('/' + MODULE_PATH.get(table_name, table_name))
    form = ""
    for field, label, kind in TABLE_FIELDS[table_name]:
        value = e(row[field])
        if kind.startswith("select:"):
            opts = kind.split(":", 1)[1].split(",")
            control = '<select name="'+field+'">' + ''.join('<option '+('selected' if o == row[field] else '')+'>'+e(o)+'</option>' for o in opts) + '</select>'
        elif kind == "textarea":
            control = f'<textarea name="{field}" required>{value}</textarea>'
        else:
            control = f'<input type="{kind}" name="{field}" value="{value}" required>'
        form += f'<label>{e(label)}</label>{control}'
    db.close()
    return page("Edit Record", f'<div class="form-card"><h1>✏️ Edit {e(table_name.title())}</h1><form method="POST">{form}<button type="submit">💾 Update</button></form><a href="/{MODULE_PATH.get(table_name,table_name)}"><button type="button" class="secondary">Cancel</button></a></div>')

@app.route("/delete/<table_name>/<int:record_id>", methods=["POST"])
@login_required
def delete_record(table_name, record_id):
    if table_name not in TABLE_FIELDS:
        return "Invalid table", 400
    db = get_db()
    db.execute(f"DELETE FROM {table_name} WHERE id=?", (record_id,))
    db.commit()
    db.close()
    return redirect('/' + MODULE_PATH.get(table_name, table_name))

# Create all database tables when the app starts.
# This is important for both local use and online hosting.
create_database()


if __name__ == "__main__":
    app.run(debug=True)
