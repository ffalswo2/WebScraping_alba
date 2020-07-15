import pymysql
import csv
from main import *

conn = pymysql.connect(host='localhost', user='root', password='stephan98', db='study_db', charset='utf8')
curs = conn.cursor()
conn.commit()

f = open('alba.csv','r')
csvReader = csv.reader(f)

for row in csvReader:
    company = (row[0])
    title = (row[1])
    location = (row[2])
    pay = (row[3])
    worktime = (row[4])
    recently = (row[5])
    howpay = (row[6])

    sql = "insert into Alba(comp,jobs,place,money,worktime,ago,howpay) values(%s,%s,%s,%s,%s,%s,%s)"
    curs.execute(sql,(company,title,location,pay,worktime,recently,howpay))

conn.commit()

f.close()
conn.close()