from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

registered_users = set()
submitted_reports = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        # Check if username is already registered
        if username in registered_users:
            return render_template('register.html', message='Account already registered. Please try to login.')
        registered_users.add(username)
        return render_template('register.html', message='Successfully registered!')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_type = request.form.get('login_type')
        username = request.form.get('username')
        password = request.form.get('password')
        # Only allow these two admin accounts
        allowed_admins = {
            'sharukeshwaranvthf@gmail.com': 'Sharu@kamal786',
            'shruthilayab3@gmail.com': 'Laya@206'
        }
        if login_type == 'admin':
            if username in allowed_admins and password == allowed_admins[username]:
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('login.html', message='Access denied: Only authorized admin emails can login.')
        return redirect(url_for('report'))
    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html', reports=submitted_reports)

@app.route('/admin_records')
def admin_records():
    return render_template('admin_records.html', reports=submitted_reports)

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        report_type = request.form.get('report_type')
        description = request.form.get('report')
        files = request.files.getlist('evidence')
        filenames = [f.filename for f in files if f and f.filename]
        submitted_reports.append({
            'type': report_type,
            'description': description,
            'files': filenames
        })
        return render_template('report.html', message='Report submitted successfully!')
    return render_template('report.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)