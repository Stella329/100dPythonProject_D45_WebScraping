from bs4 import BeautifulSoup
import requests

# Get HTML file
response = requests.get('https://news.ycombinator.com/news')
HTML = response.text
soup = BeautifulSoup(HTML, 'html.parser')

# # get the first title
# article1 = soup.find(name='span', class_='titleline').find(name='a')
# article1_name = article1.get_text()    ##--> Open source AI is the path forward
# article1_link = article1.get('href')     ## --> https://about.fb.com/news/2024/07/open-source-ai-is-the-path-forward/
# article1_upvote = soup.find(name='span', class_='score').get_text() ## --> 1846 points

# get all titles and info
articleNames =[]
articleLinks =[]
articles = soup.find_all(name='span', class_='titleline')

for item in articles:
    article = item.find(name='a')
    name = article.get_text()
    articleNames.append(name)

    link = article.get('href')
    articleLinks.append(link)
articleUpvotes = [int(score.get_text().split()[0]) for score in soup.find_all(name='span', class_='score')]    ##--turn ['1860 points',..] into [1860,..]


# get the article that has the most upvotes
highest_score = max(articleUpvotes)
index = articleUpvotes.index(highest_score)

a_name = articleNames[index]
a_link = articleLinks[index]
print(a_name, a_link, highest_score, index)
