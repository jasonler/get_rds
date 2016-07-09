#get_rds.py

Overview

本程序采用python 2.6编写，用于下载阿里云MysQL数据库的RDS备份文件。
配合crontab可以实现阿里云数据库备份文件的自动下载。
不足之处欢迎大家交流，改进。

本程序在CentOS 6.5/python2.6.6/python2.7.11下都可以正常工作。

July 9, 2016


一）概 述

1.1）基础功能
* 这个程序的基础功能是下载RDS数据库的备份文件，当然也可以是其它文件。
* 程序启动后，读取当前时间到24小时以前阿里云RDS的备份文件列表并下载。
  适合每天定期自动运行。参见第51行代码：
  dstart = dnow - timedelta(hours=24)
  这里的24就是回溯的小时，当然你可以根据你的应用场景修改，比如1周1次备份，则计划运行的时间必需能够回溯到这个备份时间。
* 手动下载时，屏幕上可以显示下载的进度。
* 程序运行结束后会写日志，日志的路径与备份文件下载的路径一致。
  日志中记录下载的文件名称以及时间。
* 程序运行结束后会在备份文件下载的路径写一个文件rds.swap，里面只记录下载的备份文件名。
  后续做线下主机自动恢复数据时，需要用到当前下载的文件名，可以从日志中提取，也可以从rds.swap文件提取。
  显然后者简单，大大简化了自动恢复脚本的编写和调试。


1.2）适用的场合
一般RDS应用都是每天做1次全量备份。编写这个程序也是适用每天定期下载1个备份。
如果你的应用1天多次备份或者1周1次备份，也可以使用get_rds.py下载，不过要调整回溯的时间。


1.3）应用方法（前提是，线修改为你自己的RDS参数）
* 手动下载，在get_rds.py所在的目录执行：
  $ python get_rds.py

* 自动下载，确保你定义的时间RDS备份已经完成，最好多处半小时的富裕时间。
  $ crontab -e
  0 6 * * * /usr/bin/python /export/xtrabackup/get_rds.py


1.4）注意事项
* 下载的路径要有写的权限
* 版本，pyhton 2.6.6以及2.7.11下都可以运行。3.x没测试。
* crontab设置时，必需是get_rds.py的全路径。
* 当处于正常部署（自动运行）时，手动执行很可能会覆盖刚刚下载的备份文件，尤其对于文件大且网速慢时手动执行更要谨慎。





二）适应性修改说明

在源代码get_rds.py中，根据你的应用，主要修改如下几处

2.1）阿里云RDS的参数
这个不言而喻，你订购的RDS有自己的参数，替换即可

第34行
aliyun.setDefaultAppInfo("your ACCESSKEYID of rds", "your ACCESSKEYSECRET of rds")
替换为你自己的ACCESSKEYID，ACCESSKEYSECRET

第44行
my_rdsname = "your instance name"
替换为你自己的rds实例名，每个MySQL实例有不同的名字，注意：一定是你产生了备份文件的那个实例哟。

第45行
my_diqu = "cn-beijing" # It should be your location of rds
替换为你的rds所在的实际地区，做好人做到底，这里是阿里云数据中心的一些名称，问问你的客服确认一下。
cn-hangzhou
cn-qingdao
cn-beijing
cn-hongkong
cn-shenzhen
分别是： 
杭州数据中心
青岛数据中心
北京数据中心
香港数据中心
深圳数据中心



2.2）运行环境的参数

第33行
BackUpPath='/export/data/ali-rds/'
BackUpPath变量是备份文件下载的路径，替换为你的主机设定的路径即可
这个路径下，除了保存备份文件，还有日志文件（get_rds.log）和文件名交换文件（rds.swap）

