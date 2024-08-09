from bs4 import BeautifulSoup #the latest versin of Beautiful Soup
# import lxml  #--if soup = BeautifulSoup(html_doc, 'lxml')

htmlFile = open('website.html', 'r')

# Parsing
soup = BeautifulSoup(htmlFile, 'html.parser')

# Indent HTML file
print(soup.prettify())

# Tap into different parts of the web
print(soup.title) ##return: <title>Angela's Personal Site</title>
print(soup.title.name) ##return the tag name: title --> (for <title> tag)
print(soup.title.string) ##return: Angela's Personal Site

print(soup.a) ##return contents of the first anchor tag
print(soup.li) ##return the first li
print(soup.p) ##return the first paragraph




# Using the tag name + the attribute name --带值

## soup.find(tag_name, otherAttributes) --return the first itme that match the query
heading1 = soup.find(name='h1', id='name')
print(heading1) ##-- <h1 id="name">Angela Yu</h1>

section_heading = soup.find(name='h3', class_='heading')
print(section_heading)   ## <h3 class="heading">Books and Teaching</h3>
print(section_heading.get('class')) ## ['heading']

## soup.find_all(name, otherAttributes)
titleAndYear = soup.find_all(name='div', class_='article-title-description__text') ## <div class="article-title-description__text"><h3 class="title">100) Stand By Me</h3><div class="descriptionWrapper"><p class="description"><p><strong>1986</strong><br/>
for item in titleAndYear:
    title = item.find('h3').get_text()



# Use Unique Selector to find the content: CSS selector, or any other selector (#ID, .class, 'tag') --只带selector

soup.select_one('CSS_selector')   #--return the first matching item
soup.select()   #--return a list: of all matching items

## 组合查找: 某一类下的某个标签中的内容，采用空格隔开（不限个数）：soup.select('.class a')
company_url = soup.select_one(selector='p, a') ##CSS selector = <p> <a> (find the 1st anchor tag sits in the paragraph tag)
headings = soup.select('.heading') ##by .class; -- return a list



# Get ALL of the XX type/contents: using func
# Using the tag name
all_anchor_tags = soup.find_all(name='a')
print(all_anchor_tags) ##return a list: [<a href="https://www.appbrewery.co/">The App Brewery</a>, <a href="https://angelabauer.github.io/cv/hobbies.html">My Hobbies</a>, <a href="https://angelabauer.github.io/cv/contact-me.html">Contact Me</a>]

# Get texts/values
for tag in all_anchor_tags:
    tag.getText() #return: The App Brewery

    #get the href (hyerlink)
    tag.get('href') #return: https://www.appbrewery.co/


htmlFile.close()