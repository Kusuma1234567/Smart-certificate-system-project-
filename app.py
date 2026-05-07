<<<<<<< HEAD
from flask import Flask, request, render_template, redirect, session
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        message TEXT,
        priority TEXT,
        status TEXT,
        reply TEXT
    )
    ''')

    conn.commit()
    conn.close()

# ---------------- PRIORITY ----------------
def get_priority(text):
    text = text.lower()

    if any(word in text for word in ["urgent", "emergency", "today", "asap"]):
        return "High (1-2 days)"
    elif any(word in text for word in ["week", "delay", "soon"]):
        return "Medium (1-4 weeks)"
    else:
        return "Low (1-3 months)"

# ---------------- EMAIL ----------------
def send_email(to_email, reply_msg):
    sender = "yourgmail@gmail.com"      
    password = "your_app_password"    

    msg = MIMEText(reply_msg)
    msg['Subject'] = "Certificate Request Update"
    msg['From'] = sender
    msg['To'] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Email error:", e)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------- SUBMIT ----------------
@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    message = request.form['message']
    priority = get_priority(message)

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO requests (email, message, priority, status, reply) VALUES (?, ?, ?, ?, ?)",
        (email, message, priority, "Pending", "")
    )

    conn.commit()
    conn.close()

    return render_template("result.html", priority=priority)

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == "admin":
            session['admin'] = True
            return redirect('/admin')
        else:
            return "Invalid Login"

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/login')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # All requests
    cursor.execute("SELECT * FROM requests")
    data = cursor.fetchall()

    # Dashboard counts
    cursor.execute("SELECT COUNT(*) FROM requests")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM requests WHERE priority LIKE 'High%'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM requests WHERE status='Resolved'")
    resolved = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        data=data,
        total=total,
        high=high,
        resolved=resolved
    )

# ---------------- REPLY ----------------
@app.route('/reply/<int:id>', methods=['POST'])
def reply(id):
    reply_msg = request.form['reply']

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Get user email
    cursor.execute("SELECT email FROM requests WHERE id=?", (id,))
    email = cursor.fetchone()[0]

    # Update reply and status
    cursor.execute(
        "UPDATE requests SET reply=?, status='Resolved' WHERE id=?",
        (reply_msg, id)
    )

    conn.commit()
    conn.close()

    # Send email
    send_email(
        email,
        f"""
Hello,

Your certificate request has been processed.

Status: Approved ✅
Message from Admin:
{reply_msg}

Thank you.
"""
    )

    return redirect('/admin')

# ---------------- TRACK ----------------
@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        email = request.form['email']

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM requests WHERE email=?", (email,))
        data = cursor.fetchall()

        conn.close()

        return render_template("track.html", data=data)

    return render_template("track.html", data=None)

# ---------------- RUN ----------------
init_db()
if __name__ == "__main__":
=======
from flask import Flask, request, render_template, redirect, session
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        message TEXT,
        priority TEXT,
        status TEXT,
        reply TEXT
    )
    ''')

    conn.commit()
    conn.close()

# ---------------- PRIORITY ----------------
def get_priority(text):
    text = text.lower()

    if any(word in text for word in ["urgent", "emergency", "today", "asap"]):
        return "High (1-2 days)"
    elif any(word in text for word in ["week", "delay", "soon"]):
        return "Medium (1-4 weeks)"
    else:
        return "Low (1-3 months)"

# ---------------- EMAIL ----------------
def send_email(to_email, reply_msg):
    sender = "yourgmail@gmail.com"      
    password = "your_app_password"    

    msg = MIMEText(reply_msg)
    msg['Subject'] = "Certificate Request Update"
    msg['From'] = sender
    msg['To'] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Email error:", e)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------- SUBMIT ----------------
@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    message = request.form['message']
    priority = get_priority(message)

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO requests (email, message, priority, status, reply) VALUES (?, ?, ?, ?, ?)",
        (email, message, priority, "Pending", "")
    )

    conn.commit()
    conn.close()

    return render_template("result.html", priority=priority)

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == "admin":
            session['admin'] = True
            return redirect('/admin')
        else:
            return "Invalid Login"

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/login')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # All requests
    cursor.execute("SELECT * FROM requests")
    data = cursor.fetchall()

    # Dashboard counts
    cursor.execute("SELECT COUNT(*) FROM requests")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM requests WHERE priority LIKE 'High%'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM requests WHERE status='Resolved'")
    resolved = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        data=data,
        total=total,
        high=high,
        resolved=resolved
    )

# ---------------- REPLY ----------------
@app.route('/reply/<int:id>', methods=['POST'])
def reply(id):
    reply_msg = request.form['reply']

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Get user email
    cursor.execute("SELECT email FROM requests WHERE id=?", (id,))
    email = cursor.fetchone()[0]

    # Update reply and status
    cursor.execute(
        "UPDATE requests SET reply=?, status='Resolved' WHERE id=?",
        (reply_msg, id)
    )

    conn.commit()
    conn.close()

    # Send email
    send_email(
        email,
        f"""
Hello,

Your certificate request has been processed.

Status: Approved ✅
Message from Admin:
{reply_msg}

Thank you.
"""
    )

    return redirect('/admin')

# ---------------- TRACK ----------------
@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        email = request.form['email']

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM requests WHERE email=?", (email,))
        data = cursor.fetchall()

        conn.close()

        return render_template("track.html", data=data)

    return render_template("track.html", data=None)

# ---------------- RUN ----------------
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
