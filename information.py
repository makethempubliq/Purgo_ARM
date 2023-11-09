from flask import Flask, request, send_from_directory, render_template, jsonify, g
from typing import List
from dataclasses import dataclass, field, astuple
#from flaskext.mysql import MySQL
import pymysql




global code
code = ''

@dataclass
class masters:
    Hname:List[str] = field(default_factory=list)
    Rank:List[str] = field(default_factory=list)
    Details:List[str] = field(default_factory=list)
    Hdirect:List[str] = field(default_factory=list)
    sql5:List[str] = field(default_factory=list)
    sql6:List[str] = field(default_factory=list)
    sql7:List[str] = field(default_factory=list)
    sql8:List[str] = field(default_factory=list)
    sql9:List[str] = field(default_factory=list)
    sql10:List[str] = field(default_factory=list)
    college:List[str] = field(default_factory=list)
    Major:List[str] = field(default_factory=list)
    Product:List[str] = field(default_factory=list)
    Competitor:List[str] = field(default_factory=list)
    Manager:List[str] = field(default_factory=list)


db = pymysql.connect(
    host='purgoarmdb.cqqwfl3a6ugn.ap-northeast-2.rds.amazonaws.com',
    user='armteam',
    passwd='purgo1234',
    db='purgo_ARM_DB',
    charset='utf8'
)
sql1 = 'select H.yadmNm, H.clCdNm, substring_index(H.addr, \' \', 2), ifnull(D.hospital_Director, \'미입력\'), H.ykiho from Hospital as H inner join hospital_Detail as D where H.ykiho = D.ykiho'
sql2 = 'select D.recent_Visiting, D.hospital_Rank, H.yadmNm, D.hospital_Director, D.meeting_Detail, D.ykiho from Hospital as H inner join hospital_Detail as D where H.ykiho = D.ykiho'

# select D.recent_Visiting, D.hospital_Rank, D.hospital_Director, D.meeting_Detail, D.ykiho from Hospital as H inner join hospital_Detail as D where H.ykiho = D.ykiho and H.ykiho = '해당병원 요양기호';
cursor = db.cursor()

def masters_init(): #masters 객체를 생성한 후 마스터테이블 값을 가져와 초기화 시킨 후 객체변수를 리턴하는 함수
    
    sql = "select yadmNm from Hospital where ykiho = " + code                         #병원명
    sql2 = "select hospital_Rank from hospital_Detail where ykiho = " + code          #랭크
    sql3 = "select meeting_Detail from hospital_Detail where ykiho = " + code         #내용(최근)
    sql4 = "select hospital_Director from hospital_Detail where ykiho = " + code      #병원장(불러오기)
    sql5 = "select director_College from hospital_Detail where ykiho = " + code       #대학(불러오기)
    sql6 = "select director_Major from hospital_Detail where ykiho = " + code         #전공(불러오기)
    sql7 = "select director_GraduateYear from hospital_Detail where ykiho = " + code  #졸업년도(불러오기)
    sql8 = "select hospital_manager from hospital_Detail where ykiho = " + code       #담당자(불러오기)
    sql9 = "select hospital_Product from hospital_Detail where ykiho = " + code       #제품(불러오기)
    sql10= "select hospital_competitor from hospital_Detail where ykiho = " + code    #경쟁업체(불러오기)
    mang_s= "select * from master_User"
    coll_s = "select * from master_College"
    maj_s = "select * from master_Major"
    pro_s = "select * from master_Product"
    com_s = "select * from master_Competitor"

    dlist_Man = []
    dlist_Hnm = []
    dlist_r = []
    dlist_detail = []
    dlist_Hdirect = []
    dlist_sql5=[]
    dlist_sql6=[]
    dlist_sql7=[]
    dlist_sql8=[]
    dlist_sql9=[]
    dlist_sql10=[]
    dlist_col = []
    dlist_maj = []
    dlist_pro = []
    dlist_com = []
    
    cursor.execute(mang_s)
    manag_p = cursor.fetchall()

    for obj in manag_p:
        dlist_Man.append(obj)

    cursor.execute(sql)
    sql_p = cursor.fetchall()

    for obj in sql_p:
        dlist_Hnm.append(obj)

    cursor.execute(sql2)
    sql2_p = cursor.fetchall()

    for obj in sql2_p:
        dlist_r.append(obj)

    cursor.execute(sql3)
    sql3_p = cursor.fetchall()

    for obj in sql3_p:
        dlist_detail.append(obj)

    cursor.execute(sql4)
    sql4_p = cursor.fetchall()

    for obj in sql4_p:
        dlist_Hdirect.append(obj)

    cursor.execute(sql5)
    sql5_p = cursor.fetchall()

    for obj in sql5_p:
        dlist_sql5.append(obj)

    cursor.execute(sql6)
    sql6_p = cursor.fetchall()

    for obj in sql6_p:
        dlist_sql6.append(obj)

    cursor.execute(sql7)
    sql7_p = cursor.fetchall()

    for obj in sql7_p:
        dlist_sql7.append(obj)

    cursor.execute(sql8)
    sql8_p = cursor.fetchall()

    for obj in sql8_p:
        dlist_sql8.append(obj)

    cursor.execute(sql9)
    sql9_p = cursor.fetchall()

    for obj in sql9_p:
        dlist_sql9.append(obj)

    cursor.execute(sql10)
    sql10_p = cursor.fetchall()

    for obj in sql10_p:
        dlist_sql10.append(obj)

