from flask import Flask,request,jsonify
import base64
app = Flask(__name__)

users = {
  "admin":"admin123",
  "root":"1234",
}

@app.route("/")
@app.route("/index")
def index():
  return "index is ok!"

@app.route('/auth',methods=['GET'])
def auth():
  auth = request.headers.get('Authorization')
  if not auth:
    return 'Unauthorized',401
  try:
    auth_type,credentials = auth.split(None,1)
    #username,password = credentials.strip().decode('base64').split(':',1)
    username, password = base64.b64decode(credentials.strip()).decode('utf-8').split(':', 1)
  except Exception as e:
    return 'Unauthorized',401
  
  if username in users and users[username] == password:
    return 'OK',200
  else:
      return 'Unauthorized',401

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8001,debug=True)