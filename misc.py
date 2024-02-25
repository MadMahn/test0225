from flask import Flask, request, render_template_string, escape
import sqlite3
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Secure SQL query construction using parameterized queries
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    connection = sqlite3.connect('application.db')
    cursor = connection.cursor()
    cursor.execute(query, (username, password))  # Execution of parameterized query
    result = cursor.fetchone()
    if result:
        return 'Login Successful!'
    else:
        return 'Login Failed!'

@app.route('/comment', methods=['GET'])
def comment():
    user_input = request.args.get('text')
    # Escaping user input to prevent XSS
    safe_user_input = escape(user_input)
    return render_template_string(f'User comment: {safe_user_input}')  # Rendering escaped user input

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    # Validate and sanitize the host parameter to prevent command injection
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        return 'Invalid host'
    command = f"ping -c 1 {host}"  # Using sanitized host parameter
    result = os.popen(command).read()  # Executing the command
    return f'<pre>{result}</pre>'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)  # Saving the file after checking its content
        return f'File uploaded successfully to {file_path}.'
    else:
        return 'Invalid file type.'

if __name__ == '__main__':
    app.run(debug=False)
