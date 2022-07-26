"""
web scraping functionality from www.indeed.com (USA)
"""
import requests
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

import pandas as pd

source = "indeed.com"
cookies = {'aep_usuc_f': 'region=US&site=glo&b_locale=en_US&c_tp=USD'}


def get_url(position):
    """
    Generate URL from position and company type: recruiter or direct employer; education level
    """
    url = f"https://indeed.com/jobs?q={position}"

    return url


def get_job_date(card):
    """
     extracts date from the job post record

    :param card:
    :return:
    """
    post_str = card.find('span', {'class': 'date'}).text  # text from the footer: days ago was posted
    post_days = re.findall(r'\d+', post_str)  # extracting number of days from posted_str

    if post_days:
        # calculated date of job posting if days are mentioned
        job_date = (datetime.now() - timedelta(days=int(post_days[0]))).strftime("%d/%m/%Y")
    else:
        job_date = datetime.now().strftime("%d/%m/%Y")  # if days are not mentioned - using today

    return job_date


def get_job_salaries(card):
    """
    extracts salaries
    :param card:
    :return:
    """

    try:
        salary_str = card.find('div', 'metadata salary-snippet-container').text
        salaries = re.findall(r"\b(\w+[.]\w+)", salary_str)

    except AttributeError:
        salaries = []

    return salaries


def get_record(card):
    """
    Extract job data from a single record
    """
    span_tag = card.h2.a.span
    a_tag = card.h2.a

    job_id = a_tag.get("data-jk")  # unique job id
    job_title = span_tag.get("title")  # job title
    job_url = 'https://www.indeed.com' + a_tag.get('href')  # job url
    company_name = card.find('span', {'class': 'companyName'}).text  # company name
    job_loc = card.find('div', {'class': 'companyLocation'}).text  # job location
    job_summary = card.find('div', {'class': 'job-snippet'}).text.strip()  # job description
    job_date = get_job_date(card)  # job posting date
    job_salary = get_job_salaries(card)  # job salaries if any

    record = (job_id, job_title, job_date, job_loc, job_summary, job_salary, job_url, company_name)

    return record


def get_jobs(position):
    """
    creates a DataFrame with all records (scraped jobs), scraping from all pages

    """

    url = get_url(position)
    records = []

    # extract the job data

    while True:

        response = ""
        while response == "":
            try:
                response = requests.get(url=url, cookies=cookies)
                break
            except ConnectionError:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

        soup = BeautifulSoup(response.text, 'html.parser')

        cards = soup.find_all('div', 'job_seen_beacon')

        for card in cards:
            record = get_record(card)
            records.append(record)

        time.sleep(3)  # making a pause before moving to the next page

        # moving to the next page - > assigning a new url
        try:
            url = 'https://indeed.com/' + soup.find('a', {'aria-label': 'Next'}).get('href')

        except AttributeError:
            break

    # save the data as DF
    columns = ['job_id',
               'job_title',
               'job_date',
               'job_loc',
               'job_summary',
               'job_salary',
               'job_url',
               'company_name']
    df = pd.DataFrame(data=records, columns=columns)

    # adding to DF columns with search parameters
    search_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    df["search_time"] = search_time
    df["search_position"] = position
    df["source"] = source

    return df
