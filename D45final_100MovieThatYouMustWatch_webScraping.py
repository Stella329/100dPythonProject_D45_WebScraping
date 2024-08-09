from bs4 import BeautifulSoup
import requests

URL = 'https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/'

response = requests.get(URL)
HTML = response.text
soup = BeautifulSoup(HTML, 'html.parser')

# Scraping titles
title_list = []

# titles = soup.find_all(name='h3', class_='title') ##--title only
titleAndYear = soup.find_all(name='div', class_='article-title-description__text')
for item in titleAndYear:     ## <div class="article-title-description__text"><h3 class="title">100) Stand By Me</h3><div class="descriptionWrapper"><p class="description"><p><strong>1986</strong><br/>
    title = item.find('h3').get_text()
    try:
        year = item.find(name='strong').get_text()
    except AttributeError:  ##不一定抓得到year
        pass
    else:
        title = title + ' --' + year

    title_list.append(title)

movie_list = title_list[::-1] ## reverse -->  ['1) The Godfather--1972', '2) The Empire Strikes Back',...]


# Write titles in a txt file:
with open ('D45final_MoiveNames.txt', mode='w', encoding="ISO-8859-1") as txt:
    for movie in movie_list:
        txt.write(f'{movie} \n')
# print(request.encoding) ##-->ISO-8859-1
##the encoding of the web page is actually utf-8, but requests thinks it's ISO-8859-1 for some reason.
##So your fix worked because requests encoded it to Python strings incorrectly, then you decoded it using the same "wrong" algorithm,
# which reverses the error, which then gets interpreted as UTF-8 output by default anyway.
## The better fix is to make requests use the right encoding so you are not doing the "two rights make a wrong" solution.