#=======================================================sql(n)
    cursor.execute(coll_s)
    coll_P = cursor.fetchall()
    
    for obj in coll_P:
        dlist_col.append(obj)

    cursor.execute(maj_s)
    maj_P = cursor.fetchall()

    for obj in maj_P:
        dlist_maj.append(obj)

    cursor.execute(pro_s)
    pro_P = cursor.fetchall()

    for obj in pro_P:
        dlist_pro.append(obj)

    cursor.execute(com_s)
    com_P = cursor.fetchall()

    for obj in com_P:
        dlist_com.append(obj)
  
    Masters  = masters(Hname =dlist_Hnm, Rank = dlist_r, Details = dlist_detail, Hdirect = dlist_Hdirect, sql5 = dlist_sql5, sql6 = dlist_sql6,sql7= dlist_sql7,
                       sql8 = dlist_sql8 , sql9= dlist_sql9, sql10 = dlist_sql10,        
                       college = dlist_col, Major=dlist_maj, Product=dlist_pro, Competitor=dlist_com, Manager= dlist_Man)

    return Masters

def getinform():
    cursor.execute(sql1)

    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    #print(data_list)
    #cursor.close()
    return data_list

def get_R_inform():
    cursor.execute(sql2)

    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    #print(data_list)
    #cursor.close()
    return data_list


def get_hospital_names():
    cursor.execute(sql1)
    data = cursor.fetchall()

    # 병원명만 추출하여 리스트로 저장
    hospital_names = [obj[0] for obj in data]

    return hospital_names

def get_progress(email, rank):
    if rank == '관리자' :
        cursor.execute("""select D.hospital_Rank, D.recent_Visiting, D.user_Dept, D.user_Name, H.yadmNm, D.meeting_Detail, D.user_Email, H.ykiho
        from (select hospital_Rank, recent_Visiting, user_Dept, user_Email, meeting_Detail, ykiho, user_Name from hospital_Detail left join master_User on user_Email = hospital_manager) as D
         inner join Hospital as H on D.ykiho = H.ykiho where user_Email is not null""")
    else :
        cursor.execute(f"""select D.hospital_Rank, D.recent_Visiting, D.user_Dept, D.user_Name, H.yadmNm, D.meeting_Detail, D.user_Email, H.ykiho
    from (select hospital_Rank, recent_Visiting, user_Dept, user_Email, meeting_Detail, ykiho, user_Name from hospital_Detail left join master_User on user_Email = hospital_manager) as D
     inner join Hospital as H on D.ykiho = H.ykiho where user_Email = \'{email}\'""")
    data = cursor.fetchall()

    # 병원명만 추출하여 리스트로 저장
    progress = []
    for obj in data:
        progress.append(obj)

    return progress




def getPinform():

    print("여기는 Pinform ")
    print(code)
    Masters = masters_init()
    return Masters


