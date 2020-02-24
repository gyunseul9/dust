'''
use mysql
create database DB_NAME default character set utf8;
create user 'DB_NAME'@'localhost' identified by 'PASSWORD';
create user 'DB_NAME'@'127.0.0.1' identified by 'PASSWORD';
grant all privileges on DB_NAME.* to 'USER_ID'@'localhost';
grant all privileges on DB_NAME.* to 'USER_ID'@'127.0.0.1';
flush privileges;
quit;

CREATE TABLE dust (
  num int(11) NOT NULL AUTO_INCREMENT,
  seq varchar(50) NOT NULL,
  src varchar(50) NOT NULL,
  mdate varchar(100) NOT NULL,
  area01 varchar(255) NOT NULL,
  area02 varchar(255) NOT NULL,
  so2 varchar(255) NOT NULL,
  co text NOT NULL,
  o3 varchar(255) NOT NULL,
  no2 varchar(255) NOT NULL,
  pm10 varchar(255) NOT NULL,
  pm25 varchar(255) NOT NULL,
  posted datetime DEFAULT NOW(),
  primary key (num)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
END'''

class Configuration:

  def get_configuration(choose):

    if(choose == 'local'):
      connect_value = dict(host='HOST_NAME',
        user='USER_ID',
        password='PASSWORD',
        database='DB_NAME',
        port=3307,
        charset='utf8')
      
    elif(choose == 'ubuntu'):
      connect_value = dict(host='HOST_NAME',
        user='USER_ID',
        password='PASSWORD',
        database='DB_NAME',
        port=3307,
        charset='utf8')

    else:
      print('Not Selected')
      connect_value = ''

    return connect_value
  


