from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ganesh@#1234",
    database="task_management"
)
cursor = db.cursor(dictionary=True)

# Routes and functions
@app.route('/')
def index():
    if 'user_id' in session:
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (session['user_id'],))
        tasks = cursor.fetchall()
        return render_template('index.html', tasks=tasks)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            error = 'Username or email already exists'
        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            db.commit()
            return redirect(url_for('login'))

    return render_template('register.html', error=error)

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' in session:
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        user_id = session['user_id']
        cursor.execute("INSERT INTO tasks (user_id, title, description, due_date) VALUES (%s, %s, %s, %s)", (user_id, title, description, due_date))
        db.commit()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)