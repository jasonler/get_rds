'''
Created by auto_sdk on 2015.06.23
'''
from aliyun.api.base import RestApi
class Mts20140618SubmitMetaInfoJobRequest(RestApi):
	def __init__(self,domain='mts.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.Input = None
		self.UserData = None

	def getapiname(self):
		return 'mts.aliyuncs.com.SubmitMetaInfoJob.2014-06-18'
