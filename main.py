import time
from bs4 import BeautifulSoup
import requests
import re

print('Put some unfamiliar skills')
unfamiliar_skills = []
unfamiliar_skills.append(input('>'))
more = input("more? y/n: ")
while more == "y":
    unfamiliar_skills.append(input('>'))
    more = input("more? y/n: ")
print(f'Filterin Out {unfamiliar_skills}')

def find_jobs():
    html_text = requests.get('https://wuzzuf.net/search/jobs/?q=python&a=hpb').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_="css-1gatmva e1v1l3u10")
    jobsc = []
    for job in jobs:
        date = job.find('div', class_='css-4c4ojb')
        if not date:
            date = job.find('div', class_='css-do6t5g').text
        else:
            date = date.text
        if int(re.search(r'\d', date).group()) < 30 and not 'month' in date:
            company_name = job.find('a', class_="css-17s97q8").text.replace(' ', '').rstrip('-')
            skills = " ".join([skill.text.strip('· ') for skill in
                               [*job.find_all('a', class_="css-o171kl"), *job.find_all('a', class_="css-5x9pm1")]])
            link = 'https://wuzzuf.net' + job.find('a', class_='css-o171kl', href=True)['href']
            text = f"{company_name},{skills},{date},{link}\n"
            for unfamiliar_skill in unfamiliar_skills:
                if not (unfamiliar_skill.lower() in skills.lower()):
                    no = True
                else:
                    no = False
            if no:
                jobsc.append(text)
    with open('jobs.csv', 'w') as jobs:
        jobs.write('Company Name,Required Skills,Date,Link\n')
        for line in jobsc:
            jobs.write(line)
        print('file saved')

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 60
        print(f'waiting {time_wait} mins')
        time.sleep(time_wait*60)
