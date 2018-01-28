# goods's price comparation in taobao
import re
import requests


def getHTMLText(url):
	r = requests.get(url)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	return r.text


def parsePage(ilt, html):
	# print('html=',html)
	tlt = re.findall(r'"raw_title":".*?"', html)
	plt = re.findall(r'"view_price":"\d*\.\d*"', html)
	for i in range(len(tlt)):
		title = eval(tlt[i].split(":")[-1])
		price = eval(plt[i].split(":")[-1])
		ilt.append([title, price])


def printGoodsList(ilt):
	tpformat = "{0:<4}\t{1:<8}\t{2:<20}"
	print(tpformat.format('序号', '价格', '名称'))
	count = 0
	for pt in ilt:
		count += 1
		print(tpformat.format(count, pt[1], pt[0]))


def main():
	start_url = 'https://s.taobao.com/search?q='
	goods = '书包'
	depth = 2
	infoList = []
	for i in range(depth):
		url = start_url + goods + "&s=" + str(44 * i)
		# print(url)
		html = getHTMLText(url)
		# print(html)
		parsePage(infoList, html)

	printGoodsList(infoList)


main()