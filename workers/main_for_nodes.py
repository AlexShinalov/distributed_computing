import requests
from flask import send_from_directory

from flask import Flask, request, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("upload.html")

@app.route('/upload/1/<filename>')
def uploaded_file(filename):

    filename = 'done.jpg'
    return send_from_directory('upload', filename)

@app.route('/upload/2/<filename>')
def uploaded_file_2(filename):
    filename1="done2.jpg"
    return send_from_directory('upload', filename1)

@app.route('/upload/3/<filename>')
def uploaded_file_3(filename):
    return send_from_directory('upload', 'done3.jpg')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

