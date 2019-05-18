# lianjia-pyspider
use pyspider framework to crawl www.lianjia.com


## 1 安装三方库
```
其中 python==3.6
PyMySQL（必须）
pyspider（必须）
fake-useragent（必须）
```
- 注意安装完pyspider后会有一些它的依赖三方库也是必须的，这里不再列出
```
安装phantomjs，并把phantomjs/bin 加入到系统环境中，具体安装安装phantomjs和pyspider请右转百度或者谷歌，这里不再赘述。
```

## 2 创建mysql的数据库和表以及字段
- 创建数据库
```
create database lianjia charset=utf8;
```

- 创建表以及字段
```
CREATE TABLE `home_house` (
  `house_id` varchar(255) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `house_price` varchar(255) DEFAULT NULL,
  `house_area` varchar(255) DEFAULT NULL,
  `house_type` varchar(255) DEFAULT NULL,
  `house_floor` varchar(255) DEFAULT NULL,
  `house_diretion` varchar(255) DEFAULT NULL,
  `house_describle` varchar(255) DEFAULT NULL,
  `house_address` varchar(255) DEFAULT NULL,
  `house_man_name` varchar(255) DEFAULT NULL,
  `house_man_number` varchar(255) DEFAULT NULL,
  `house_province` varchar(255) DEFAULT NULL,
  `house_city` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`house_id`),
  KEY `house_id` (`house_id`),
  KEY `house_provice` (`house_province`),
  KEY `house_city` (`house_city`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 |

```
```
CREATE TABLE `home_picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pic` varchar(255) DEFAULT NULL,
  `house_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8;
```

## 3 启动pypider
```
1:
mac$ pyspider all
```
```
2:
浏览器打开
http://127.0.0.1:5000
```
```
3:
复制lianjia.py的代码到右侧区域
```
```
4:
返回pyspider首页，将lianjia项目的status由TODO改为RUNNING
```

## 4 成果图片展示
![爬取结果部分展示](https://github.com/xjblszyy/lianjia-pyspider/blob/master/result_images/01.png)
![数据库数据展示](https://github.com/xjblszyy/lianjia-pyspider/blob/master/result_images/02.png)
![数据库数据展示](https://github.com/xjblszyy/lianjia-pyspider/blob/master/result_images/03.png)

## 5 TODO
```
用docker部署项目
```
