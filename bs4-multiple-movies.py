import re
from bs4 import BeautifulSoup
import requests

# Extracting links from pagination bar

# How To Get The HTML
root = 'https://subslikescript.com'
website = f'{root}/movies_letter-X'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

# Locate the box that contains the pagination bar
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

# Extracting the links of multiple movie transcripts inside each page listed

# Loop through all the pages and send a request to each link
for page in range(1, int(last_page) + 1):
    result = requests.get(f'{website}?page={page}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # Locate the box that contains a list of movies
    box = soup.find('article', class_='main-article')

    # Store each link in the "links" list
    links = [link['href'] for link in box.find_all('a', href=True)]

    # Extracting the movie transcript
    for link in links:
        try:
            result = requests.get(f'{root}/{link}')
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            # Locate the box that contains title and transcript
            box = soup.find('article', class_='main-article')
            # Locate title and transcript
            title = box.find('h1').get_text()
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

            # Sanitize the title for use as a file name
            sanitized_title = re.sub(r'[\/:*?"<>|]', '', title)

            # Export data to a text file with the sanitized "title" name
            with open(f'{sanitized_title}.txt', 'w', encoding='utf-8') as file:
                file.write(transcript)
        except Exception as e:
            print('------ Link not working -------')
            print(link)
            print('Error:', str(e))
