import requests
import bs4
import pymysql

db = pymysql.connect(host='purgoarmdb.cqqwfl3a6ugn.ap-northeast-2.rds.amazonaws.com',user='armteam',passwd='purgo1234',db='purgo_ARM_DB',charset='utf8')

cursor = db.cursor()
clCD = ['01', '11', '41', '51']
for i in clCD :
    url1 = f'https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList?ServiceKey=pxp83Ms51yvx5MQYAGnfLSJndXx1bi0W1j6n8ul13Ty%2FoDJK3tzJJnpK6Q1ProOguWEpr9c6igNbZnefE8qnbg%3D%3D&numOfRows=100000&clCd={i}'
    response = requests.get(url1)
    content = response.text
    xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
    rows = xml_obj.findAll('item')
    # xml 안의 데이터 수집
    for i in range(0, len(rows)):
        columns = rows[i].find_all()
        #첫째 행 데이터 수집
        text1 = ''
        text2 = ''
        text3 = ''
        for j in range(0,len(columns)):
            text1 = text1 + columns[j].name + ', '
            text2 = text2 + '\"' + columns[j].text + '\"' + ', '
            if columns[j].name != 'ykiho' :
                text3 = text3 + " " + columns[j].name + " = VALUES(" + columns[j].name + "),"
        text1 = text1[:len(text1) - 2]
        text2 = text2[:len(text2) - 2]
        text3 = text3[:len(text3) - 1]
        sql1 = f"INSERT Into Hospital({text1}) VALUES ({text2}) ON DUPLICATE KEY UPDATE {text3}"
        cursor.execute(sql1)
sql2 = "INSERT IGNORE into hospital_Detail(ykiho) select ykiho from Hospital"
cursor.execute(sql2)
db.commit()