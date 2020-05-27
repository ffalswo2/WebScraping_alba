import csv

def save_to_file(jobs): # csv 파일로 저장
    file = open("alba.csv",mode="w")
    writer = csv.writer(file)
    writer.writerow(["title","company","location","pay","workTime","recently","howpay"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return