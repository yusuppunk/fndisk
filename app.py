from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import base64

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

users = {
    "adm": "admin123",
    "root": "1234",
}

@app.route("/")
@app.route("/index")
def index():
    if 'username' in session:
        return "Hello, " + session['username'] + "!"
    return redirect(url_for('login_page'))

@app.route('/auth', methods=['GET'])
def auth():
    auth = request.headers.get('Authorization')
    if not auth:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        auth_type, credentials = auth.split(None, 1)
        decoded_credentials = base64.b64decode(credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
    except Exception as e:
        return jsonify({"error": "Unauthorized"}), 401
    
    if username in users and users[username] == password:
        session['username'] = username
        return jsonify({"message": "OK"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Incorrect username or password.")
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
