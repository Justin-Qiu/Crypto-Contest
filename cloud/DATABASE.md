# Database Operations

#### 在Ubuntu服务器上安装MySQL
'''
sudo apt-get update
sudo apt-get upgrade
sudo apt-get -f install
sudo apt-get install mysql-server
sudo apt-get isntall mysql-client
sudo apt-get install libmysqlclient-dev
'''

#### 检查是否安装成功
'''
sudo netstat -tap | grep mysql
'''

#### 登录root用户
'''
mysql -u root -p 
'''

#### 添加管理员用户
'''
GRANT ALL ON  *.* TO admin@localhost IDENTIFIED BY '123456';
'''

#### 登录数据库
'''
mysql -u admin -p
'''

#### 建立数据库
'''
CREATE DATABASE img;
'''

#### 使用数据库
'''
use img
'''
或命令行直接输入
'''
mysql -u admin -p img
'''

#### 建立一个名为images的表
'''
create table images(
   id int(11) not null auto_increment,
   image_id varchar(100) not null,
   feature1 varchar(10000) not null ,
   feature2 varchar(10000) not null ,
   dhash varchar(50) not null,
   primary key(id)
)ENGINE=InnoDB DEFAULT
CHARSET=utf8;
'''

#### 添加信息
'''
insert into images(image_id, feature) values(IMAGE_ID, IMAGE_FEATURE_1, IMAGE_FEATURE_2,  IMAGE_DHASH);
'''

#### 查看表内容
'''
select * from images;
'''

