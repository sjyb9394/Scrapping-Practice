import requests
from bs4 import BeautifulSoup

def extract_job(html,jobid,url):
    title = html.find("h2",{"class":"title"}).find("a").string.strip()
    company = html.find("div",{"class":"company"}).find("span",{"class":"name"}).string
    location = html.find("div",{"class":"location"}).find("span",{"class":"name"}).string.strip()
    job_id = jobid
    date = html.find("div",{"class":"meta"}).find("time").string
    return {'Title': title, 'Company': company, 'Location':location, 'Link': f"{url}&jobid={job_id}",'Date':date}

def extract(url):
    jobs = []
    print(f"Scrapping Monster Website")
    url_result = requests.get(f"{url}")
    soup = BeautifulSoup(url_result.text,'html.parser')
    results = soup.find_all("section",{"class":"card-content"})
    
    for result in results:
        try:
            job_id = result["data-jobid"]
            job = extract_job(result,job_id,url)
            jobs.append(job)
        except:
            pass

    return jobs

def monster_get_jobs(word):
    URL = f"https://www.monster.com/jobs/search/?q={word}&intcid=skr_navigation_nhpso_searchMainPrefill&stpage=1&page=5"
    jobs = extract(URL)
    return jobs