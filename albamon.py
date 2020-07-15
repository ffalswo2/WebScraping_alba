#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

URL = "http://www.albamon.com/list/gi/mon_young_list.asp?"
URL2 = "gubun=2&univ=&ps=50&ob=6&sExcChk=y&lvtype=1&rArea=,I000,&gender=M&rWDate=1&Empmnt_Type="

# 여러 페이지 스크레핑 방법 찾아야함


def get_last_page(): # 마지막 페이지를 찾는 함수
    # global page
    result = requests.get(URL+URL2)
    soup = BeautifulSoup(result.text,"html.parser")
    pagenation = soup.find("div",{"class":"pagenation"})
    pages = pagenation.find_all("a")
    last_page = int(pages[-1].get_text())

    return last_page

def normalize(s): # pay : str을 int로 캐스팅변환
    if s == None:
        return 0
    elif s != None:
        return s.replace(',','').strip().replace('원','').strip()

def extract_job(html): # 회사,모집명,위치,시급,근무시간,올린시간 찾아서 딕셔너리로 반환

    company = html.find("div",{"class":"subWrap"}).find("p",{"class":"cName"}).get_text(strip=True)
    title = html.find("div",{"class":"subWrap"}).find("p",{"class":"cTit"}).get_text(strip=True)
    location = html.find("td",{"class":"area"}).get_text(strip=True)[3:]
    pay = html.find("p",{"class":"won"}).get_text(strip=True)
    wage = int(normalize(pay))
    recently = html.find("td",{"class":"recently"}).get_text(strip=True)
    work_time = html.find_previous("td").find_previous("td").get_text(strip=True)

    dic = {'comp': company, 'jobs': title, 'place': location, "money": wage, 'worktime': work_time, 'ago': recently,'howpay':'None'}
    if '' in list(dic.values()):
        i = list(dic.values()).index('')
        keys = list(dic.keys())
        dic[keys[i]] = 'None'
    return dic


def extract_jobs(last_page): # 정보들이 담긴 딕셔너리 리스트에 저장
    jobs = []
    for page in range(last_page):
        print(f"Scraping Albamon page: {page+1}")
        result = requests.get(f"{URL}page={page+1}&{URL2}")
        soup = BeautifulSoup(result.content.decode('euc-kr','replace'),"html.parser")
        results = soup.find_all("tr",id=True)
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs(): # 실행 함수
    last_page = get_last_page()
    alba = extract_jobs(last_page)

    return alba