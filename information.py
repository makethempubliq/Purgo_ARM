from flask import Flask, request, send_from_directory, render_template
from flaskext.mysql import MySQL
import pymysql

global code
code = ''

db = pymysql.connect(
    host='purgoarmdb.cqqwfl3a6ugn.ap-northeast-2.rds.amazonaws.com',
    user='armteam',
    passwd='purgo1234',
    db='purgo_ARM_DB',
    charset='utf8'
)
sql1 = 'select H.yadmNm, H.clCdNm, substring_index(H.addr, \' \', 2), ifnull(D.hospital_Director, \'미입력\'), H.ykiho from Hospital as H inner join hospital_Detail as D where H.ykiho = D.ykiho'


cursor = db.cursor()


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
    sql2 = "select * from hospital_Detail where ykiho = " + code
    print(sql2)
    cursor.execute(sql2)

    data = cursor.fetchall()
    data_list = []
    for obj in data:
        data_list.append(obj)

    #print(data_list)
    #cursor.close()
    return data_list


    

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