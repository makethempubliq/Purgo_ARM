from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, g
import pymysql
import json
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from jinja2 import Environment

from loginregister import UserCreateForm, UserLoginForm, ResetPasswordForm, ChangePasswordForm
from information import getinform, set_code, getPinform,get_R_inform, p_update,get_hospital_names,getSMinform,getMJ_inform,getRK_inform,getCP_inform,getPD_inform,master_update, get_progress,get_ykiho_from_hospital_name,save_data,getU_inform,mn_Update

from flask_sqlalchemy import SQLAlchemy

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import bs4
import requests
from flask_mail import Mail, Message
from datetime import datetime, timedelta
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

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'action_123@hufs.ac.kr'
app.config['MAIL_PASSWORD'] = '9597okokok.'

mail = Mail(app)

def daily_API():
    db = pymysql.connect(host='purgoarmdb.cqqwfl3a6ugn.ap-northeast-2.rds.amazonaws.com', user='armteam',
                         passwd='purgo1234', db='purgo_ARM_DB', charset='utf8')

    cursor = db.cursor()
    cursor.execute("set innodb_lock_wait_timeout= 28800;")
    clCD = ['01', '11', '41', '51']
    for i in clCD:
        url1 = f'https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList?ServiceKey=pxp83Ms51yvx5MQYAGnfLSJndXx1bi0W1j6n8ul13Ty%2FoDJK3tzJJnpK6Q1ProOguWEpr9c6igNbZnefE8qnbg%3D%3D&numOfRows=100000&clCd={i}'

        response = requests.get(url1, verify=False)

        content = response.text
        xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
        rows = xml_obj.findAll('item')
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # xml 안의 데이터 수집
        for i in range(0, len(rows)):
            columns = rows[i].find_all()
            # 첫째 행 데이터 수집
            text1 = ''
            text2 = ''
            text3 = ''
            for j in range(0, len(columns)):
                text1 = text1 + columns[j].name + ', '
                text2 = text2 + '\"' + columns[j].text + '\"' + ', '
                if columns[j].name != 'ykiho':
                    text3 = text3 + " " + columns[j].name + " = VALUES(" + columns[j].name + "),"
            text1 = text1[:len(text1) - 2]
            text2 = text2[:len(text2) - 2]
            text3 = text3[:len(text3) - 1]
            sql1 = f"INSERT Into Hospital({text1}) VALUES ({text2}) ON DUPLICATE KEY UPDATE {text3}"
            cursor.execute(sql1)
    sql2 = "INSERT IGNORE into hospital_Detail(ykiho) select ykiho from Hospital"
    cursor.execute(sql2)
    db.commit()
    print("Scheduled task executed!")


def send_Email():
    with app.app_context():
        cursor = db.cursor()
        cursor.execute("select hospital_manager, recent_Visiting, yadmNm from hospital_Detail as d inner join Hospital as h where d.ykiho = h.ykiho and hospital_manager is not null")
        list = cursor.fetchall()

        for obj in list:
            if obj[1] == (datetime.today()-timedelta(90)).strftime("%Y-%m-%d"):
                email = obj[0]
                msg = Message('담당 병원 재방문 요망', sender='action_123@hufs.ac.kr', recipients=[email])
                msg.body = f'{obj[2]}의 최근 방문일로부터 90일 경과되었습니다.'
                mail.send(msg)
    print("Scheduled task executed!")



# APScheduler를 설정하여 매일 정각에 scheduled_task 함수를 실행합니다
def schedule_task():
    scheduler = BackgroundScheduler()

    # daily_API 작업 추가
    trigger_daily_api = CronTrigger(hour=0, minute=0, second=0)
    #scheduler.add_job(daily_API, trigger=trigger_daily_api)

    # send_Email 작업 추가
    trigger_send_email = CronTrigger(hour=0, minute=30, second=0)
    scheduler.add_job(send_Email, trigger=trigger_send_email)

    scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/master-school.html')
def master_school():
    if not g.user :
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else :
        if g.user[6] == 'Y' :
            return render_template('master-school.html', sm_master=getSMinform())
        else :
            flash("권한이 없습니다.")
            return redirect(url_for('index'))


    
@app.route('/master-major.html')
def master_major():
    if not g.user :
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else :
        if g.user[6] == 'Y':
            return render_template('master-major.html', mj_master = getMJ_inform())
        else:
            flash("권한이 없습니다.")
            return redirect(url_for('index'))

