# -*- coding: utf-8 -*-
'''
Created on 2016-6-28
@author: Jason Le
For security reason, source code keep downloading code in comment status. 
You can remove the comment for the line including "urllib.urlretrieve".

为安全起见，源程序并不开启下载，需手动取消注释: urllib.urlretrieve
'''

import sys,os,shutil,string
import re
import urllib,urllib2
import logging
import time
from  datetime  import timedelta
from  datetime  import datetime
import aliyun.api


# Show the progress of downloading.
def Schedule(a,b,c):
  #a:已经下载的数据块
  #b:数据块的大小
  #c:远程文件的大小
  percentage = 100.0 * a * b / c
  if percentage > 100 :
    percentage = 100
  #print '%.2f%%' % percentage
  sys.stdout.write('%.2f%%\r' % percentage)


BackUpPath='/export/data/ali-rds/'
aliyun.setDefaultAppInfo("your ACCESSKEYID of rds", "your ACCESSKEYSECRET of rds")

logging.basicConfig(level=logging.INFO,
  format='%(asctime)s %(levelname)s %(message)s',
  datefmt='%a, %d %b %Y %H:%M:%S',
  filename=BackUpPath + 'get_rds.log',
  filemode='a')    


#RDS实例名
my_rdsname = "your instance name"
my_diqu = "cn-beijing" # It should be your location of rds


#查询备份文件的信息
#从发当前时间前推24小时，因为一般RDS的自动备份是1天1次
dnow = datetime.now()
dstart = dnow - timedelta(hours=24)
d1 = dstart.strftime("%Y-%m-%dT%H:%MZ")
d2 = dnow.strftime("%Y-%m-%dT%H:%MZ")
#print d1, d2 #just for debug
ali = aliyun.api.Rds20140815DescribeBackupsRequest()
ali.RegionId = my_diqu
ali.DBInstanceid = my_rdsname
ali.StartTime = d1
ali.EndTime =  d2

#每次执行前先清空rds.swap的内容，以便其它脚本判断是否下载成功（空：表示无备份下载）
swapfile=open(BackUpPath+'rds.swap','w')
swapfile.write("")
swapfile.close

#获取备份列表，在现有模式下，1天仅1个全备份
try:
  f = ali.getResponse()
  if("Code" in f):
    print("Fasle")
    print(f["Code"])
    print(f["Message"]) 
  else:
    f = ali.getResponse()
    #print(f)
    f = str(f)

    my_re = re.compile(r"(http://.*?)',")
    my_data = my_re.findall(f)
    my_url = my_data

    my_len = len(my_url) 
    print("\n")
    print "From %r to %r, start download, please wait..." % (ali.StartTime, ali.EndTime)
    print("\n")

    for m in my_url:
      if ( re.search(r".internal.",m) ):
        continue

      res = re.findall(r'hins(.*)\?OSSAccessKeyId',m)
      filename= "hins" + res[0]

      # Generating a file recording the real downloaded file name for further desposal, say auto recovery
      # 虽然你可以从日志文件倒数第2行读出下载的文件名，但提供一个rds.swap记录下载的文件名，还是更方便，简化运维步骤
      if( len(filename)!=4 ):
        swapfile=open(BackUpPath+'rds.swap','w')
        swapfile.write(filename)
        swapfile.close

      curr = time.strftime('%Y-%m-%d %H:%M:%S')
      print "[%r] downloading %r, please wait..." % (curr,filename)
      logging.info('Start downloading: %r'% (filename))

      urllib.urlretrieve(m, BackUpPath+filename, Schedule)
      logging.info('Successfully download: %r'% (filename))
      #break

    endtime = time.strftime('%Y-%m-%d %H:%M:%S')
    dend = datetime.now()
    dtotal = dend-dnow
    print "[%r] downloading over, please check dir[%r]!" % (endtime, BackUpPath)
    logging.info('Task over, using : %r seconds' % (dtotal.seconds))

except Exception,e:
  print(e)
