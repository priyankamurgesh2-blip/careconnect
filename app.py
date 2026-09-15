
from flask import Flask, request, redirect, send_from_directory
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = "careconnect.db"


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


def page(title, body):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - CareConnect</title>
        <link rel="stylesheet" href="/style.css">
        <link rel="manifest" href="/manifest.json">
        <meta name="theme-color" content="#2563eb">
    </head>
    <body>{body}
        <script>
        if ("serviceWorker" in navigator) {{
            window.addEventListener("load", function () {{
                navigator.serviceWorker.register("/sw.js").catch(function (error) {{
                    console.log("Service worker registration failed:", error);
                }});
            }});
        }}
        </script>
    </body>
    </html>
    """


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "1234":
            return redirect("/dashboard")
        message = '<p class="error">Invalid username or password</p>'
    else:
        message = ""

    return page("Login", f"""
    <div class="login-box">
        <h1>🏠 CARECONNECT</h1>
        <h2>NEST CARE HOME</h2>
        <p>Smart Care Management</p>
        {message}
        <form method="POST">
            <label>Username</label>
            <input name="username" required>
            <label>Password</label>
            <input type="password" name="password" required>
            <button type="submit">Login</button>
        </form>
        <p><b>Demo login:</b> admin / 1234</p>
    </div>
    """)


@app.route("/dashboard")
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
def residents():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO residents (name,age,gender,room,contact) VALUES (?,?,?,?,?)",
                   tuple(request.form[x] for x in ("name","age","gender","room","contact")))
        db.commit()
    rows = db.execute("SELECT * FROM residents ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(
        f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['age']}</td><td>{r['gender']}</td><td>{r['room']}</td><td>{r['contact']}</td></tr>"
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
    <table><tr><th>ID</th><th>Name</th><th>Age</th><th>Gender</th><th>Room</th><th>Contact</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/rooms", methods=["GET", "POST"])
def rooms():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO rooms (room,capacity) VALUES (?,?)",
                   (request.form["room"], request.form["capacity"]))
        db.commit()
    rows = db.execute("SELECT * FROM rooms ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['room']}</td><td>{r['capacity']}</td></tr>" for r in rows)
    return page("Rooms", f"""
    <h1>🚪 Rooms</h1>
    <form method="POST"><label>Room Number</label><input name="room" required>
    <label>Capacity</label><input name="capacity" required><button>Add Room</button></form>
    <h2>Room List</h2><table><tr><th>ID</th><th>Room</th><th>Capacity</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/doctors", methods=["GET", "POST"])
