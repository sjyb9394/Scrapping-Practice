import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    if soup.find("div", {"class":"s-pagination"}) is not None:
      pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
    else:
      return 0
    last_page = pages[-2].get_text(strip=True)
    page_num = int(last_page)
    if page_num <= 3:
      return page_num
    else:
      page_num = 4
    return page_num

def extract(last_page,url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page+1}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div",{"class":"-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def extract_job(html):
    title = html.find("h2",{"class":"mb4"}).find("a")["title"]
    company = html.find("span").get_text(strip = True)
    location = html.find("span",{"class":"fc-black-500"}).string.strip()
    link = html["data-jobid"]
    date = html.find("ul",{"class":"mt4"}).find("span").string
    return {'Title':title, 'Company':company,'Location':location,'Link':f"https://stackoverflow.com/jobs/{link}",'Date':date}

def so_get_jobs(word):
    URL = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(URL)
    jobs = extract(last_page,URL)
    return jobs