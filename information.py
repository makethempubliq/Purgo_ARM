from flask import Flask, request, send_from_directory, render_template
from typing import List
from dataclasses import dataclass, field, astuple
#from flaskext.mysql import MySQL
import pymysql




global code
code = ''

@dataclass
class masters:

    Rank:List[str] = field(default_factory=list)
    Details:List[str] = field(default_factory=list)
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

    sql2 = "select hospital_Rank from hospital_Detail where ykiho = " + code
    sql3 = "select meeting_Detail from hospital_Detail where ykiho = " + code
    coll_s = "select * from master_College"
    maj_s = "select * from master_Major"
    pro_s = "select * from master_Product"
    com_s = "select * from master_Competitor"

    dlist_r = []
    dlist_detail = []
    dlist_col = []
    dlist_maj = []
    dlist_pro = []
    dlist_com = []
    print("ㅈㅇㅁㅈㅇㅁㅈㅇㅁㅈㅇㅈㅁ코드: " + code)
    print("sql2 = "+sql2)
    cursor.execute(sql2)
    sql2_p = cursor.fetchall()

    for obj in sql2_p:
        dlist_r.append(obj)

    cursor.execute(sql3)
    sql3_p = cursor.fetchall()

    for obj in sql3_p:
        dlist_detail.append(obj)

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
  
    Masters  = masters(Rank = dlist_r, Details = dlist_detail, college = dlist_col, Major=dlist_maj, Product=dlist_pro, Competitor=dlist_com)

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