@app.route('/master-grade.html')
def master_grade():
    if not g.user :
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else :
        if g.user[6] == 'Y':
            return render_template('master-grade.html', rk_master = getRK_inform())
        else:
            flash("권한이 없습니다.")
            return redirect(url_for('index'))

@app.route('/master-competition.html')
def master_competition():
    if not g.user :
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else :
        if g.user[6] == 'Y':
            return render_template('master-competition.html', cp_master = getCP_inform())
        else:
            flash("권한이 없습니다.")
            return redirect(url_for('index'))

@app.route('/master-product.html')
def master_product():
    if not g.user :
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else :
        if g.user[6] == 'Y':
            return render_template('master-product.html', pd_master = getPD_inform())
        else:
            flash("권한이 없습니다.")
            return redirect(url_for('index'))

@app.route('/master-information.html')
def master_information():
    if not g.user :
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else :
        if g.user[6] == 'Y':
            return render_template('master-information.html', ur_master = getU_inform())
        else:
            flash("권한이 없습니다.")
            return redirect(url_for('index'))

@app.route('/hospital-information.html')
def hospital_information():
    if not g.user :
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else :
        if g.user[6] == 'Y':
            return render_template('hospital-information.html',hospital = getinform())
        else:
            flash("권한이 없습니다.")
            return redirect(url_for('index'))

@app.route('/progress-registration.html')
def progress_registration():
    if not g.user :
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else :
        if g.user[6] == 'Y':
            return render_template('progress-registration.html',hospital = get_R_inform())
        else:
            flash("권한이 없습니다.")
            return redirect(url_for('index'))

@app.route('/progress-confirmation.html')
def progress_confirmation():
    if not g.user :
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else :
        if g.user[6] == 'Y':
            return render_template('progress-confirmation.html', progress = get_progress(g.user[3], g.user[5]))
        else:
            flash("권한이 없습니다.")
            return redirect(url_for('index'))

@app.route('/manager-function.html')
def manager_function():
    if not g.user:
        flash("로그인이 필요한 기능입니다.")
        return redirect(url_for('login'))
    else:
        if g.user[5] == '관리자' and g.user[6] == 'Y':
            return render_template('manager-function.html', mnfunc = getU_inform())
        else :
            flash("권한이 없습니다.")
            return redirect(url_for('index'))

