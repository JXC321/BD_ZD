import requests
import re
from bs4 import BeautifulSoup
import time

url_1 = "https://zhidao.baidu.com/search?word="
url_2 = "&ie=gbk&site=-1&sites=0&date=0&pn="
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

def Get_html(keyword, number = 0):
    #输入关键字，获取得到结果的数量和源码
    url = url_1 + keyword + url_2 + str(number)
    print(url)
    res = requests.get(url = url, headers = header)
    res.encoding = 'gbk'
    html = res.text
    if number == 0:
        reg = r'<a class="pager-last".+?pn=(.+?)">尾页</a>'
        reg = re.compile(reg)
        number = re.findall(reg,html)[0]
        return [html,number]
    else:
        return html

def Get_URL(html):
    #从html源码中解析出url并返回
    Soup = BeautifulSoup(html,'lxml')
    info = Soup.select('.list-inner')
    info = info[0].select('.ti')
    return [i['href'] for i in info]

def Get_info(url):
    #进入详情页获取问题和答案
    res = requests.get(url, headers = header)
    res.encoding = 'gbk'
    Soup = BeautifulSoup(res.text,'lxml')
    
    try:
        info = Soup.select('pre[accuse="aContent"]')
        if len(info) < 1:
            print(url)
            info = Soup.select('div[accuse="aContent"]')
            if len(info) < 1:
                info = Soup.select('dt[class="title"]')

        info = info[0].text
    except:
        info = ''
        print('获取回答失败,对应的URL为:',url)
    try:
        ask = Soup.select('.ask-title ')
        if len(ask) < 1:
            ask = Soup.select('.qb-content')

        ask = ask[0].text
    except:
        ask = ''
        print('获取标题失败，对应的URL为:',url)
    
    return ask,info

if __name__ == '__main__':
    keyword = '标书'
    
    [html,number] = Get_html(keyword)
    URL = Get_URL(html)
    for u in URL:
        #print(u)
        [ask,answer] = Get_info(u)
        with open('记录.txt','a',encoding='utf-8') as f:
            f.write(ask+"\n"+answer+"\n\n")
        time.sleep(1)
    print("首页获取完毕！")
    time.sleep(3)

    for i in range(1,int(number)+1):
        html = Get_html(keyword,i*10)
        URL = Get_URL(html)
        for u in URL:
            #print(u)
            [ask,answer] = Get_info(u)
            with open('记录.txt','a',encoding='utf-8') as f:
                f.write(ask+"\n"+answer+"\n\n")
                f.close()
            time.sleep(1)
        print("第" + str(i+1) + "页获取完毕！")
        time.sleep(3)
