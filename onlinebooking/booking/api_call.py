import pandas as objPnd
import requests
import json
import sys

def apiResponse(type, methodname, params=None):
	
	if type == 'GET':
		getApiResponse(methodname, params)
	elif type == 'POST':
		postApiResponse(methodname, params)
	else:
		print('Please pass correct parameters')

def getApiResponse(methodname, params=None):
	if params != None:
		params = {'business_unit':params}
	print(params)
	serURL = 'http://10.223.126.65/BPCWebApi/api/workflow/'+methodname
	print(serURL)
	Result = requests.get(serURL,params)
	if Result.status_code == 200:
		response = Result.text
		print(response)

def postApiResponse(methodname, params):
	serURL = 'http://10.223.126.65/BPCWebApi/api/workflow/'+methodname
	headers = {'content-type': 'application/json; charset=utf-8'}
	Result = requests.post(serURL, data=json.dumps([params]), headers=headers)
	if Result.status_code == 200:
		response = Result.text
		print(response)


if __name__ == '__main__':
	type = sys.argv[1]
	methodname = sys.argv[2]
	if len(sys.argv) >= 4:
		params = sys.argv[3]
		#print(sys.argv)
		apiResponse(type,methodname,params)
	else:
		params=None
		#print(sys.argv)
apiResponse(type,methodname,params)