import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

# job_titles = soup.find_all('h2')

# for job_title in job_titles:
#     print(job_title.text)
jobs = []

# card_content_tags = soup.find_all('div', class_='card-content')

h2_titles = soup.find_all('h2', string=lambda text: "python" in text.lower())

for h2_tag in h2_titles:
    job = h2_tag.parent.parent.parent

    # job_title = job.find('h2')
    job_title = h2_tag.text
    # if job_title:
    #     job_title = job_title.text.strip()
    # if 'python' not in job_title.lower():
    #     continue

    company = job.find('h3', class_='company')
    if company:
        company = company.text.strip()

    location = job.find('p', class_='location')
    if location:
        location_parts = location.text.strip().split(', ')
        city = location_parts[0]
        state = location_parts[1]
        location = location.text.strip()

    date = job.find('time')
    if date:
        date = date.text.strip()

    footer = job.find('footer')
    links = footer.find_all('a')

    link_href = ''
    for link in links:
        if link.text == 'Apply':
            link_href = link['href']

    jobs.append({
        'title': job_title,
        'company': company,
        'city': city,
        'state': state,
        'date_posted': date,
        'apply_link': link_href
    })


# #### PART 2 ####
# # Open each job page and get the description!!

for job in jobs:
    url = job['apply_link']
    if not url:
        continue
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    content_div = soup.find('div', class_='content')

    description_tag = content_div.find('p')
    if not description_tag:
        continue
    description = description_tag.text.strip()

    job['description'] = description


for job in jobs:
    print(f"{job['title']}\n{job['company']} -- {job['city']}, {job['state']}\n{job['description']}\n{job['date_posted']}\nApply here: {job['apply_link']}\n")
