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
fofa_url = config.get('配置信息', 'fofa_url')
email = config.get('配置信息', 'email')
key = config.get('配置信息', 'key')


def excel(name, fofa_):
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


def fofa_api(msg, quantity):
	herders = {
		'email': email,
		'key': key,
		'qbase64': base64.b64encode(msg.encode()),
		'size': str(quantity)
	}
	resp = requests.get(fofa_url, data=herders)
	return resp.json()['results']


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', dest='f', type=str, help='查询的fofa语法')
	parser.add_argument('-s', dest='s', type=int, help='查询的数量,默认查询数量为20')
	parser.add_argument('-e', dest='e', help='使用execel保存')
	args = parser.parse_args()
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
