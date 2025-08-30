from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (username TEXT PRIMARY KEY, password TEXT)''')
        conn.commit()

def get_user_from_db(username):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
    return user

def add_user_to_db(username, password):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_from_db(username)
        if user:
            message = 'Username already exists!'
        else:
            add_user_to_db(username, password)
            return redirect(url_for('login'))
    return render_template('signup.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_from_db(username)
        if user and user[1] == password:
            session['username'] = username
            return redirect(url_for('degree_selection'))
        else:
            message = 'Invalid credentials!'
    return render_template('login.html', message=message)

@app.route('/degree-selection', methods=['GET', 'POST'])
def degree_selection():
    if request.method == 'POST':
        degree_type = request.form['degree_type']
        department = request.form['department']
        
        session['degree_type'] = degree_type
        session['department'] = department
        
        return redirect(url_for('marks_input'))
    
    return render_template('degree_selection.html')

@app.route('/marks-input', methods=['GET', 'POST'])
def marks_input():
    if request.method == 'POST':
        degree_type = session.get('degree_type')
        district = request.form['district']
        community = request.form['community']
        session['district'] = district
        session['community'] = community


        
        if degree_type == 'UG':
            physics = float(request.form['physics'])
            chemistry = float(request.form['chemistry'])
            maths = float(request.form['maths'])
            
            cutoff = (physics / 2) + (chemistry / 2) + maths
            session['cutoff'] = cutoff
            
        elif degree_type == 'PG':
            cgpa = float(request.form['cgpa'])
            cutoff = cgpa * 10
            session['cutoff'] = cutoff

        return redirect(url_for('eligible_colleges'))

    degree_type = session.get('degree_type')
    if degree_type == 'UG':
        return render_template('marks_input_ug.html')
    elif degree_type == 'PG':
        return render_template('marks_input_pg.html')
    else:
        return redirect(url_for('degree_selection'))

@app.route('/eligible-colleges')
def eligible_colleges():
    cutoff = session.get('cutoff')
    department = session.get('department')
    district = session.get('district')
    degree_type = session.get('degree_type')
    community = session.get('community')

    #  Apply community-based relaxation
    if community == 'SC' or community == 'ST':
        cutoff += 5
    elif community == 'MBC':
        cutoff += 3
    elif community == 'BC':
        cutoff += 2

    # College list updated for UG and PG separately
    colleges = [
   

    # Coimbatore - UG
    {'name': 'PSG Tech', 'department': 'CSE', 'cutoff': 190, 'district': 'Coimbatore', 'degree': 'UG', 'website': 'https://www.psgtech.edu/'},
    {'name': 'Kumaraguru College', 'department': 'CSE', 'cutoff': 180, 'district': 'Coimbatore', 'degree': 'UG', 'website': 'https://www.kct.ac.in/'},

    {'name': 'Sri Krishna College', 'department': 'IT', 'cutoff': 170, 'district': 'Coimbatore', 'degree': 'UG'},
    {'name': 'Hindusthan College', 'department': 'EEE', 'cutoff': 160, 'district': 'Coimbatore', 'degree': 'UG'},
    {'name': 'Karpagam College', 'department': 'CSE', 'cutoff': 150, 'district': 'Coimbatore', 'degree': 'UG'},
    {'name': 'SNS College of Technology', 'department': 'CSE', 'cutoff': 155, 'district': 'Coimbatore', 'degree': 'UG'},
    {'name': 'Sri Ramakrishna Engineering College', 'department': 'IT', 'cutoff': 165, 'district': 'Coimbatore', 'degree': 'UG'},
    {'name': 'Dr. N.G.P Institute of Technology', 'department': 'EEE', 'cutoff': 158, 'district': 'Coimbatore', 'degree': 'UG'},
    {'name': 'P.A. College of Engineering and Technology', 'department': 'CSE', 'cutoff': 140, 'district': 'Coimbatore', 'degree': 'UG'},

    # Coimbatore - PG
    {'name': 'PSG Tech', 'department': 'CSE', 'cutoff': 75, 'district': 'Coimbatore', 'degree': 'PG'},
    {'name': 'Kumaraguru College', 'department': 'CSE', 'cutoff': 70, 'district': 'Coimbatore', 'degree': 'PG'},
    {'name': 'Sri Krishna College', 'department': 'IT', 'cutoff': 68, 'district': 'Coimbatore', 'degree': 'PG'},
    {'name': 'Hindusthan College', 'department': 'EEE', 'cutoff': 65, 'district': 'Coimbatore', 'degree': 'PG'},
    {'name': 'Karpagam College', 'department': 'CSE', 'cutoff': 60, 'district': 'Coimbatore', 'degree': 'PG'},
    {'name': 'SNS College of Technology', 'department': 'CSE', 'cutoff': 62, 'district': 'Coimbatore', 'degree': 'PG'},
    {'name': 'Sri Ramakrishna Engineering College', 'department': 'IT', 'cutoff': 67, 'district': 'Coimbatore', 'degree': 'PG'},
    {'name': 'Dr. N.G.P Institute of Technology', 'department': 'EEE', 'cutoff': 64, 'district': 'Coimbatore', 'degree': 'PG'},
    {'name': 'P.A. College of Engineering and Technology', 'department': 'CSE', 'cutoff': 58, 'district': 'Coimbatore', 'degree': 'PG'},

    # Chennai - UG
    {'name': 'College of Engineering, Guindy', 'department': 'CSE', 'cutoff': 190, 'district': 'Chennai', 'degree': 'UG'},
    {'name': 'Anna University', 'department': 'CSE', 'cutoff': 195, 'district': 'Chennai', 'degree': 'UG'},
    {'name': 'SSN College of Engineering', 'department': 'IT', 'cutoff': 185, 'district': 'Chennai', 'degree': 'UG'},
    {'name': 'MIT Campus', 'department': 'EEE', 'cutoff': 180, 'district': 'Chennai', 'degree': 'UG'},
    {'name': 'SRM Institute of Science and Technology', 'department': 'CSE', 'cutoff': 170, 'district': 'Chennai', 'degree': 'UG'},
    {'name': 'Saveetha Engineering College', 'department': 'CSE', 'cutoff': 165, 'district': 'Chennai', 'degree': 'UG'},
    {'name': 'VIT Chennai', 'department': 'IT', 'cutoff': 175, 'district': 'Chennai', 'degree': 'UG'},

    # Chennai - PG
    {'name': 'College of Engineering, Guindy', 'department': 'CSE', 'cutoff': 78, 'district': 'Chennai', 'degree': 'PG'},
    {'name': 'Anna University', 'department': 'CSE', 'cutoff': 80, 'district': 'Chennai', 'degree': 'PG'},
    {'name': 'SSN College of Engineering', 'department': 'IT', 'cutoff': 76, 'district': 'Chennai', 'degree': 'PG'},
    {'name': 'MIT Campus', 'department': 'EEE', 'cutoff': 75, 'district': 'Chennai', 'degree': 'PG'},
    {'name': 'SRM Institute of Science and Technology', 'department': 'CSE', 'cutoff': 70, 'district': 'Chennai', 'degree': 'PG'},
    {'name': 'Saveetha Engineering College', 'department': 'CSE', 'cutoff': 68, 'district': 'Chennai', 'degree': 'PG'},
    {'name': 'VIT Chennai', 'department': 'IT', 'cutoff': 74, 'district': 'Chennai', 'degree': 'PG'},

    # Trichy - UG
    {'name': 'NIT Trichy', 'department': 'CSE', 'cutoff': 195, 'district': 'Trichy', 'degree': 'UG'},
    {'name': 'Saranathan College of Engineering', 'department': 'IT', 'cutoff': 170, 'district': 'Trichy', 'degree': 'UG'},
    {'name': 'M.A.M College of Engineering', 'department': 'EEE', 'cutoff': 160, 'district': 'Trichy', 'degree': 'UG'},
    {'name': 'Oxford Engineering College', 'department': 'CSE', 'cutoff': 150, 'district': 'Trichy', 'degree': 'UG'},
    {'name': 'Jayaram College of Engineering', 'department': 'CSE', 'cutoff': 140, 'district': 'Trichy', 'degree': 'UG'},

    # Trichy - PG
    {'name': 'NIT Trichy', 'department': 'CSE', 'cutoff': 80, 'district': 'Trichy', 'degree': 'PG'},
    {'name': 'Saranathan College of Engineering', 'department': 'IT', 'cutoff': 70, 'district': 'Trichy', 'degree': 'PG'},
    {'name': 'M.A.M College of Engineering', 'department': 'EEE', 'cutoff': 65, 'district': 'Trichy', 'degree': 'PG'},
    {'name': 'Oxford Engineering College', 'department': 'CSE', 'cutoff': 60, 'district': 'Trichy', 'degree': 'PG'},
    {'name': 'Jayaram College of Engineering', 'department': 'CSE', 'cutoff': 58, 'district': 'Trichy', 'degree': 'PG'},

    # Madurai - UG
    {'name': 'Thiagarajar College of Engineering', 'department': 'CSE', 'cutoff': 180, 'district': 'Madurai', 'degree': 'UG'},
    {'name': 'Madurai Institute of Engineering and Technology', 'department': 'IT', 'cutoff': 160, 'district': 'Madurai', 'degree': 'UG'},
    {'name': 'Velammal College of Engineering', 'department': 'EEE', 'cutoff': 165, 'district': 'Madurai', 'degree': 'UG'},
    {'name': 'K.L.N. College of Engineering', 'department': 'CSE', 'cutoff': 150, 'district': 'Madurai', 'degree': 'UG'},
    {'name': 'Raja College of Engineering and Technology', 'department': 'CSE', 'cutoff': 140, 'district': 'Madurai', 'degree': 'UG'},

    # Madurai - PG
    {'name': 'Thiagarajar College of Engineering', 'department': 'CSE', 'cutoff': 77, 'district': 'Madurai', 'degree': 'PG'},
    {'name': 'Velammal College of Engineering', 'department': 'EEE', 'cutoff': 70, 'district': 'Madurai', 'degree': 'PG'},
    {'name': 'K.L.N. College of Engineering', 'department': 'CSE', 'cutoff': 68, 'district': 'Madurai', 'degree': 'PG'},
    {'name': 'Raja College of Engineering and Technology', 'department': 'CSE', 'cutoff': 60, 'district': 'Madurai', 'degree': 'PG'},


    ]

    # Filter based on degree type
    eligible_colleges = [
        college for college in colleges
        if college['department'] == department and
           college['district'] == district and
           college['degree'] == degree_type and
           college['cutoff'] <= cutoff
    ]

    return render_template('eligible_colleges.html', colleges=eligible_colleges, cutoff=cutoff)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('degree_type', None)
    session.pop('department', None)
    session.pop('cutoff', None)
    session.pop('district', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
