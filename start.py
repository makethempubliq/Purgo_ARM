from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, g
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from jinja2 import Environment

from loginregister import UserCreateForm, UserLoginForm
from information import getinform, set_code, getPinform,get_R_inform, p_update,get_hospital_names,getSMinform,getMJ_inform,getRK_inform,getCP_inform,getPD_inform,master_update

from flask_sqlalchemy import SQLAlchemy

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import bs4
import requests

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

def scheduled_task():
    db = pymysql.connect(host='purgoarmdb.cqqwfl3a6ugn.ap-northeast-2.rds.amazonaws.com', user='armteam',
                         passwd='purgo1234', db='purgo_ARM_DB', charset='utf8')

    cursor = db.cursor()
    clCD = ['01', '11', '41', '51']
    for i in clCD:
        url1 = f'https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList?ServiceKey=pxp83Ms51yvx5MQYAGnfLSJndXx1bi0W1j6n8ul13Ty%2FoDJK3tzJJnpK6Q1ProOguWEpr9c6igNbZnefE8qnbg%3D%3D&numOfRows=100000&clCd={i}'
        response = requests.get(url1)
        content = response.text
        xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
        rows = xml_obj.findAll('item')
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

# APScheduler를 설정하여 매일 정각에 scheduled_task 함수를 실행합니다
def schedule_task():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=0, minute=0, second=0)  # 매일 00:00:00에 실행
    scheduler.add_job(scheduled_task, trigger=trigger)
    scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/master-school.html')
def master_school():
    return render_template('master-school.html', sm_master = getSMinform())
    
@app.route('/master-major.html')
def master_major():
    return render_template('master-major.html', mj_master = getMJ_inform())

@app.route('/master-grade.html')
def master_grade():
    return render_template('master-grade.html', rk_master = getRK_inform())

@app.route('/master-competition.html')
def master_competition():
    return render_template('master-competition.html', cp_master = getCP_inform())

@app.route('/master-product.html')
def master_product():
    return render_template('master-product.html', pd_master = getPD_inform())

@app.route('/master-information.html')
def master_information():
    return render_template('master-information.html')

@app.route('/hospital-information.html')
def hospital_information():
    
    return render_template('hospital-information.html',hospital = getinform())

@app.route('/progress-registration.html')
def progress_registration():
    return render_template('progress-registration.html',hospital = get_R_inform())

@app.route('/progress-confirmation.html')
def progress_confirmation():
   
    return render_template('progress-confirmation.html', hospital_names = get_hospital_names())

@app.route('/manager-function.html')
def manager_function():
    return render_template('manager-function.html')

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

@app.route('/forgot-password.html')
def forgot_password():
    return render_template('forgot-password.html')

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

def get_ykiho_from_hospital_name(hospital_name):
    cursor = db.cursor()
    select_query = "SELECT ykiho FROM Hospital WHERE yadmNm = %s"
    cursor.execute(select_query, (hospital_name,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[0]  
    else:
        return None

@app.route('/save_data_sm', methods=['POST'])
def save_data_sm():
    print("테스트문구:")
    jso = master_update(request.form.get('name'),request.form.get('pagdesc'))
    return jsonify({"message": jso})      
       
    


@app.route('/save_data', methods=['POST'])
def save_data():
    try:
        hospital_name = request.form.get('hospitalName')
        grade = request.form.get('grade')
        content = request.form.get('content')

        ykiho = get_ykiho_from_hospital_name(hospital_name)

        if ykiho:
            update_query = "UPDATE hospital_Detail SET hospital_Rank = %s, meeting_Detail = %s, hospital_manager = %s WHERE ykiho = %s"
            insert_query = "INSERT into meeting_Log(hospital_Rank, meeting_Detail, meeting_Date, meeting_ManagerID, ykiho) select %s, %s, recent_Visiting, %s, %s from hospital_Detail where ykiho = %s"
            cursor = db.cursor()
            cursor.execute(update_query, (grade, content, g.user[3], ykiho))
            cursor.execute(insert_query, (grade, content, g.user[3], ykiho, ykiho))
            db.commit()
            cursor.close()
            return jsonify({"message": "데이터가 성공적으로 업데이트되었습니다"})
        else:
            return jsonify({"message": "해당 병원명이 존재하지 않습니다."})

    except Exception as e:
        print(f"데이터 저장 또는 업데이트 중 오류 발생: {e}")
        return jsonify({"error": "데이터 저장 중 오류가 발생했습니다: "})

def fetch_hospital_data_from_db():
    with db.cursor() as cursor:
        select_sql = "SELECT * FROM Hospital_Detail"
        cursor.execute(select_sql)
        hospital_data = cursor.fetchall()
    return hospital_data

@app.route('/update_registration_date', methods=['POST'])
def update_registration_date():
    selected_date = request.form.get('registration_date')
    selected_ykiho = request.form.get('ykiho')

    try:
        with db.cursor() as cursor:
            update_sql = "UPDATE hospital_Detail SET recent_Visiting = %s WHERE ykiho = %s"
            cursor.execute(update_sql, (selected_date, selected_ykiho))
            db.commit()
            return jsonify({"message": "날짜가 성공적으로 저장되었습니다"})
    except pymysql.Error as e:
        db.rollback()
        return jsonify({"error": f"데이터베이스 오류: {str(e)}"})
    except Exception as e:
        return jsonify({"error": f"서버 오류: {str(e)}"})

if __name__ == '__main__':
    schedule_task()
    app.run(debug=True)