def doctors():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO doctors (name,specialization,hospital,contact) VALUES (?,?,?,?)",
                   tuple(request.form[x] for x in ("name","specialization","hospital","contact")))
        db.commit()
    rows = db.execute("SELECT * FROM doctors ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['specialization']}</td><td>{r['hospital']}</td><td>{r['contact']}</td></tr>" for r in rows)
    return page("Doctors", f"""
    <h1>👨‍⚕️ Doctors</h1>
    <form method="POST"><label>Name</label><input name="name" required>
    <label>Specialization</label><input name="specialization" required>
    <label>Hospital</label><input name="hospital" required>
    <label>Contact</label><input name="contact" required><button>Add Doctor</button></form>
    <h2>Doctor List</h2><table><tr><th>ID</th><th>Name</th><th>Specialization</th><th>Hospital</th><th>Contact</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/hospitals", methods=["GET", "POST"])
def hospitals():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO hospitals (name,address,contact) VALUES (?,?,?)",
                   (request.form["name"],request.form["address"],request.form["contact"]))
        db.commit()
    rows = db.execute("SELECT * FROM hospitals ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['address']}</td><td>{r['contact']}</td></tr>" for r in rows)
    return page("Hospitals", f"""
    <h1>🏥 Hospitals</h1>
    <form method="POST"><label>Name</label><input name="name" required>
    <label>Address</label><input name="address" required>
    <label>Contact</label><input name="contact" required><button>Add Hospital</button></form>
    <h2>Hospital List</h2><table><tr><th>ID</th><th>Name</th><th>Address</th><th>Contact</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/medicines", methods=["GET", "POST"])
def medicines():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO medicines (resident,medicine,time,status,date_time) VALUES (?,?,?,?,?)",
                   (request.form["resident"],request.form["medicine"],request.form["time"],request.form["status"],datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    rows = db.execute("SELECT * FROM medicines ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['medicine']}</td><td>{r['time']}</td><td>{r['status']}</td><td>{r['date_time']}</td></tr>" for r in rows)
    return page("Medicines", f"""
    <h1>💊 Medicines</h1>
    <form method="POST"><label>Resident</label><input name="resident" required>
    <label>Medicine</label><input name="medicine" required><label>Time</label><input type="time" name="time" required>
    <label>Status</label><select name="status"><option>Pending</option><option>Given</option><option>Missed</option></select>
    <button>Add Medicine</button></form><h2>Medicine Records</h2>
    <table><tr><th>ID</th><th>Resident</th><th>Medicine</th><th>Time</th><th>Status</th><th>Date/Time</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/health", methods=["GET", "POST"])
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
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['temperature']}</td><td>{r['bp']}</td><td>{r['pulse']}</td><td>{r['oxygen']}</td><td>{r['weight']}</td><td>{r['condition']}</td><td>{r['doctor']}</td><td>{r['date_time']}</td></tr>" for r in rows)
    return page("Health", f"""
    <h1>❤️ Health Records</h1><form method="POST">
    <label>Resident</label><input name="resident" required><label>Temperature</label><input name="temperature" required>
    <label>Blood Pressure</label><input name="bp" required><label>Pulse</label><input name="pulse" required>
    <label>Oxygen</label><input name="oxygen" required><label>Weight</label><input name="weight" required>
    <label>Condition</label><input name="condition" required><label>Doctor</label><input name="doctor" required>
    <button>Save Health Record</button></form><h2>Health List</h2>
    <table><tr><th>ID</th><th>Resident</th><th>Temp</th><th>BP</th><th>Pulse</th><th>Oxygen</th><th>Weight</th><th>Condition</th><th>Doctor</th><th>Date/Time</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/visitors", methods=["GET", "POST"])
def visitors():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO visitors (visitor,resident,relation,contact,date,time,purpose)
        VALUES (?,?,?,?,?,?,?)""", tuple(request.form[x] for x in ("visitor","resident","relation","contact","date","time","purpose")))
        db.commit()
    rows = db.execute("SELECT * FROM visitors ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['visitor']}</td><td>{r['resident']}</td><td>{r['relation']}</td><td>{r['contact']}</td><td>{r['date']}</td><td>{r['time']}</td><td>{r['purpose']}</td></tr>" for r in rows)
    return page("Visitors", f"""
    <h1>👥 Visitors</h1><form method="POST">
    <label>Visitor Name</label><input name="visitor" required><label>Resident</label><input name="resident" required>
    <label>Relation</label><input name="relation" required><label>Contact</label><input name="contact" required>
    <label>Date</label><input type="date" name="date" required><label>Time</label><input type="time" name="time" required>
    <label>Purpose</label><input name="purpose" required><button>Add Visitor</button></form>
    <h2>Visitor List</h2><table><tr><th>ID</th><th>Visitor</th><th>Resident</th><th>Relation</th><th>Contact</th><th>Date</th><th>Time</th><th>Purpose</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/caretakers", methods=["GET", "POST"])
def caretakers():
    db = get_db()
    if request.method == "POST":
        db.execute("INSERT INTO caretakers (name,contact,duty_time,duties) VALUES (?,?,?,?)",
                   tuple(request.form[x] for x in ("name","contact","duty_time","duties")))
        db.commit()
    rows = db.execute("SELECT * FROM caretakers ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['contact']}</td><td>{r['duty_time']}</td><td>{r['duties']}</td></tr>" for r in rows)
    return page("Caretakers", f"""
    <h1>🧑‍⚕️ Caretakers</h1><form method="POST">
    <label>Name</label><input name="name" required><label>Contact</label><input name="contact" required>
    <label>Duty Time</label><input name="duty_time" required><label>Duties</label><textarea name="duties" required></textarea>
    <button>Add Caretaker</button></form><h2>Caretaker List</h2>
    <table><tr><th>ID</th><th>Name</th><th>Contact</th><th>Duty Time</th><th>Duties</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/meals", methods=["GET", "POST"])
def meals():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO meals (resident,breakfast,lunch,dinner,water,notes,date_time)
        VALUES (?,?,?,?,?,?,?)""", (request.form["resident"],request.form["breakfast"],request.form["lunch"],
        request.form["dinner"],request.form["water"],request.form["notes"],datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    rows = db.execute("SELECT * FROM meals ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['breakfast']}</td><td>{r['lunch']}</td><td>{r['dinner']}</td><td>{r['water']}</td><td>{r['notes']}</td><td>{r['date_time']}</td></tr>" for r in rows)
    return page("Meals", f"""
    <h1>🍲 Meals</h1><form method="POST"><label>Resident</label><input name="resident" required>
    <label>Breakfast</label><input name="breakfast" required><label>Lunch</label><input name="lunch" required>
    <label>Dinner</label><input name="dinner" required><label>Water</label><input name="water" required>
    <label>Notes</label><textarea name="notes" required></textarea><button>Save Meal</button></form>
    <h2>Meal Records</h2><table><tr><th>ID</th><th>Resident</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th><th>Water</th><th>Notes</th><th>Date/Time</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/dailycare", methods=["GET", "POST"])
def dailycare():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO dailycare (resident,food,water,activity,condition,date_time)
        VALUES (?,?,?,?,?,?)""", (request.form["resident"],request.form["food"],request.form["water"],
        request.form["activity"],request.form["condition"],datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    rows = db.execute("SELECT * FROM dailycare ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['food']}</td><td>{r['water']}</td><td>{r['activity']}</td><td>{r['condition']}</td><td>{r['date_time']}</td></tr>" for r in rows)
    return page("Daily Care", f"""
    <h1>📝 Daily Care</h1><form method="POST"><label>Resident</label><input name="resident" required>
    <label>Food</label><input name="food" required><label>Water</label><input name="water" required>
    <label>Activity</label><input name="activity" required><label>Condition</label><input name="condition" required>
    <button>Save Daily Care</button></form><h2>Daily Care Records</h2>
    <table><tr><th>ID</th><th>Resident</th><th>Food</th><th>Water</th><th>Activity</th><th>Condition</th><th>Date/Time</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO appointments
        (resident,doctor,hospital,date,time,reason,status) VALUES (?,?,?,?,?,?,?)""",
        tuple(request.form[x] for x in ("resident","doctor","hospital","date","time","reason","status")))
        db.commit()
    rows = db.execute("SELECT * FROM appointments ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['doctor']}</td><td>{r['hospital']}</td><td>{r['date']}</td><td>{r['time']}</td><td>{r['reason']}</td><td>{r['status']}</td></tr>" for r in rows)
    return page("Appointments", f"""
    <h1>📅 Appointments</h1><form method="POST"><label>Resident</label><input name="resident" required>
    <label>Doctor</label><input name="doctor" required><label>Hospital</label><input name="hospital" required>
    <label>Date</label><input type="date" name="date" required><label>Time</label><input type="time" name="time" required>
    <label>Reason</label><input name="reason" required><label>Status</label>
    <select name="status"><option>Scheduled</option><option>Completed</option><option>Cancelled</option></select>
    <button>Add Appointment</button></form><h2>Appointment List</h2>
    <table><tr><th>ID</th><th>Resident</th><th>Doctor</th><th>Hospital</th><th>Date</th><th>Time</th><th>Reason</th><th>Status</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a>
    """)


@app.route("/history")
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
def emergency():
    db = get_db()
    if request.method == "POST":
        db.execute("""INSERT INTO emergencies (resident,room,problem,date_time)
        VALUES (?,?,?,?)""", (request.form["resident"],request.form["room"],request.form["problem"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    rows = db.execute("SELECT * FROM emergencies ORDER BY id DESC").fetchall()
    db.close()
    table = "".join(f"<tr><td>{r['id']}</td><td>{r['resident']}</td><td>{r['room']}</td><td>{r['problem']}</td><td>{r['date_time']}</td></tr>" for r in rows)
    return page("Emergency", f"""
    <div class="emergency-page"><h1>🚨 Emergency</h1>
    <p class="warning">Use this page to record an emergency immediately.</p>
    <form method="POST"><label>Resident</label><input name="resident" required>
    <label>Room</label><input name="room" required><label>Problem</label><textarea name="problem" required></textarea>
    <button class="danger" type="submit">🚨 Record Emergency</button></form>
    <h2>Emergency Records</h2><table><tr><th>ID</th><th>Resident</th><th>Room</th><th>Problem</th><th>Date/Time</th></tr>{table}</table>
    <a href="/dashboard"><button>⬅ Dashboard</button></a></div>
    """)


# Create all database tables when the app starts.
# This is important for both local use and online hosting.
create_database()


if __name__ == "__main__":
    app.run(debug=True)
