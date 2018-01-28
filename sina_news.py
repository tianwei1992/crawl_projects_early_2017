"""
（1）getNewsDetail（url），实现了从单个新闻url获取7项信息，以字典形式返回。

（2）getPageurls（url），实现了从1个分页请求url获取多条（这里是22条）新闻链接，以列表形式返回。

说明：新浪新闻-国内新闻页面下方有很多条新闻链接，为了提高页面打开速度，这些链接并不是一开始全部加载，而是鼠标向下滚动到那里，才发送请求获取链接。发送1个请求能够获取22个新闻链接。getPageurls（url）这个函数就是从这1个请求地址获取22个链接。

（3）22条链接显然不够，于是我们需要请求n个分页，获取n*22条链接。每个分页的url只有page参数值不同，因此我们可以使用for循环依次获取，首先指定url模板，然后在在每次循环内构造当页的url并调用getPageurls（url），将结果用list.extend方法加入总列表，也就是urllist。

（4）对urllist中的每个url依次调用getNewsDetail（url），将结果用append追加到total_list=[]中。total_list就是所有的成果。后面用pandas处理。
"""
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import pandas

def get_page_urls(start_url):
	res=requests.get(start_url)
	urlstrip=res.text.lstrip('  newsloadercallback(').rstrip(');')
	jd=json.loads(urlstrip)
	page_urls=[]
	for ele in jd['result']['data']:
		page_urls.append(ele['url'])
	#print(page_urls)
	return page_urls

"""
urlMod = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1510043690292'
urllst = []
for i in range(1, 3):
	# print(i)
	eleurl = urlMod.format(i)
	# print(eleurl)
	# print(getPageurls(eleurl))
	urllst.extend(getPageurls(eleurl))
print(urllst)
print(len(urllst))

"""


def getNewsDetail(newsurl):
    #newsurl='http://news.sina.com.cn/c/nd/2017-11-05/doc-ifynmnae1934564.shtml'
    res=requests.get(newsurl)
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    title=soup.select('#artibodyTitle')[0].text
    editor=soup.select('.article-editor')[0].text.strip('责任编辑：')
    body=soup.select('#artibody p')
    #print(articles)
    timeorig=soup.select('.time-source')[0].contents[0].strip()
    #print(timeorig)
    dt=datetime.strptime(timeorig,'%Y年%m月%d日%H:%M')
    newssource=body[-2:-1][0].text.strip().strip('来源：')
    source =soup.select('.time-source')[0].contents[1].text.strip()
    article=' '.join([p.text.strip() for p in body[:-2]])
    #str1=newsurl.rstrip('.shtml').lstrip('http://news.sina.com.cn/c/nd/.*/doc')
    #str1 can be calculated in 2 ways
    str1=newsurl.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
   # m=re.search('doc-i(.*).shtml',newsurl)
    #str1=m.group(1)
    #print('str1:',str1)
    general_url='http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&'
    commenturl=general_url.format(str1)
    #print('commenturl:',commenturl)
    res=requests.get(commenturl)
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text,"html.parser")
    jd=json.loads(soup.text.strip('var data='))
    #print('1 title:',title)
    #print('2 editor:',editor)
    #print('3 dt:',dt)
    #print('4 newssource:',newssource)
    #print('5 source:',source)
    #print('6 commoncount:',jd['result']['count']['qreply'])
    #print('7 article:',article)
    data={}
    data['1title']=title
    data['2editor']=editor
    data['3dt']=dt
    data['4newssource']=newssource
    data['5source']=source
    data['6commoncount']=jd['result']['count']['qreply']
    data['7article']=article
    return data



def get_url_lst():
	urlMod = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1510043690292'
	urllst = []
	for i in range(1, 3):
		eleurl = urlMod.format(i)
		urllst.extend(get_page_urls(eleurl))
	print(urllst)
	return urllst

def main():
	urllst=get_url_lst()
	total_list = []
	for ele in urllst:
		#print(ele)
		total_list.append(getNewsDetail(ele))
		#print(len(total_list))
	df = pandas.DataFrame(total_list)
	print(df.head(6))
	df.to_excel('total_list.xlsx')


if __name__=='__main__':
	main()
