
# -*- coding: utf-8 -*- 

import os, glob
import requests
import time
import datetime
import sys
from config import Configuration
from db import DBConnection,Query
from xml.etree import ElementTree as et
from time import sleep

class Dust:

	def __init__(self,area,platform):
		#print('init')
		self.area = area
		self.platform = platform

	def set_params(self):
		#print('set_params')
		self.area = sys.argv[1]
		self.platform = sys.argv[2]

	def validate(self):
		default	= {
			'area':'1',
			'platform':'mac'
		}

		self.area = default.get('area') if self.area == '' else self.area
		self.platform = default.get('platform')	if self.platform == '' else self.platform.lower()

	def table_dust(self,pm25_value):
		if pm25_value == '-':
			result = '-'
		else:
			if int(pm25_value) < 16:
				result = '좋음'
			elif int(pm25_value) > 16 and int(pm25_value) < 36:
				result = '보통'
			elif int(pm25_value) > 36 and int(pm25_value) < 78:
				result = '나쁨'
			elif int(pm25_value) > 78:
				result = '매우나쁨'
			else:
				result = '-'

		return result			

	def api(self):

		#print('crawling')
		self.validate()

		try:
			
			configuration = Configuration.get_configuration(self.platform)
			_host = configuration['host']
			_user = configuration['user']
			_password = configuration['password']
			_database = configuration['database']
			_port = configuration['port']
			_charset = configuration['charset']

			conn = DBConnection(host=_host,
				user=_user,
				password=_password,
				database=_database,
				port=_port,
				charset=_charset)

			data_time = []
			city_name = []
			so2_value = []
			co_value = []
			o3_value = []
			no2_value = []
			pm10_value = []
			pm25_value = []

			url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=SERVICE_KEY'

			#과천시, 광주시, 군포시, 김포시, 남양주시, 수원시, 안성시, 양주시, 양평군, 연천군, 용인시, 의왕시, 파주시, 화성시,
			#location = {'1':['부산','강서구','19'],'2':['경기','안성시','31']}
			'''
			location = {
						'101':['경기','과천시','31'],
						'102':['경기','광주시','31'],
						'103':['경기','군포시','31'],
						'104':['경기','김포시','31'],
						'105':['경기','남양주시','31'],
						'106':['경기','수원시','31'],
						'107':['경기','안성시','31'],
						'108':['경기','양주시','31'],
						'109':['경기','양평군','31'],
						'110':['경기','연천군','31'],
						'111':['경기','용인시','31'],
						'112':['경기','의왕시','31'],
						'113':['경기','파주시','31'],
						'114':['경기','화성시','31']
						}
			'''
			location = {'1':['경기','31'],'2':['강원','17'],'3':['충북','11'],'4':['서울','25'],'5':['부산','16'],'6':['대구','10'],'7':['인천','9'],'8':['광주','5'],'9':['대전','5'],'10':['울산','5'],'11':['충남','15'],'12':['전북','14'],'13':['전남','21'],'14':['경북','14'],'15':['경남','18'],'16':['제주','2'],'17':['세종','1']}

			rows = location[self.area][1]
			sido = location[self.area][0]

			page = '1'
			srch = 'HOUR'

			params = {'numOfRows': rows, 'pageNo': page, 'sidoName': sido, 'searchCondition': srch}

			response = requests.get(url, params=params)

			with open('result.xml','w') as file:
				file.write(response.text)

			tree = et.parse("result.xml")
			root = tree.getroot()

			for response in root:
				for body in response:
					for items in body:
						for item in items:
							if item.tag == 'dataTime':
								#print(item.text)
								data_time.append(item.text)
							elif item.tag == 'cityName':
								#print(item.text)
								city_name.append(item.text)
							elif item.tag == 'so2Value': #아황산가스
								#print(item.text)
								so2_value.append(item.text)
							elif item.tag == 'coValue': #일산화탄소
								#print(item.text)
								co_value.append(item.text)
							elif item.tag == 'o3Value': #오존
								#print(item.text)
								o3_value.append(item.text)
							elif item.tag == 'no2Value': #이산화질소
								#print(item.text)
								no2_value.append(item.text)
							elif item.tag == 'pm10Value': #미세먼지
								#print(item.text)
								pm10_value.append(item.text)
							elif item.tag == 'pm25Value': #미세먼지
								#print(item.text)
								pm25_value.append(item.text)

			print('>',sido)
			print()

			num = len(data_time)

			for i in range(0,num):
				idx = data_time[i].replace('-','')
				idx = idx.replace(':','')
				idx = idx.replace(' ','')		
			
				src = '공공데이터포털'

				print('>',idx,city_name[i])
				print()

				cnt = conn.exec_select_dust(idx,city_name[i])

				if cnt:
					print('overlap seq: ',i,cnt)
				else:	
					print('does not overlap seq: ',i,cnt)

					conn.exec_insert_dust(idx,src,data_time[i],location[self.area][0],city_name[i],so2_value[i],co_value[i],o3_value[i],no2_value[i],pm10_value[i],pm25_value[i])


		except Exception as e:
			with open('./dust.log','a') as file:
				file.write('{} You got an error: {}\n'.format(datetime.datetime.now().strtime('%Y-%m-%d %H:%M:%S'),str(e)))

def run():
	dust = Dust('','')
	dust.set_params()
	dust.api()

if __name__ == "__main__":
	run()
