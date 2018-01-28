import requests
from bs4 import BeautifulSoup
import bs4


def getHTMLText(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		html = r.text
		return html
	except:
		print('爬取失败')


def fillUnivList(urlst, html):
	# print(html)
	soup = BeautifulSoup(html, 'html.parser')
	# print(soup.prettify())
	trs = soup.find('tbody')
	for tr in trs.children:
		if isinstance(tr, bs4.element.Tag):
			# print(tr)
			tds = tr.find_all('td')
			# print(tds)
			urlst.append([tds[0].string, tds[1].string, tds[2].string])
		# urlst.append([tr.find('td').string,tr.find('td').next_sibling.string,tr.find('td').next_sibling.next_sibling.next_sibling.string])
	return urlst


def printUnivList(ulst, num):
	print('{0:^4}\t{1:{3}^12}\t{2:^10}'.format('排位', '学校', '新生高考成绩', chr(12288)))
	for i in range(0, num):
		# print(ulst[i])
		print('{0:{3}^4}\t{1:{3}^12}\t{2:{3}^10}'.format(ulst[i][0], ulst[i][1], ulst[i][2], chr(12288)))


def main():
	url = 'http://www.zuihaodaxue.com/shengyuanzhiliangpaiming2017.html'
	uinfo = []
	html = getHTMLText(url)
	fillUnivList(uinfo, html)
	printUnivList(uinfo, 10)


main()