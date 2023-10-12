from flask import Flask, render_template,request,g,redirect,url_for
from information import getinform, Hinform_Upadate, set_code,getPinform
import pymysql

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

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
    return render_template('progress-registration.html')

@app.route('/progress-confirmation.html')
def progress_confirmation():
    return render_template('progress-confirmation.html')

@app.route('/manager-function.html')
def manager_function():
    return render_template('manager-function.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/forgot-password.html')
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

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