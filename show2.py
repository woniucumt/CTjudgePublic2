from flask import Flask
from flask import render_template
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from calculateCT import cal
from calculateCT2 import cal2
from os.path import dirname, abspath
from featureExtraction import mian
from flask import render_template
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from os.path import dirname, abspath
# 文件上传需要
ALLOWED_EXTENSIONS = {'txt','py'}
UPLOAD_FOLDER=dirname(abspath(__file__))+"/upload"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def hello_world():
    return render_template('personPage.html')
@app.route('/hello2/')
@app.route('/hello2/<name>')
def hello(name=None):
    return render_template('hello.html', name=[3, 2, 2, 3, 3])

# 文件上传
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/save', methods=['GET', 'POST'])
def upload_file():
    result2=[]
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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as archivo:
            #     print(archivo)

        print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        result2=cal2(filename)
            # return redirect(url_for('uploaded_file',
            #
        #                        filename=filename))
    # return render_template('uploadfile.html')
        return render_template('hello.html', name=result2)
    return render_template('uploadfile.html')


@app.route("/text", methods=("GET", "POST"))
def login():
    # GET请求
    if request.method == "GET":
        return render_template("text.html")
    # POST请求
    if request.method == "POST":

        print(request.headers)
        print(request.json)
        print(request.data)
        # 获取数据并转化成字典
        user_info = request.form.to_dict()
        if user_info.get("username") == "admin" and user_info.get("password") == '123456':
            return redirect("/")
    # print(request.form.to_dict())
    # args 获取地址栏的hash值
    print(request.args.to_dict())
    # print(user_info.get("text"))
    result=cal(user_info.get("text"))
    return render_template('hello.html', name=result)

@app.route('/save2', methods=['GET', 'POST'])
def upload_file2():
    result2=[]
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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as archivo:
            #     print(archivo)

        print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mian.start(filename)
            # return redirect(url_for('uploaded_file',
            #
        #                        filename=filename))
    # return render_template('uploadfile.html')
        return render_template('hello.html', name=result2)
    return render_template('uploadfileDeadibility.html')

@app.route('/JudgeChoose')
def JudgeChoose():
    return render_template('judgeChoose.html')



if __name__ == '__main__':
    app.run()
