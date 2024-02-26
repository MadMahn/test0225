from flask import Flask, request, render_template_string, escape
import sqlite3
import os
import shlex

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    connection = sqlite3.connect('application.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    if result:
        return 'Login Successful!'
    else:
        return 'Login Failed!'

@app.route('/comment', methods=['GET'])
def comment():
    user_input = request.args.get('text')
    safe_user_input = escape(user_input)
    return render_template_string(f'User comment: {safe_user_input}')

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    safe_host = shlex.quote(host)
    command = f"ping -c 1 {safe_host}"
    result = os.popen(command).read()
    return f'<pre>{escape(result)}</pre>'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join('uploads', filename)
    file.save(file_path)
    safe_file_path = escape(file_path)
    return f'File uploaded successfully to {safe_file_path}.'

if __name__ == '__main__':
    app.run(debug=False)
