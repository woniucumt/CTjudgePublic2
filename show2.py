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
from readabilityJudge import reababilityJudge
import xgboost as xgb
from xgboost import XGBClassifier
# 文件上传需要
ALLOWED_EXTENSIONS = {'txt','py'}
UPLOAD_FOLDER=dirname(abspath(__file__))+"/upload"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "hskghsaklg"

# root is homepage.
@app.route('/')
def hello_world():
    return render_template('homepageAdaptative.html')

@app.route('/personPage')
def personPage():
    return render_template('personPage.html')
@app.route('/hello2/')
@app.route('/hello2/<name>')
def hello(name=None):
    return render_template('ctResult.html', name=[3, 2, 2, 3, 3])

# 文件上传
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ctjudge', methods=['GET', 'POST'])
def upload_file():
    result2=[]
    filename="sample.py"
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('uploadfileCT.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('uploadfileCT.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as archivo:
            #     print(archivo)
        else:
            print("not a python file!")
            return render_template('uploadfileCT.html')


        print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        result2=cal2(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #
        #                        filename=filename))
    # return render_template('uploadfile.html')
    #     删除已上传的文件，不然服务器东西太多了。
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('ctResult.html', name=result2)
    return render_template('uploadfileCT.html')


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
    return render_template('ctResult.html', name=result)

@app.route('/readjudge', methods=['GET', 'POST'])
def upload_file2():
    result2=[]
    resultAttr=[]
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
        resultAttr=mian.start(filename)
        print("safdasfsad")
        print (resultAttr)
        print("zai show2limian")
        print(reababilityJudge.readabilityJudgeFunc(resultAttr))

            # return redirect(url_for('uploaded_file',
            #
        #                        filename=filename))
    # return render_template('uploadfile.html')
        return render_template('readabilityResult.html', name=result2)
    return render_template('uploadfileDeadibility.html')

@app.route('/JudgeChoose')
def JudgeChoose():
    return render_template('judgeChoose.html')
@app.route('/homepage')
def homepage():
    return render_template('homepageAdaptative.html')
@app.route('/personalPhoto')
def personalPhoto():
    return render_template('index.html')
@app.route('/personalPhotoGD')
def personalPhotoGD():
    return render_template('index2.html')
@app.route('/personalPhotoInbupt')
def personalPhotoInbupt():
    return render_template('index3.html')
@app.route('/personalPhotoSpring')
def personalPhotoSpring():
    return render_template('index4.html')
@app.route('/personalPhotoFC')
def personalPhotoFc():
    return render_template('index5.html')

if __name__ == '__main__':
    app.run()
