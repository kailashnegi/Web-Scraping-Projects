
from bs4 import BeautifulSoup
import requests
import time

# This is to filter out skills that you dont want jobs for
print("Put some skills that you are not familiar with")
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

# Function to scrap jobs data from timesjobs.com
def find_jobs():
    # link of the job search
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=').text

    # parsing the html page that we have received in html_text
    soup = BeautifulSoup(html_text, 'lxml')

    # fetching all jobs from the page
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    # running a loop over all jobs
    for index,job in enumerate(jobs):

        # fetches us published days of job...for example if job was posted 5 days ago, a month ago for few days back
        published_date = job.find('span', class_='sim-posted').span.text

        # Only checking for jobs which were posted recently...hence checking for keyword 'few'
        if 'few' in published_date:

            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
            skills = job.find('span', class_='srp-skills').text.replace(' ', '')
            links = job.header.h2.a['href']

            # Filtering out unfamiliar job skills that we entered at the beginning.
            if unfamiliar_skill not in skills:

                # Saving each job in a separate txt file in a folder named 'posts' within your current working directory
                with open(f'posts/{index}.txt','w') as f:
                    f.write(f"Company name: {company_name.strip()} \n")
                    f.write(f"Required skills: {skills.strip()} \n")
                    f.write(f"More Info: {links} \n")
                print(f'File Saved: {index}')


# Running main function which runs at the beginning and calls other functions.
if __name__ == '__main__':
    while True:
        find_jobs()

        # Putting scrapper to sleep for 10 mins so that it doesn't send too many requests to site.
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait*60)
