import pymysql

class DBConnection:
	def __init__(self,host,user,password,database,charset,port):
		self.connection = pymysql.connect(
			host=host,
			user=user,
			password=password,
			db=database,
			charset=charset,
			port=port,
			cursorclass=pymysql.cursors.DictCursor)

	def exec_select_dust(self,seq,area02):
		with self.connection.cursor() as cursor:
			query = Query().get_select_dust(seq,area02)
			cursor.execute(query)
			for row in cursor:
				data = row.get('cnt')
		return data	

	def exec_insert_dust(self,seq,src,mdate,area01,area02,so2,co,o3,no2,pm10,pm25): 
		query = Query().get_insert_dust(seq,src,mdate,area01,area02,so2,co,o3,no2,pm10,pm25) 
		with self.connection as cur:
			cur.execute(query)

	def close(self):
		self.connection.close()

	def commit(self):
		self.connection.commit()

class Query:
	def get_select_dust(self,seq,area02):
		query = 'select \
		count(*) as cnt \
		from dust \
		where seq=\'{}\' and area02=\'{}\''.format(seq,area02)

		return query

	def get_insert_dust(self,seq,src,mdate,area01,area02,so2,co,o3,no2,pm10,pm25):
		query = 'insert into dust (seq,src,mdate,area01,area02,so2,co,o3,no2,pm10,pm25) \
		values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(seq,src,mdate,area01,area02,so2,co,o3,no2,pm10,pm25)

		return query		