def p_update(data): #팝업 업데이트 함수
    error_sql = "SET FOREIGN_KEY_CHECKS = 0"
    cursor.execute(error_sql)
    up_sql = "update hospital_Detail set hospital_Director = " + "'" + data['H_dir'] + "'" + ", director_College = " + "'" + data['college'] + "'" + ", director_Major = " + "'" + data['major'] + "'" + ", director_GraduateYear = " + "'" + data['GraduYear'] + "'" + ", hospital_manager = " + "'" + data['Manager'] + "'" + ", hospital_Product = " + "'" + data['product'] + "'" + ", hospital_competitor = " + "'" + data['competitor'] + "'" + " where ykiho = " + code
    cursor.execute(up_sql)
    cursor.connection.commit()
    return None

def set_code(s_code):
    global code
    code = s_code
    print("setter :" + code)
    #get_code()

def getSMinform(): #학교 마스터 정보 불러오기 함수
    sql_sm = "select * from master_College"
    cursor.execute(sql_sm)
    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    #print(data_list)
    print(data_list)
    return data_list

def getMJ_inform(): #전공 마스터 정보 불러오기 함수
    sql_mj = "select * from master_Major"
    cursor.execute(sql_mj)
    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    #print(data_list)
    return data_list

def getRK_inform(): #전공 마스터 정보 불러오기 함수
    sql_rk = "select * from master_Rank"
    cursor.execute(sql_rk)
    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    return data_list

def getCP_inform(): #전공 마스터 정보 불러오기 함수
    sql_cp = "select * from master_Competitor"
    cursor.execute(sql_cp)
    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    #print(data_list)
    return data_list

def getPD_inform(): #전공 마스터 정보 불러오기 함수
    sql_pd = "select * from master_Product"
    cursor.execute(sql_pd)
    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    #print(data_list)
    return data_list

def master_update(name, pagdesc):
    try:
        pagdesc = pagdesc
        print("넘버 :" + pagdesc)
        if(pagdesc == "school"): #학교 마스터
            sm_name = name
            
            print("마스터 등록 이름 : " + sm_name)
            check_query = "select * from master_College where college_Name  = %s"
            insert_query = "INSERT into master_College(college_Name) values(%s);"
            cursor = db.cursor()

            if cursor.execute(check_query, (sm_name)): #중복(데이터가 이미 존재하면)(if절이 작동하면 중복)
                return ("동일한 학교명이 이미 존재합니다.")
                    
            elif sm_name == "":                    #입력 데이터가 공백일시
                return ("학교명을 입력하세요.")
                    
            else:
                cursor.execute(insert_query, (sm_name))
                db.commit()
                cursor.connection.commit()
                cursor.close()

                print("엘스")
                return ("해당 학교가 등록되었습니다.")
            
        if(pagdesc == 'major'): #전공 마스터
            Mname = name
            print("넘버 :" + pagdesc)
            print("마스터 등록 이름 : " + Mname)
            check_query = "select * from master_Major where major_Name  = %s"
            insert_query = "INSERT into master_Major(major_Name) values(%s);"
            cursor = db.cursor()

            if cursor.execute(check_query, (Mname)): #중복(데이터가 이미 존재하면)(if절이 작동하면 중복)
                return ("동일한 전공명이 이미 존재합니다.")
            
            elif Mname == "":                    #입력 데이터가 공백일시
                return ("전공명을 입력하세요.")
            
            else:
                cursor.execute(insert_query, (Mname))
                db.commit()
                cursor.close()
                return ("해당 전공이 등록되었습니다.")
        
        if(pagdesc == 'rank'): #전공 마스터
            Rname = name
            print("넘버 :" + pagdesc)
            print("마스터 등록 이름 : " + Rname)
            check_query = "select * from master_Rank where rank_Name  = %s"
            insert_query = "INSERT into master_Rank(rank_Name) values(%s);"
            cursor = db.cursor()

            if cursor.execute(check_query, (Rname)): #중복(데이터가 이미 존재하면)(if절이 작동하면 중복)
                return ("동일한 등급이 이미 존재합니다.")
            
            elif Rname == "":                    #입력 데이터가 공백일시
                return ("등급을 입력하세요.")
            
            else:
                cursor.execute(insert_query, (Rname))
                db.commit()
                cursor.close()
                return ("해당 등급이 등록되었습니다.")
            
        if(pagdesc == 'competitor'): #전공 마스터
            CPname = name
            print("넘버 :" + pagdesc)
            print("마스터 등록 이름 : " + CPname)
            check_query = "select * from master_Competitor where competitor_Name  = %s"
            insert_query = "INSERT into master_Competitor(competitor_Name) values(%s);"
            cursor = db.cursor()

            if cursor.execute(check_query, (CPname)): #중복(데이터가 이미 존재하면)(if절이 작동하면 중복)
                return ("동일한 경쟁업체가 이미 존재합니다.")
            
            elif CPname == "":                    #입력 데이터가 공백일시
                return ("경쟁업체를 입력하세요.")
            
            else:
                cursor.execute(insert_query, (CPname))
                db.commit()
                cursor.close()
                return ("해당 경쟁업채가 등록되었습니다.")
        
        if(pagdesc == 'product'): #전공 마스터
            PDname = name
            print("넘버 :" + pagdesc)
            print("마스터 등록 이름 : " + PDname)
            check_query = "select * from master_Product where product_Name  = %s"
            insert_query = "INSERT into master_Product(product_Name) values(%s);"
            cursor = db.cursor()

            if cursor.execute(check_query, (PDname)): #중복(데이터가 이미 존재하면)(if절이 작동하면 중복)
                return ("동일한 제품이 이미 존재합니다.")
            
            elif PDname == "":                    #입력 데이터가 공백일시
                return ("제품을 입력하세요.")
            
            else:
                cursor.execute(insert_query, (PDname))
                db.commit()
                cursor.close()
                return ("해당 제품이 등록되었습니다.")
            
    except Exception as e:
        print(f"데이터 저장 또는 업데이트 중 오류 발생: {e}")
        return ({"error": "데이터 저장 중 오류가 발생했습니다: "})       