@app.route('/login.html', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        cursor = db.cursor()
        cursor.execute(f"select user_Email from master_User where user_Email = \'{form.email.data}\'")
        user = cursor.fetchone()
        cursor.execute(f"select user_Password from master_User where user_Email = \'{form.email.data}\'")
        pw = cursor.fetchone()
        cursor.close()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(pw[0], form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        flash(error)
    return render_template('login.html', form=form)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/forgot-password.html', methods=('GET', 'POST'))
def forgot_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        cursor = db.cursor()
        cursor.execute(f"select * from master_User where user_Email = \'{form.email.data}\'")
        user = cursor.fetchone()
        if user:
            # Generate and send a reset password email
            send_reset_password_email(email)
            flash('Password reset email sent. Check your inbox.')
            return redirect(url_for('index'))
        else:
            flash('Invalid email address.')
    return render_template('forgot-password.html', form=form)

def send_reset_password_email(email):
    # Generate a temporary password (you may want to use a secure method)
    temp_password = 'temporary-password'
    tempPW = generate_password_hash(temp_password)
    cursor = db.cursor()
    cursor.execute(f"UPDATE master_User SET user_Password = \'{tempPW}\' WHERE user_Email = \'{email}\'")
    cursor.close()
    db.commit()
    # Send the reset password email
    msg = Message('Password Reset', sender='action_123@hufs.ac.kr', recipients=[email])
    msg.body = f'Your temporary password is: {temp_password}\nPlease reset your password after logging in.'
    mail.send(msg)

@app.route('/change-password.html', methods=('GET', 'POST'))
def change_Password():
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        cursor = db.cursor()
        cursor.execute(f"select user_Email from master_User where user_Email = \'{form.email.data}\'")
        user = cursor.fetchone()
        cursor.execute(f"select user_Password from master_User where user_Email = \'{form.email.data}\'")
        pw = cursor.fetchone()
        cursor.close()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(pw[0], form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            newPassword = generate_password_hash(form.newpassword.data)
            cursor = db.cursor()
            cursor.execute(f"UPDATE master_User SET user_Password = \'{newPassword}\' WHERE user_Email = \'{form.email.data}\'")
            cursor.close()
            db.commit()
            return redirect(url_for('login'))
    return render_template('change-password.html', form=form)

@app.route('/register.html', methods=('GET', 'POST'))
def register():
    form = UserCreateForm()
    cursor = db.cursor()
    cursor.execute(f"select user_Email from master_User where user_Email = \'{form.email.data}\'")
    user = cursor.fetchall()
    if request.method == 'POST' and form.validate_on_submit():
        if not user:
            username=form.username.data
            password=generate_password_hash(form.password1.data)
            email=form.email.data
            dept=form.dept.data
            sql = f"insert into master_User(user_Name, user_Password, user_Email, user_Dept) values(\'{username}\', \'{password}\', \'{email}\', \'{dept}\')"
            cursor.execute(sql)
            db.commit()
            cursor.close()
            return redirect(url_for('index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('register.html', form=form)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = pymysql.connect(
            host='purgoarmdb.cqqwfl3a6ugn.ap-northeast-2.rds.amazonaws.com',
            user='armteam',
            passwd='purgo1234',
            db='purgo_ARM_DB',
            charset='utf8'
        )
        cursor = db.cursor()
        cursor.execute(f"select * from master_User where user_Email = \'{user_id}\'")
        g.user = cursor.fetchone()
        cursor.close()


@app.route('/update', methods=['POST'])
def popup_update():
    data = {"H_dir" : request.form.get("H_dir"), "college" : request.form.get("college"), "major" : request.form.get("major"), 
            "GraduYear" : request.form.get("GraduYear"),"Manager" : request.form.get("Manager"),"product" : request.form.get("product")
            ,"competitor":request.form.get("competitor")}
    
    p_update(data)
    return redirect(url_for('popup_function'))

@app.route('/save_data_mn', methods=['POST'])
def save_data_nm():
    print("여긴 nm 테스트")
    # HTML에서 전송된 데이터를 받아옴
    data_list_json = request.form.get('dataList')
    
    # JSON 형식의 데이터를 파이썬 리스트로 변환
    data_list = json.loads(data_list_json)
    
    # 여기서 data_list를 사용하여 필요한 작업 수행
    print("받은 데이터:", data_list)
    
    # 예를 들어 데이터를 데이터베이스에 저장하거나 다른 처리를 할 수 있습니다.
    mn_Update(data_list)

    return redirect(url_for('manager_function'))


@app.route('/popup')
def popup_function():
    return render_template('popup.html',P_hospital=getPinform())


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print("output")
    print(output)
    set_code(output) #여기서 코드값 inform.py로 넘긴다
    return ('', 204)

def generate_unique_id():
    pass

@app.route('/get_hospital_names', methods=['GET'])
def get_hospital_names_endpoint():
    hospital_names = get_hospital_names()
    return jsonify(hospital_names)

app.jinja_env.globals['generate_unique_id'] = generate_unique_id


@app.route('/save_data_sm', methods=['POST'])
def save_data_sm():
    print("테스트문구:")
    jso = master_update(request.form.get('name'),request.form.get('pagdesc'))
    return jsonify({"message": jso})  

       
@app.route('/get_Log_inform', methods=['POST'])
def get_Log_inform(): #로그 불러오기
    cursor = db.cursor()
    ykiho = request.form.get('ykiho')
    sql_log = "select meeting_Date, hospital_Rank, meeting_Detail from meeting_Log where ykiho = %s order by meeting_Date desc"
    cursor.execute(sql_log, (ykiho, ))
    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)
    return data_list

@app.route('/save_data', methods=['POST'])
def save_data_route():
    hospitalName = request.form.get('hospitalName')
    grade = request.form.get('grade')
    content = request.form.get('content')
    registration_date = request.form.get('registration_date')  
    
    try:
        result = save_data(hospitalName, grade, content, registration_date)
        if result == "데이터가 성공적으로 업데이트되었습니다":
            return jsonify({"message": result})
        else:
            return jsonify({"error": result})
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": "데이터 저장 또는 업데이트 중 오류 발생: " + error_message})

def fetch_hospital_data_from_db():
    with db.cursor() as cursor:
        select_sql = "SELECT * FROM Hospital_Detail"
        cursor.execute(select_sql)
        hospital_data = cursor.fetchall()
    return hospital_data


if __name__ == '__main__':
    schedule_task()
    app.run(debug=True)
