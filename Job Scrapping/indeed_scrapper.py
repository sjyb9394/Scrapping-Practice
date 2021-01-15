import requests
from bs4 import BeautifulSoup

LIMIT = 30

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,'html.parser')
    pagination = soup.find("div",{"class":"pagination"})
    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    page_num = int(max_page)
    if page_num <=3:
      return page_num
    else:
      page_num = 4
    return page_num

def extract_job(html):
    title = html.find("h2",{"class":"title"}).find("a")["title"]
    company = html.find("span",{"class":"company"})
    company_anchor = company.find("a")
    if company.find("a") is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    date = html.find("span",{"class":"date"}).string

    return {'Title': title, 'Company': company, 'Location':location, 'Link': f"https://www.indeed.com/viewjob?jk={job_id}",'Date':date}

def extract(pgnum,url):
    jobs = []
    for page in range(pgnum):
        print(f"Scrapping page {page+1}")
        result = requests.get(f"{url}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text,'html.parser')
        results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs

def indeed_get_jobs(word):
    URL = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}"
    page_num = get_last_page(URL)
    jobs = extract(page_num,URL)
    return jobs