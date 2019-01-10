# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import xml.etree.ElementTree as ET
import requests

# Create your views here.
def allview(request):
	return render(request,"booking/index.html",{})



def ticket_view(request):
	print "Api call view"

	try:
		# response = requests.get("https://ws.test.acprailinternational.com/")
		# response = requests.get("https://ws.test.acprailinternational.com/method=ACP_authenticateRQ")
		print ("response")
	except Exception, e:
		print "got Exception"
		raise e

	
	return render(request,"booking/tickets.html",{})

def traveller_info(request):
	return render(request,"booking/traveller-information.html",{})

def api_call(request):	

	# xml = """<?xml version='1.0' encoding='utf-8'?>
	# <a>б</a>"""

	xml = """
		<?xml version="1.0" encoding="UTF-8"?>
		<ACP_RailAvailRQ xmlns="http://www.acprailinternational.com/API/R2" ResponseType="Native-Availability">
	  		<POS>
	    		<RequestorID>RTG-XML</RequestorID>
	  		</POS>
  			<RailAvailInfo>
    			<OriginDestinationSpecifications>
	      			<OriginLocation LocationCode="7000123"/>
	      			<DestinationLocation LocationCode="7000008"/>
	      			<Departure DepartureDate="2017-06-16T09:15:00"/>
    			</OriginDestinationSpecifications>
    			<PassengerSpecifications>
      				<PassengerType Age="-1" Quantity="3"/>
    			</PassengerSpecifications>
    			<FareQualifier RateCategory="Regular"/>
    				<ResponsePtPTypes>
      					<ResponsePtPType>TW</ResponsePtPType>
    				</ResponsePtPTypes>
  			</RailAvailInfo>
		</ACP_RailAvailRQ>
	"""


	# headers = {'Content-Type': 'application/xml'} # set what your server accepts
	# print requests.post('http://httpbin.org/post', data=xml, headers=headers).text


	serURL = 'http://www.acprailinternational.com/API/R2'
	headers = {'content-type': 'application/xml; charset=utf-8'}
	print "Before request"
	Result = requests.post(serURL, data=xml, headers=headers)
	if Result.status_code == 200:
		response = Result.text
		print response
	else:
		print "Status code error", Result.status_code
	print "After request"
	print "Response is ---->",Result
	return "API VIEW"



