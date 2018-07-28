# @Author  : ShiRui

import requests
import os
import re


class CrawlData:

	def queue_sex(self):     # 输入性别

		sex = input("请输入你想要的性别如(女):")
		if sex == '男':

			gender = 1

		else:

			gender = 2

		return gender

	def queue_age(self):       # 输入年龄

		age = int(input("请输入你想要的年龄如(20)："))
		if 21 <= age <= 30:

			startage = 21
			endage = 30

		elif 31 <= age <= 40:

			startage = 31
			endage = 40

		else:

			startage = 0
			endage = 0

		return startage, endage

	def queue_money(self):  # 输入收入

		money = int(input("请输入你想要的工资(如:2000):"))
		if 2000 <= money < 5000:

			salary = 2

		elif 5000 <= money < 10000:

			salary = 3

		elif 10000 <= money <= 20000:

			salary = 4

		elif 20000 <= money:

			salary = 5

		else:

			salary = 0

		return salary

	def queue_height(self):  # 输入身高

		height = int(input("请输入你想要的身高(如:161)："))
		if 151 <= height <= 160:

			startheight = 151
			endheight = 160

		elif 161 <= height <= 170:

			startheight = 161
			endheight = 170

		elif 171 <= height <= 180:

			startheight = 171
			endheight = 180

		elif 181 <= height <= 190:

			startheight = 181
			endheight = 190

		else:

			startheight = 0
			endheight = 0

		return startheight, endheight

	def crawl_data(self):  # 爬取数据

		startage, endage = self.queue_age()  # 下面这些都是接收返回值
		gender = self.queue_sex()
		salary = self.queue_money()
		startheight, endheight = self.queue_height()

		print(startage, endage, gender, salary, startheight, endheight)

		header = {    # 响应头，针对一些网站的反扒

			# 'Host': 'www.lovewzly.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Accept-Encoding': 'gzip, deflate, br',
			# 'Referer': ' http://www.lovewzly.com/jiaoyou.html',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'X-Requested-With': 'XMLHttpRequest',
			'Cookie': 'Hm_lvt_ad61b7e39c2050f6b2b13390d4decf4f = 1532680389;Hm_lpvt_ad61b7e39c2050f6b2b13390d4decf4f = 1532680389',
			'Connection': 'keep-alive',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache'
		}

		for i in range(1, 10):  # 爬取前十页的数据

			url = "http://www.lovewzly.com/api/user/pc/list/search?startage={}&endage={}&gender={}&marry=1&education=40&salary={}&page={}".format(
				startage, endage, gender, salary, i)  # 地址
			html = requests.get(url=url, headers=header)  # 返回响应值

			data = html.json()['data']['list']  # 获取需要数据
			for m in range(len(data)):  # 遍历每个数据

				image_url = data[m]['avatar']  # 照片的地址
				response = requests.get(image_url)  # 请求照片的地址
				name = data[m]['username']  # 照片的名字
				rstr = r"[\/\\\:\*\?\"\<\>\|]"  # 正则避免保存时出现'/'等不必要错误
				name = re.sub(rstr, "_", name)  # 将名字中的/换成_

				if not os.path.exists("info"):  # 如果没有这个info文件夹

					os.mkdir("info")  # 就创建这文件夹

				with open("./info/" + name + ".txt", "w", encoding="UTF-8") as file_info:  # 打开文件夹
					file_info.write('名字：' + name + ', 城市:' + data[m]['city'] + ', 个性签名:' + data[m]['monolog'])  # 把一些需的信息写入

				if response.status_code == 200:  # 如果返回的响应头是200

					if not os.path.exists("images"):  # 如果路径没有这个文件

						os.mkdir("images")  # 创建这个文件

					file_path = ".//images//%s.jpg" % name  # 照片的路径
					if not os.path.exists(file_path):  # 下次筛选的条件如果一样，避免重复照片
						print("正在获取:%s的信息" % data[m]['username'])  # 打印信息
						with open(file_path, "wb") as file:  # 打开照片的路径
							file.write(response.content)  # 把照片存入文件夹

if __name__ == "__main__":

	crawldata = CrawlData()
	crawldata.crawl_data()
