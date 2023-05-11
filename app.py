from flask import Flask, render_template, request, redirect, url_for, session
import db

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Assurez-vous de remplacer 'your-secret-key' par une clé secrète réelle

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db.add_comment(request.form['comment'])

    search_query = request.args.get('q')

    comments = db.get_comments(search_query)

    return render_template('index.html', comments=comments, search_query=search_query, username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = db.get_users()

        for user in users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                session['isadmin'] = user[2]
                return redirect(url_for('index'))

        return 'Invalid credentials, please try again.'

    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'username' not in session or 'isadmin' not in session or not session['isadmin']:
        return redirect(url_for('login'))
    return render_template('admin.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
