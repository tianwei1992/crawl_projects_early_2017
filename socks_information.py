"""
东方数据网获得股票代码，再从百度股票获得股票信息，并保存至文件

"""
import re
from bs4 import BeautifulSoup
import requests
import traceback


def getHTMLText(url, encoding='utf-8'):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = encoding
		return r.text
	except Exception as e:
		print('getHTML失败')
		print(e)


def getStockList(lst, stockURL):
	html = getHTMLText(stockURL, "gb2312")
	soup = BeautifulSoup(html, 'html.parser')
	# print(soup)
	# 目标在a标签的href字段中，所以先找a，再提取其href值
	aTags = soup.find_all('a')
	for aTag in aTags:
		try:
			lst.append(re.findall(r's[hz]\d{6}', aTag.attrs['href'])[0])
		except:
			continue
	print(lst)


def getStockInfo(lst, stockURL, fpath):
	count = 0
	for ele in lst:
		url = stockURL + ele + '.html'
		print(url)
		html = getHTMLText(url)
		try:
			if html == "":
				continue
			soup = BeautifulSoup(html, 'html.parser')
			stockinfo = soup.find_all('div', attrs={"class": "stock-bets"})[0]
			stock_dic = {}
			name = stockinfo.find_all('a', attrs={"class": "bets-name"})[0].text.strip()
			stock_dic.update({'name': name})
			keys = stockinfo.find_all('dt')
			values = stockinfo.find_all('dd')
			for i in range(len(keys)):
				key = keys[i].string
				value = values[i].string
				stock_dic[key] = value
			# print(stock_dic)
			# 合法的mode有：
			# r、rb、r+、rb+、w、wb、w+、wb+、a、ab、a+、ab+
			with open(fpath, 'a+') as f:
				f.write(str(stock_dic) + '\n')
				count += 1
				# print("\r已完成：{:.2f}%".format(count*100/len(lst)),end='')
				print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
		except:
			traceback.print_exc()
			# print('\r已完成：{:.2f}%'.format(count*100/len(lst)),end='')
			print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
			continue


def main():
	stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
	stock_info_url = 'https://gupiao.baidu.com/stock/'
	output_file = 'D://BaiduStockInfo_grace2.txt'
	slist = []
	getStockList(slist, stock_list_url)
	print('slist=',slist)
	getStockInfo(slist, stock_info_url, output_file)

main()