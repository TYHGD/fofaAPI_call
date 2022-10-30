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
		sheet = book.add_worksheet('fofa查询结果')
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


if __name__ == '__main__':
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument('-f', dest='f', type=str, help='查询的fofa语法')
		parser.add_argument('-s', dest='s', type=int, help='查询的数量,默认查询数量为20')
		parser.add_argument('-e', dest='e', help='使用execel保存')
		parser.add_argument('-i', dest='i', help='使用-i进行联合查询')
		args = parser.parse_args()
		if args.f:
			fofa_msg = args.f
		if args.i:
			fofa_msg = (args.f + ' && ' + args.i)
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