def Hinform_Upadate():
    sql2 = "select * from hospital_Detail where ykiho = "
    cursor.execute(sql2)
    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    #print(data_list)
    #cursor.close()
    return data_list


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
    

def save_data(hospitalName, grade, content, registration_date):
    try:
        hospital_name = request.form.get('hospitalName')
        grade = request.form.get('grade')
        content = request.form.get('content')
        registration_date = request.form.get('registration_date')  
        
        ykiho = get_ykiho_from_hospital_name(hospitalName)

        if ykiho:
            update_query = "UPDATE hospital_Detail SET hospital_Rank = %s, meeting_Detail = %s, recent_Visiting = %s, hospital_manager = %s WHERE ykiho = %s"
            insert_query = "INSERT into meeting_Log(hospital_Rank, meeting_Detail, meeting_Date, meeting_ManagerID, ykiho) select %s, %s, %s, %s, %s from hospital_Detail where ykiho = %s"
            cursor = db.cursor()
            cursor.execute(update_query, (grade, content, registration_date, g.user[3], ykiho))
            cursor.execute(insert_query, (grade, content, registration_date, g.user[3], ykiho, ykiho))

            db.commit()
            cursor.close()

            return "데이터가 성공적으로 업데이트되었습니다"
    except Exception as e:
        print(f"데이터 저장 또는 업데이트 중 오류 발생: {e}")
        return "데이터 저장 중 오류가 발생했습니다"

#17:33:42	update hospital_Detail set hospital_Director = '조석훈' where ykiho = "JDQ4MTg4MSM1MSMkMSMkMCMkNzIkNTgxMzUxIzExIyQxIyQzIyQ3OSQzNjEwMDIjNjEjJDEjJDAjJDgz"	1 row(s) affected Rows matched: 1  Changed: 1  Warnings: 0	0.015 sec
#17:33:21	update hospital_Detail set hospital_Director = '조석훈', hospital_competitor = 'Allo-Oss' where ykiho = "JDQ4MTg4MSM1MSMkMSMkMCMkNzIkNTgxMzUxIzExIyQxIyQzIyQ3OSQzNjEwMDIjNjEjJDEjJDAjJDgz"	Error Code: 1452. Cannot add or update a child row: a foreign key constraint fails (`purgo_ARM_DB`.`hospital_Detail`, CONSTRAINT `hospital_Detail_ibfk_6` FOREIGN KEY (`hospital_competitor`) REFERENCES `master_Competitor` (`competitor_Name`))	0.016 sec
# 대학, 전공, 등급, 제품, 경쟁업체
