import datetime
import logging
import requests
import bs4
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json
import os
import threading
from jobber.models import JobPositionItem, JobCitySetItem, JobTypeFind, MaxResultsPerCity, Host, JobTransparencyLinks

def GetJobs_Task():
    header = {
        "Content-type": "application/json",
        "Accept": "text/plain",
    }
    jobs_done = []
    max_results_per_city = MaxResultsPerCity.objects.first().MaxNumber
    postionFind = []
    for item in JobPositionItem.objects.all():
        postionFind.append(str(item))

    job_Type = "fulltime"
    city_set = []

    for item in JobCitySetItem.objects.all():
        city_set.append(str(item))

    max_age = "15"
    host = Host.objects.first().Host
    techTrans = JobTransparencyLinks.objects.first().TechTrans
    techTransCheck = JobTransparencyLinks.objects.first().TechTransCheck

    def checkifdup(description, url, title):
        data = json.dumps({"description": description,"url":url,"title":title})
        response = requests.post(url=techTransCheck, data=data, headers=header)
        time.sleep(1)
        if response.text == 'false':
            return False
        elif response.text == 'true':
            return True
        else:
            return False

    def dotheWork(city, pos, start, finalFileName):
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
            + max_age
            + "&start="
            + str(start)
        )
        time.sleep(1)  # ensuring at least 1 second between page grabs
        soup = BeautifulSoup(page.text, "html.parser")
        for each in soup.find_all(class_="result"):
            try:
                title = each.find(class_="jobtitle").text.replace("\n", "").replace(",", "")
            except:
                title = "NULL"
            # print(title)
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
                    # print(synopsis)
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
                if checkifdup(synopsis, job_URL, title) == False:
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
                    mainPage = requests.post(url=techTrans, data=r, headers=header)
                else:
                    print("Already found this Job")

    def Indeed():
        workers = []
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S").replace(" ", "").replace(":", "")
        finalFileName = ("JobPostingIndeed" + dt_string).replace("/", "")

        # scraping code:
        for city in city_set:
            for pos in postionFind:
                for start in range(0, max_results_per_city, 10):
                    # dotheWork()
                    thread1 = threading.Thread(
                        target=dotheWork,
                        args=(city, pos, start, city + pos + str(start) + finalFileName),
                    )
                    workers.append(thread1)

        for process in workers:
            process.start()

        for process in workers:
            process.join()

    def startup():
        start = time.time()
        print("Starting Scrapping")
        Indeed()
        print("Completed Scrapping")
        end = time.time()
        total_time_needed = end - start
        newJobCount = len(jobs_done)

    startup()