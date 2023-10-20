from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect


from loginregister import UserCreateForm
from information import getinform, set_code, getPinform


import config


db = pymysql.connect(
    host='purgoarmdb.cqqwfl3a6ugn.ap-northeast-2.rds.amazonaws.com',
    user='armteam',
    passwd='purgo1234',
    db='purgo_ARM_DB',
    charset='utf8'
)

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
app.config.from_object(config)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/master-school.html')
def master_school():
    return render_template('master-school.html')
    


@app.route('/master-major.html')
def master_major():
    return render_template('master-major.html')

@app.route('/master-grade.html')
def master_grade():
    return render_template('master-grade.html')

@app.route('/master-competition.html')
def master_competition():
    return render_template('master-competition.html')

@app.route('/master-product.html')
def master_product():
    return render_template('master-product.html')

@app.route('/master-information.html')
def master_information():
    return render_template('master-information.html')

@app.route('/hospital-information.html')
def hospital_information():
    
    return render_template('hospital-information.html',hospital = getinform())

@app.route('/progress-registration.html')
def progress_registration():
    hospital_names = get_hospital_names()
    return render_template('progress-registration.html',hospital_names=hospital_names)

@app.route('/progress-confirmation.html')
def progress_confirmation():
    hospital_names = get_hospital_names()
    return render_template('progress-confirmation.html', hospital_names=hospital_names)

@app.route('/manager-function.html')
def manager_function():
    return render_template('manager-function.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/forgot-password.html')
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/register.html', methods=('GET', 'POST'))
def register():
    form = UserCreateForm()
    cursor = db.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        cursor.execute(f"select user_Email from master_User where user_Email = \'{form.email.data}\'")
        user = cursor.fetchall()
        data_list = []
        for obj in user:
            data_list.append(obj)
        if form.email.data not in data_list:
            username=form.username.data
            password=generate_password_hash(form.password1.data)
            email=form.email.data
            dept=form.dept.data
            sql = f"insert into master_User(user_Name, user_Password, user_Email, user_Dept) values(\'{username}\', \'{password}\', \'{email}\', \'{dept}\')"
            cursor.execute(sql)
            db.commit()
            return redirect(url_for('index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('register.html', form=form)


@app.route('/popup')
def popup_function():
    return render_template('popup.html',P_hospital=getPinform())


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()

    set_code(output)
    return ('', 204)


if __name__ == '__main__':
    app.run(debug=True)
