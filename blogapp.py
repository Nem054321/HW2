from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os.path

UPLOAD_FOLDER = '/templates'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    if len(session) == 0:
        return render_template("login.html")
    else:
        return redirect(url_for("homepage"))

postlist = []

@app.route("/homepage_action",methods = ["POST","GET"])
def homepage_action():
    if request.method == "POST" and len(request.form["inputtext"])>0:
        now = datetime.now()
        inputtext = request.form["inputtext"]
        postlist.append([str(now.strftime("%m/%d/%Y %H:%M:%S:%f")),inputtext])
    return homepage(postlist)

@app.route("/homepage")
def homepage(*append):
    webpage = '''
    <html>
    <head>
    <title>Home</title>
    </head>
    <body>
    <p style='text-align:left;'>
    <h1>Welcome to the TECH 136 blog by LAM
    <span style='float:right;'>
    Username:
    ''' + session["username"] + " <a href='" + url_for("logout") + "'>Logout</a></h1></span></p>"

    webpage += '''
    <form action = 'homepage_action' method = 'post'>
    Enter your comment here:
    <br>
    <textarea id='inputtext' name='inputtext' rows='2' cols='100'></textarea>
    <br>
    <input type = 'submit' value = 'Submit' /> <a href=''' + "/upload" + '''>OR Upload image</a>
    <br>
    <br>
    '''   
    if len(append)> 0:
        for i in range (0, len(append[0])):
            webpage = webpage + '''
            <br>
            ''' + str(append[0][i][0]) + '''
            <br>
            <textarea id='inputtext' name='inputtext''' + str(i) + ''' rows='2' cols='100'>''' + str(append[0][i][1]) + '''</textarea>
            <br>
            '''
    return webpage

@app.route("/login_action",methods = ["POST","GET"])
def login_action():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Dummy user validation
        if username == "guest" and password == "password":
            session["username"] = username
            if len(postlist) > 0:
                return homepage(postlist)
            return redirect(url_for("homepage"))
    return render_template("login.html")

@app.route("/upload_action",methods = ["POST","GET"])
def upload_action():
    if request.method == "POST":
        now = datetime.now()
        postlist.append([str(now.strftime("%m/%d/%Y %H:%M:%S:%f")),"File uploaded successfully"])
    return homepage(postlist)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('upload', filename=file.filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data form action = 'upload_action'>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("login.html")

# main driver function
if __name__ == "__main__":

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="0.0.0.0",port=5002)



