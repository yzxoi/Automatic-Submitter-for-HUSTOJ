import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
import requests, time, re
from lxml import etree

URL = "http://syzoj.hustoj.com/"
MAIN_SUBMITTER = "STD_USERNAME"
LANGUAGE = "6"
USER_ID = "USER_ID"
PASSWORD = "USER_PASSWORD"

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
	"Cookie": '<STD COOKIE>'
}

vis = {}
prob = []
lk = []
def main():
	print("注意：请先登录syzoj，然后复制cookie，替换掉headers中的cookie")
	print("如若报错，请检查 USER 是否提交过题目（须至少提交一题）")
	print("正在搜索提交记录...")
	tp = 0
	while True:
		if tp==0:
			url = URL + "status.php?problem_id=&user_id=" + MAIN_SUBMITTER + "&language=" + LANGUAGE + "&jresult=4"
		else:
			url = URL + "status.php?problem_id=&user_id=" + MAIN_SUBMITTER + "&language=" + LANGUAGE + "&jresult=4&top=" + str(tp)
		
		response = requests.get(url=url, headers=headers)
		text = response.content.decode("utf-8")
		html = etree.HTML(text)
		links = html.xpath('//*[@id="result-tab"]/tbody/tr/td[1]/b/text()')
		probs = html.xpath('//*[@id="result-tab"]/tbody/tr/td[4]/b/div/a/text()')
		if tp==0:
			fi = 0
		else:
			fi = 1
		for pro in range(fi,len(probs)):
			prob.append(probs[pro])
			lk.append(links[pro])
		if tp==links[-1]:
			break
		tp = links[-1]

	driver = webdriver.Chrome()
	url = URL + "loginpage.php"
	driver.get(url)
	driver.find_element(By.NAME,"user_id").send_keys(USER_ID)
	driver.find_element(By.NAME,"password").send_keys(PASSWORD)
	time.sleep(1)
	driver.find_element(By.NAME,"submit").click()

	for i in prob:
		vis[i] = 0
	
	tp = 0
	while True:
		if tp==0:
			url = URL + "status.php?problem_id=&user_id=" + USER_ID + "&jresult=4"
		else:
			url = URL + "status.php?problem_id=&user_id=" + USER_ID + "&jresult=4&top=" + str(tp)
		driver.get(url)
		time.sleep(1)
		text = driver.page_source
		html = etree.HTML(text)
		done_probs = html.xpath('//*[@id="result-tab"]/tbody/tr/td[4]/b/div/a/text()')
		done_links = html.xpath('//*[@id="result-tab"]/tbody/tr/td[1]/b/text()')
		for i in done_probs:
			vis[i] = 1
		if tp==done_links[-1]:
			break
		tp = done_links[-1]

	print("STD 搜索到的提交记录对应题目：",prob)
	print("USER 未完成的题目：",end='')
	print(list(filter(lambda x: vis[x] == 0, prob)))
	print("USER 未完成的题目数量：",end='')
	print(len(list(filter(lambda x: vis[x] == 0, prob))))

	cnt = 0
	for link in lk:
		if vis[prob[cnt]] == 0:
			driver.get(URL)
			time.sleep(5)
			vis[prob[cnt]] = 1
			url = URL + "showsource.php?id=" + link
			response = requests.get(url=url, headers=headers)
			text = response.content.decode("utf-8")
			html = etree.HTML(text)
			code = html.xpath('//pre/text()')[0]
			url = URL + "submitpage.php?id=" + prob[cnt]
			driver.get(url)
			sel = driver.find_element(By.ID,"language")
			Select(sel).select_by_value(LANGUAGE)
			time.sleep(2)
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
			time.sleep(2)
			driver.find_element(By.ID,"Submit").click()
			time.sleep(5)
		cnt = cnt + 1
		print("目前完成进度: " + str(cnt) + "/" + str(len(lk)))

if __name__ == '__main__':
	main()
