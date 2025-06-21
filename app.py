from flask import Flask, render_template, request, redirect, session
from models import db, User, Leave
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect('/dashboard')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    leaves = Leave.query.filter_by(user_id=user.id).all() if not user.is_admin else Leave.query.all()
    return render_template('dashboard.html', user=user, leaves=leaves)

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        leave = Leave(
            user_id=session['user_id'],
            leave_type=request.form['leave_type'],
            from_date=request.form['from_date'],
            to_date=request.form['to_date'],
            reason=request.form['reason'],
            status='Pending'
        )
        db.session.add(leave)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('apply_leave.html')

@app.route('/approve/<int:leave_id>')
def approve(leave_id):
    if not session.get('is_admin'):
        return "Unauthorized"
    leave = Leave.query.get(leave_id)
    leave.status = 'Approved'
    db.session.commit()
    return redirect('/dashboard')

@app.route('/reject/<int:leave_id>')
def reject(leave_id):
    if not session.get('is_admin'):
        return "Unauthorized"
    leave = Leave.query.get(leave_id)
    leave.status = 'Rejected'
    db.session.commit()
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)