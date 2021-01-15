import csv

def save_to_file(jobs):
    file = open("Jobs.csv",mode="w",newline='',encoding="utf8")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Location", "Link", "Date"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return