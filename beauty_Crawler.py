import requests
import urllib.parse
import re
from bs4 import BeautifulSoup


INDEX = 'https://www.ptt.cc/bbs/beauty/index2000.html'
NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

def get_posts_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    posts = list()
    popular = list()
    for article in soup.find_all('div', 'r-ent'):
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        if meta.get('href') != None:
            if not re.search('\[公告\]', meta.getText().strip()):
            
                posts.append({
                    'title': meta.getText().strip(),
                    'link': meta.get('href'),
                    'date': article.find('div', 'date').getText(),
                    'push': article.find('div', 'nrec').getText(),
                })
    #next page
    next_link = soup.find('div', 'btn-group-paging').find_all('a', 'btn')[2].get('href')
    
    return posts, next_link

def get_pages(num):
    #網址
    page_url = INDEX 
    all_posts = list()
    for i in range(num):
        posts, link = get_posts_on_page(page_url)
        if page_url == 'https://www.ptt.cc/bbs/beauty/index2000.html':
            for j in range(0,13):
                posts.pop(0)
        
        all_posts += posts
        page_url = urllib.parse.urljoin(INDEX, link)

    for k in range(0,6):
        del all_posts[-1]
        
    return all_posts



# if __name__ == '__main__':
#     pages = 353
#     with open('all_articles.txt', 'w', encoding = 'utf8') as f:
#         with open('all_popular.txt', 'w', encoding = 'utf8') as w:
#             for post in get_pages(pages):
#                 if post['push'] == '爆':
#                     w.write(post['date'].replace('/','').strip()  + ',' + post['title'] + ',' + 'https://www.ptt.cc' + post['link'] + "\n")
#                 #print(post['date'].replace('/','').strip(), post['title'], 'https://www.ptt.cc' + post['link'])
#                 f.write(post['date'].replace('/','').strip()  + ',' + post['title'] + ',' + 'https://www.ptt.cc' + post['link'] + "\n")


def getdate(start_date, end_date):
    push_user = dict()
    boo_user = dict()
    like = 0
    boo = 0
    count = 0 
    #有中文問題要轉換
    f = open('all_articles.txt', 'r', encoding='utf8')

    for line in f.readlines():
        #print(int(line.split(',')[0]))
        if int(line.split(',')[0].strip()) >= start_date and int(line.split(',')[0].strip()) <= end_date :
            #print(type(line.split(',')[0]))
            count = count + 1
            #取得TXT檔中的url
            url = line.split(',')[-1].strip('\n')
            #print(url)
            response = requests.get(url)
            #將原始碼做整理
            soup = BeautifulSoup(response.text, 'lxml')
            #使用find_all()找尋特定目標
            articles = soup.find_all('div', 'push')

            for article in articles:
                #count = count + 1
                if article.find("span", {'class': 'push-userid'}) != None:
                    userId = article.find("span", {'class': 'push-userid'}).text
                    push_tag = article.find("span", {'class': 'push-tag'}).text
                
                    if push_tag == u'推 ':
                        like += 1
                        if not userId in push_user.keys():
                            push_user.update({userId : 1})
                        else:
                            push_user[userId] += 1
                    elif push_tag == u'噓 ':
                        boo += 1
                        if not userId in boo_user.keys():
                            boo_user.update({userId : 1})
                        else:
                            boo_user[userId] += 1

    print('all like: ', like)
    print('all boo: ', boo)
    push_user = sorted(push_user.items(),key = lambda item : item[1], reverse = True)
    boo_user = sorted(boo_user.items(),key = lambda item : item[1], reverse = True)

    key = 0
    num = 0
    for i,j in push_user[0 : 10]:
        key += 1
        print('like #' + str(key) + ':', i, j)
    
    for i,j in boo_user[0 : 10]:
        num += 1
        print('boo #' + str(num) + ':', i, j)

    print(count)
    f.close()

#getdate(101, 1231)

#
def popularLinks(start_date, end_date):
    count_popular = 0
    popular_url = []
    f = open('all_popular.txt', 'r', encoding='utf8')
    for line in f.readlines():  
        
        if int(line.split(',')[0].strip()) >= start_date and int(line.split(',')[0].strip()) <= end_date :
            count_popular += 1
            url = line.split(',')[-1].strip('\n')
            #建立回應
            response = requests.get(url)
            #將原始碼做整理
            soup = BeautifulSoup(response.text, 'lxml')
            #使用find_all()找尋特定目標
            #articles = soup.find_all('div', 'push')
            articles = soup.find(id = 'main-container').find_all('a')
            
            for article in articles:
                if article['href'].endswith('.jpg'):
                    popular_url.append(article['href'])
                    print(article['href'])
                elif article['href'].endswith('.jpeg'):
                    popular_url.append(article['href'])
                    print(article['href'])
                elif article['href'].endswith('.png'):
                    popular_url.append(article['href'])
                    print(article['href'])
                elif article['href'].endswith('.gif'):
                    popular_url.append(article['href'])
                    print(article['href'])

            with open('popular.txt', 'w', encoding='utf8') as f:
                f.write('number of popular articles: ')
                f.write(str(count_popular))
                f.write("\n")
                for i in popular_url:            
                    f.write(i + "\n")

    print('number of popular articles: ', count_popular)
    f.close()

#popularLinks(101, 1231)

def keywords(start_date, end_date):
    f = open('all_articles.txt', 'r', encoding='utf8')
    keywords_url = []
    for line in f.readlines():
        if int(line.split(',')[0].strip())>= start_date and int(line.split(',')[0].strip())<=end_date:
            url = line.split(',')[-1].strip('\n')
            #建立回應
            response = requests.get(url)
            #將原始碼做整理
            soup = BeautifulSoup(response.text, 'lxml')
            #print(soup)
            contents = soup.find(id='main-content').text
            #print(re.match('^https?://(i.)?(m.)?imgur.com', contents))
            #print(contents,end='')
            target_content = u'--'
            #去除掉 target_content i.e. --
            contents = contents.split(target_content)
            #print(contents[0])
            
            if re.search('正妹', contents[0]):
                #print(contents[0])
                #建立回應
                response = requests.get(url)
                #將原始碼做整理
                soup = BeautifulSoup(response.text, 'lxml')
                #使用find_all()找尋特定目標
                articles = soup.find(id = 'main-container').find_all('a')
                #with open('keywords.txt', 'w', encoding='utf8') as f:
                for article in articles:
                    if article['href'].endswith('.jpg'):
                        keywords_url.append(article['href'])
                        print(article['href'])
                    elif article['href'].endswith('.jpeg'):
                        keywords_url.append(article['href'])
                        print(article['href'])
                    elif article['href'].endswith('.png'):
                        keywords_url.append(article['href'])
                        print(article['href'])
                    elif article['href'].endswith('.gif'):
                        keywords_url.append(article['href'])
                        print(article['href'])
    print('Complete !')
    print(keywords_url)
    with open('keywords.txt', 'w', encoding='utf8') as f:
        for url in keywords_url:
            f.write(url + '\n')
        f.close()
    #f.close()
keywords(701, 801)