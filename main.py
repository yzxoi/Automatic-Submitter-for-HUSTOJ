import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
import requests, time, re
from lxml import etree

URL = "http://syzoj.hustoj.com/"
MAIN_SUBMITTER = "std"
LANGUAGE = "6"
USER_ID = "spider"
PASSWORD = "spider123456"

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
	"Cookie": "<cookie>"
}


vis = {}
def main():
	url = URL + "status.php?problem_id=&user_id=" + MAIN_SUBMITTER + "&language=" + LANGUAGE + "&jresult=4"
	response = requests.get(url=url, headers=headers)
	text = response.content.decode("utf-8")
	html = etree.HTML(text)
	links = html.xpath('//*[@id="result-tab"]/tbody/tr/td[1]/b/text()')
	probs = html.xpath('//*[@id="result-tab"]/tbody/tr/td[4]/b/div/a/text()')

	print("搜索到的提交记录对应题目：",end='')
	print(probs)
	
	driver = webdriver.Chrome()
	url = URL + "loginpage.php"
	driver.get(url)
	driver.find_element(By.NAME,"user_id").send_keys(USER_ID)
	driver.find_element(By.NAME,"password").send_keys(PASSWORD)
	time.sleep(1)
	driver.find_element(By.NAME,"submit").click()

	for i in probs:
		vis[i] = 0

	cnt = 0
	for link in links:
		if vis[probs[cnt]] == 0:
			vis[probs[cnt]] = 1
			url = URL + "showsource.php?id=" + link
			response = requests.get(url=url, headers=headers)
			text = response.content.decode("utf-8")
			html = etree.HTML(text)
			code = html.xpath('//pre/text()')[0]
			url = URL + "submitpage.php?id=" + probs[cnt]
			driver.get(url)
			sel = driver.find_element(By.ID,"language")
			Select(sel).select_by_value(LANGUAGE)
			time.sleep(1)
			t= ""
			for j in range(0,len(code)): # 转义字符问题
				if ord(code[j])==10:
					t += "\\n"
				elif ord(code[j])==13:
					t+="\\t"
				elif code[j]=="'":
					t+="\\\'"
				elif code[j]=="/" and code[j+1]=='*':
					break # 去掉注释
				else:
					t+=code[j]
			stri = "editor.setValue('" + str(t) + "')"
			driver.execute_script(stri)
			time.sleep(1)
			driver.find_element(By.ID,"Submit").click()
			time.sleep(10)
		cnt = cnt + 1
		print("cur progress: " + str(cnt) + "/" + str(len(links)))

if __name__ == '__main__':
	main()
