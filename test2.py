#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

URL = "http://www.albamon.com/list/gi/mon_young_list.asp?"
URL2 = "gubun=2&univ=&ps=50&ob=6&sExcChk=y&lvtype=1&rArea=,I000,&gender=M&rWDate=1&Empmnt_Type="

# 여러 페이지 스크레핑 방법 찾아야함


def get_last_page(): # 마지막 페이지를 찾는 함수
    global page
    result = requests.get(URL+URL2)
    soup = BeautifulSoup(result.text,"html.parser")
    pagenation = soup.find("div",{"class":"pagenation"})
    pages = pagenation.find_all("a")
    last_page = int(pages[-1].get_text())

    return last_page

def extract_job(html): # 회사와 모집명 찾아서 딕셔너리로 반환

    company = html.find("div",{"class":"subWrap"}).find("p",{"class":"cName"}).get_text(strip=True)
    title = html.find("div",{"class":"subWrap"}).find("p",{"class":"cTit"}).get_text(strip=True)

    return {'company':company,'title':title}

def extract_location(html): # 위치를 찾아서 딕셔너리로 반환

    location = html.get_text(strip=True)[3:]

    return {'location':location}



def extract_jobs(last_page): # 딕셔너리로 받은 회사와 회사명을 리스트로 저장
    jobs = []
    for page in range(last_page):
        print(f"Scraping Albamon page: {page+1}")
        result = requests.get(f"{URL}page={page+1}&{URL2}")
        soup = BeautifulSoup(result.content.decode('euc-kr','replace'),"html.parser")
        results = soup.find_all("td",{"class":"subject"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs

def extract_jobs_location(last_page): # 딕셔너리로 받은 위치를 리스트로 저장
    location = []

    for page in range(last_page):
        result = requests.get(f"{URL}page={page+1}&{URL2}")
        soup = BeautifulSoup(result.content.decode('euc-kr','replace'),"html.parser")
        results = soup.find_all("td",{"class":"area"})

        for result in results:
            loca = extract_location(result)
            location.append(loca)

    return location




def get_jobs(): # 리스트1(회사&회사명) + 리스트2(위치), 최종완성리스트 작성
    dict_list1 = extract_jobs(get_last_page())
    dict_list2 = extract_jobs_location(get_last_page())

    final_list = []
    for i in dict_list1:
        for j in dict_list2:
            i.update(j)
            final_list.append(i)

    return final_list