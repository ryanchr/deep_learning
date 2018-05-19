#coding=utf-8
#-*- coding: utf-8 -*-

import re
import sys
import json
import requests
import io
import random
import traceback

from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

webSiteName = ""
load = {
'from' : '/bbs/' + webSiteName + '/index.html',
'yes' : 'yes'
}


rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
FILENAME=""


##given a board name, count links for the board
def pageCount(webSiteName):
    res = rs.get('https://www.ptt.cc/bbs/'+webSiteName+'/index.html', verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    allPageURL = soup.select('.btn.wide')[1]['href']
    allPage = int(getPageNum(allPageURL)) + 1
    return allPage 


def crawler(webSiteName, parsingPage):
    allPage = pageCount(webSiteName)
    gId = 0
    
    for num in range(allPage, allPage-int(parsingPage), -1):
        ## print("pagenum: ",num)
        res = rs.get('https://www.ptt.cc/bbs/'+webSiteName+'/index'+str(num)+'.html',verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        for tag in soup.select('div.title'):
            ## print(tag)
            try:
                atag = tag.find('a')
                time = random.uniform(0,1)/5
                sleep(time)
                if(atag):
                    URL = atag['href']
                    link = 'https://www.ptt.cc' + URL
                    ## print(link)

                    gId = gId + 1
                    parseGos(link, gId)
            except Exception  as ex:
                print(traceback.format_exc())
		print('error:' + URL) 
                ## print ex
                ## break


def parseGos(link, gId):
    res = rs.get(link, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    #author
    author = soup.select('.article-meta-value')[0].text
    ##print ('author: ' + author)
    #title
    title = soup.select('.article-meta-value')[2].text
    ##print ('title: ' + title)
    #date
    date = soup.select('.article-meta-value')[3].text
    ##print 'date:', date
    #ip
    try:
        targetIP = u'※ 發信站: 批踢踢實業坊'
        ##print soup.text
        ip = soup.find(string = re.compile(targetIP))
        # print("ip: " + ip)
        ip = re.search(r"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*", ip).group()
    except Exception as ex:
        ##print ex
        print(traceback.format_exc())
        ip = "ip is not found"
    
    #
    content = soup.find(id = "main-content").text
    target_content = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
    content = content.split(target_content)
    content = content[0].split(date)
    main_content = content[1].replace('\n', ' ').replace('\t', ' ')

    num, g, b, n, message = 0,0,0,0,{}
    for tag in soup.select('div.push'):
        num += 1
        push_tag = tag.find("span", {'class': 'push-tag'}).text
        push_userid = tag.find("span", {'class': 'push-userid'}).text
        push_content = tag.find("span", {'class': 'push-content'}).text
        push_content = push_content[1:]

        push_ipdatetime = tag.find("span", {'class': 'push-ipdatetime'}).text
	push_ipdatetiem = remove(push_ipdatetime, '\n')

        message[num]={"狀態":push_tag.encode('utf-8'),"留言者":push_userid.encode('utf-8'), "留言內容":push_content.encode('utf-8'),"留言時間":push_ipdatetime.encode('utf-8')}

        if push_tag == u'推 ':
	    g += 1
	elif push_tag == u'噓 ':
	    b += 1
	else: 
	    n += 1

    messageNum = {"g":g, "b":b, "n":n, "all":num}

    d={ "a_ID":gId , "b_作者":author.encode('utf-8'), "c_標題":title.encode('utf-8'), "d_日期":date.encode('utf-8'), "e_ip":ip.encode('utf-8'), "f_內文":main_content.encode('utf-8'), "g_推文":message,"h_推文總數":messageNum} 

    json_data = json.dumps(d, ensure_ascii=False, indent=4, sort_keys=True)+','
    store(json_data)


def store(data):
    with open(FILENAME, 'a') as f:
        f.write(data)


def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value.rstrip()


def getPageNum(content):
    startIdx = content.find('index')
    endIdx = content.find('.html')
    pageNum = content[startIdx + 5: endIdx]
    return pageNum


if __name__ == "__main__":
    webSiteName = str(sys.argv[1])
    parsingPage = int(sys.argv[2])
    FILENAME = 'data-'+webSiteName+'-'+datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.json'
    store('[')
    print 'Start parsing [', webSiteName, ']...'
    crawler(webSiteName, parsingPage)
    store(']')


    with open(FILENAME, 'r') as f:
        p = f.read()
    with open(FILENAME, 'w') as f:
        f.write(p[:-2]+']')
