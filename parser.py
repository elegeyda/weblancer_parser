import urllib.request
from bs4 import BeautifulSoup
import csv
 
BASE_URL  = 'https://www.weblancer.net/jobs/'
 
def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()
 
 
def get_page_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = soup.find('div', class_='pagination_box') # страницы
    count = pagination.find_all('a')[-1]
    return int(((count.get('href'))[12:]))
 
 
def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('div', class_='page_content') 
 
    projects = []
 
    for rows in table.find_all('div', class_='row'):
        cols = rows.find_all('div')
 
        projects.append({
                'title': [title.text for title in rows.find_all('h2', class_='title')],
                'categories': [category.text for category in rows.find_all('a', class_='text-muted')],
                'price': [price.text for price in rows.find_all('div', class_='float-right float-sm-none title amount indent-xs-b0')],
                'application': [application.text.strip() for application in rows.find_all('div', class_='float-left float-sm-none text_field')],
            })

    return projects
 
def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Проект', 'Категории', 'Цена', 'Заявки'))
 
        # re.sub(r'[\'\[\]]', string)
        for project in projects:
            writer.writerow((', '.join(project['title']), ', '.join(project['categories']), ', '.join(project['price']), ', '.join(project['application'])))

 
def main():
    page_count = get_page_count(get_html(BASE_URL))
 
    print('Всего найдено страниц %d' % page_count)
 
    projects = []
 
    for page in range(1,page_count):
        print('Парсинг %d%%' % (page / page_count *100) )
        projects.extend(parse(get_html(BASE_URL + '/?page={}'.format(page))))
 
    save(projects, 'projects.csv')
 
   
if __name__ == '__main__':
    main()