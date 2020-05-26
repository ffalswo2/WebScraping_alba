#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
# &page={page}

LIMIT = 50
URL = f"http://www.alba.co.kr/job/area/MainLocal.asp?schnm=LOCAL&viewtype=L&sidocd=02&gugun=&d_areacd=&hidListView=LIST&hidSortCnt={LIMIT}&gendercd=C01"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")
    pagenation = soup.find("div",id="NormalInfo").find("strong").get_text(strip=True)
    last = pagenation.replace(',','')

    last_page = int(last) - 14

    if last_page % 50 > 0:
        last_page = (last_page // LIMIT) + 1
    else:
        last_page = last_page // LIMIT

    return last_page

def extract_job(html):
    title = html.find("span",{"class":"title"}).get_text(strip=True)
    company = html.find("span",{"class":"company"}).get_text(strip=True)
    location = html.find("td",{"class":"local"}).get_text(strip=True)
    workTime = html.find("td",{"class":"data"}).get_text(strip=True)
    pay = html.find("span",{"class":"number"}).get_text(strip=True)
    howPay = html.find("span",{"class":"payIcon"}).get_text(strip=True)

    return {'company': company, 'title': title,'location':location,'workTime':workTime,'pay':pay,'howPay':howPay}

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&page={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("tr" and "tr",{"class":"divide"})
        for result in results:
            job = extract_job(result)
            print(job)
            jobs.append(job)

    return jobs

def get_jobs():
    last_page = get_last_page()
    alba = extract_jobs(last_page)

    return alba