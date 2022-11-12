#!E:\python3\python.exe
# -*-coding:utf-8-*-
import xlsxwriter
import base64
import argparse
import configparser
import os
import requests

path = os.getcwd()
config_path = os.path.join(path, 'config.ini')
config = configparser.ConfigParser()        # 类实例化
config.read(config_path, encoding='utf-8')
fofa_url = config.get('message', 'fofa_url')
email = config.get('message', 'email')
key = config.get('message', 'key')


def excel(name, fofa_):
	try:
		index_ = 1
		book = xlsxwriter.Workbook((name + '.xlsx').strip())
		sheet = book.add_worksheet('one-fox安全团队')
		title = ['url', 'IP', '端口']
		for index, data in enumerate(title):
			sheet.write(0, index, data)
		for i in range(len(fofa_)):
			# print(fofa_[i])
			for ii in range(len(fofa_[i])):
				sheet.write(index_, ii, fofa_[i][ii])
			index_ += 1
		book.close()
	except:
		pass


def fofa_api(msg, quantity):
	try:
		herders = {
			'email': email,
			'key': key,
			'qbase64': base64.b64encode(msg.encode()),
			'size': str(quantity)
		}
		resp = requests.get(fofa_url, data=herders)
		return resp.json()['results']
	except:
		print('查询失败')


def r(a):
	with open(a, mode='r', encoding='utf-8') as f:
		return f.read()


if __name__ == '__main__':
	print("""
  __        __                         _ 
 / _| ___  / _| __ _        __ _ _ __ (_)
| |_ / _ \| |_ / _` |_____ / _` | '_ \| |
|  _| (_) |  _| (_| |_____| (_| | |_) | |
|_|  \___/|_|  \__,_|      \__,_| .__/|_|
                                |_|        
                                            one-fox安全团队""")
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument('-r', dest='r', type=str, help='从文本中读取fofa联合查询语句')
		parser.add_argument('-s', dest='s', type=int, help='查询的数量,默认查询数量为20')
		parser.add_argument('-e', dest='e', help='使用execel保存')
		parser.add_argument('-f', dest='f', help='查询fofa语法')
		args = parser.parse_args()
		if args.r:
			fofa_msg = r(args.r)
		if args.f:
			fofa_msg = args.f
		if args.s:
			quantity = args.s
		else:
			quantity = 20
		if args.e:
			excel_name = args.e
		fofa = fofa_api(fofa_msg, quantity)
		excel(excel_name, fofa)
	except:
		pass
