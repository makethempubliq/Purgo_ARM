from flask import Flask, request, send_from_directory, render_template
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


db = pymysql.connect(
    host='purgoarmdb.cqqwfl3a6ugn.ap-northeast-2.rds.amazonaws.com',
    user='armteam',
    passwd='purgo1234',
    db='purgo_ARM_DB',
    charset='utf8'
)
sql1 = 'select H.yadmNm, H.clCdNm, substring_index(H.addr, \' \', 2), ifnull(D.hospital_Director, \'미입력\'), H.ykiho from Hospital as H inner join hospital_Detail as D where H.ykiho = D.ykiho'


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
    coll_s = "select * from master_College"
    maj_s = "select * from master_Major"
    pro_s = "select * from master_Product"
    com_s = "select * from master_Competitor"

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
                       college = dlist_col, Major=dlist_maj, Product=dlist_pro, Competitor=dlist_com)

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


def get_hospital_names():
    cursor.execute(sql1)
    data = cursor.fetchall()

    # 병원명만 추출하여 리스트로 저장
    hospital_names = [obj[0] for obj in data]

    return hospital_names



def getPinform():

    

    #data_list = []
    #for obj in data:
    #    data_list.append(obj)
    Masters = masters_init()
    print("여긴 객체 테스트")
    print(Masters.Rank)
    print(Masters.college)
    #print(data_list)
    #cursor.close()
    return Masters


def p_update(data): #팝업 업데이트 함수
    error_sql = "SET FOREIGN_KEY_CHECKS = 0"
    cursor.execute(error_sql)
    up_sql = "update hospital_Detail set hospital_Director = " + "'" + data['H_dir'] + "'" + ", director_College = " + "'" + data['college'] + "'" + ", director_Major = " + "'" + data['major'] + "'" + ", director_GraduateYear = " + "'" + data['GraduYear'] + "'" + ", hospital_manager = " + "'" + data['Manager'] + "'" + ", hospital_Product = " + "'" + data['product'] + "'" + ", hospital_competitor = " + "'" + data['competitor'] + "'" + " where ykiho = " + code
    cursor.execute(up_sql)
    cursor.connection.commit()
    print(up_sql)
    return None

def set_code(s_code):
    global code
    code = s_code
    print("setter :" + code)
    #get_code()

def Hinform_Upadate():
    sql2 = "select * from hospital_Detail where ykiho = "
    print(sql2)
    cursor.execute(sql2)
    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    #print(data_list)
    #cursor.close()
    return data_list
#17:33:42	update hospital_Detail set hospital_Director = '조석훈' where ykiho = "JDQ4MTg4MSM1MSMkMSMkMCMkNzIkNTgxMzUxIzExIyQxIyQzIyQ3OSQzNjEwMDIjNjEjJDEjJDAjJDgz"	1 row(s) affected Rows matched: 1  Changed: 1  Warnings: 0	0.015 sec
#17:33:21	update hospital_Detail set hospital_Director = '조석훈', hospital_competitor = 'Allo-Oss' where ykiho = "JDQ4MTg4MSM1MSMkMSMkMCMkNzIkNTgxMzUxIzExIyQxIyQzIyQ3OSQzNjEwMDIjNjEjJDEjJDAjJDgz"	Error Code: 1452. Cannot add or update a child row: a foreign key constraint fails (`purgo_ARM_DB`.`hospital_Detail`, CONSTRAINT `hospital_Detail_ibfk_6` FOREIGN KEY (`hospital_competitor`) REFERENCES `master_Competitor` (`competitor_Name`))	0.016 sec
# 대학, 전공, 등급, 제품, 경쟁업체
