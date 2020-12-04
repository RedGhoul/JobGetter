import requests
from bs4 import BeautifulSoup
import time
import json
from decouple import config
import random
from fake_useragent import UserAgent
from jobber.models import JobPositionItem, JobCitySetItem, JobTypeFind, MaxResultsPerCity, Host, JobTransparencyLinks, \
    MaxAge


# pip freeze > requirements.txt
def Get_Jobs_Task():
    def send_simple_message(JobsFound, ElapsedTime):
        return requests.post(
            "https://api.mailgun.net/v3/experimentsinthedeep2.com/messages",
            auth=("api", config('YOUR_API_KEY', default='JobGetter')),
            data={"from": "JobGetter@experimentsinthedeep2.com",
                  "to": ["avaneesab5@gmail.com"],
                  "subject": "Job Status - JobGetter",
                  "text":
                      f'Total Number of Jobs Found: {str(JobsFound)} ' +
                      f'& Total Time Taken {str(ElapsedTime)}'})

    def check_if_dup(description, url, title):
        header = {
            "Content-type": "application/json",
            "Accept": "text/plain",
        }
        data = json.dumps({"description": description, "url": url, "title": title})
        response = requests.post(url=techTransCheck, data=data, headers=header)
        time.sleep(1)
        if response.text == 'false':
            return False
        elif response.text == 'true':
            return True
        else:
            return False

    jobs_done = []
    max_results_per_city = MaxResultsPerCity.objects.first().MaxNumber
    postionFind = []
    for item in JobPositionItem.objects.all():
        postionFind.append(str(item))

    job_Type = "fulltime"
    city_set = []

    for item in JobCitySetItem.objects.all():
        city_set.append(str(item))

    max_age = MaxAge.objects.first().Age
    host = Host.objects.first().Host
    techTrans = JobTransparencyLinks.objects.first().TechTrans
    techTransCheck = JobTransparencyLinks.objects.first().TechTransCheck

    def make_indeed_request(city, pos, start):
        ua = UserAgent().ie
        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            'User-Agent': ua
        }
        page = requests.get(
            "http://"
            + host
            + "/jobs?q="
            + pos
            + "+%2420%2C000&l="
            + str(city)
            + "&jt="
            + job_Type
            + "&fromage="
            + str(max_age)
            + "&start="
            + str(start),
            headers=headers
        )
        soup = BeautifulSoup(page.text, "html.parser")
        for each in soup.find_all(class_="result"):
            try:
                title = each.find(class_="jobtitle").text.replace("\n", "").replace(",", "")
            except:
                title = "NULL"
            job_URL = "NULL"
            try:
                job_URL = (
                        "https://"
                        + host
                        + each.find(class_="jobtitle")["href"].replace(",", "")
                )

            except:
                job_URL = "NULL"
            try:
                if job_URL != "NULL":
                    mainPage = requests.get(job_URL)
                    time.sleep(1)
                    DescriptionSoup = BeautifulSoup(mainPage.text, "html.parser")
                    synopsis = str(
                        DescriptionSoup.findAll("div", {"id": "jobDescriptionText"})[0]
                            .prettify()
                            .replace("\n", "")
                            .replace(",", "")
                    )
                    if synopsis is None:
                        continue
            except:
                synopsis = "NULL"

            try:
                location = (
                    each.find("span", {"class": "location"})
                        .text.replace("\n", "")
                        .replace(",", "")
                )
            except:
                location = "N/A"
            try:
                company = (
                    each.find(class_="company").text.replace("\n", "").replace(",", "")
                )
            except:
                company = "NULL"
            try:
                salary = each.find(class_="salary.no-wrap").text.replace(",", "")
            except:
                salary = "N/A"

            try:
                PostDate = each.find(class_="date").text.replace("\n", "").replace(",", "")
            except:
                PostDate = "N/A"
            if job_URL != "NULL":
                if check_if_dup(synopsis, job_URL, title) == False:
                    ua = UserAgent().ie
                    headers = {
                        "Content-type": "application/json",
                        "Accept": "text/plain",
                        'User-Agent': ua
                    }
                    jobs_done.append("1")
                    body = {
                        "title": title,
                        "description": synopsis,
                        "url": job_URL,
                        "company": company,
                        "location": location,
                        "postDate": PostDate,
                        "salary": salary,
                        "jobSource": "Indeed",
                        "numberOfApplies": 0,
                        "numberOfViews": 0,
                        "poster": None,
                        "posters": "None",
                    }
                    r = json.dumps(body)
                    mainPage = requests.post(url=techTrans, data=r, headers=headers)
                else:
                    print("Already found this Job")

    start = time.time()
    for city in city_set:
        for pos in postionFind:
            for start in range(0, max_results_per_city, 10):
                time.sleep(random.randint(1, 6) * 5)
                make_indeed_request(city, pos, start)

    end = time.time()
    total_time_needed = end - start
    send_simple_message(len(jobs_done), total_time_needed)
