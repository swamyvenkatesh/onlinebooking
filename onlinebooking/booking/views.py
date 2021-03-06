# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import xml.etree.ElementTree as ET
import requests
from django.http import HttpResponse
import xmltodict
import json
import ast
import datetime
from xlrd import open_workbook
import os
from django.conf import settings

# Create your views here.
def allview(request):
    return render(request,"booking/index.html",{})



def ticket_view(request):
    originLoc = "Chichester"
    destinationLoc = "Delamere"
    date="30-01-2019"
    presentdate=datetime.datetime.today()    
    # print presentdate
 
    # from xlrd import open_workbook
    #excelpath=settings.STATIC_URL+"media/FE-locations.xlsx"
    wb=open_workbook(os.path.join(settings.MEDIA_ROOT, "FE-locations.xlsx"))
    worksheet = wb.sheet_by_index(0)
    nc = worksheet.ncols
    nr = worksheet.nrows
    ortakes=[]
    desttakes=[]
    fr=[]
    dict1={}
    orgLocCode = 0
    countryCode = 0
    for cr in range(1, nr):
        firstcol=worksheet.cell_value(cr, 1).encode('utf-8')
        if firstcol == originLoc :
            orgLocCode = int(worksheet.cell_value(cr, 0))
            countryCode = int(worksheet.cell_value(cr, 2))            
        if firstcol == destinationLoc :
            destLocCode = int(worksheet.cell_value(cr, 0))
            countryCode = int(worksheet.cell_value(cr, 2))
    # print orgLocCode, destLocCode, "^^^^"

    xml = """
        <?xml version="1.0" encoding="UTF-8"?>
            <ACP_RailAvailRQ xmlns="http://www.acprailinternational.com/API/R2" ResponseType="Native-Availability">
                <POS>
                    <RequestorID>RTG-XML</RequestorID>
                </POS>
                <RailAvailInfo>
                    <OriginDestinationSpecifications>
                        <OriginLocation LocationCode="%d"/>
                        <DestinationLocation LocationCode="%d"/>
                        <Departure DepartureDate="2019-01-30T08:00:00.0Z"/>
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
        """%(orgLocCode, destLocCode)

    serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ'
    headers = {'content-type': 'application/xml; charset=utf-8'}
    print "Before request"
    Result = requests.post(serURL, data=xml, headers=headers)
    if Result.status_code == 200:
        response = Result.text        
        result = xmltodict.parse(response)        
        try:            
            result = ast.literal_eval(json.dumps(result, ensure_ascii=False).encode('utf8'))            
        except:
            pass
        # print "^^^"*40
        # print type(result)
        originLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['OriginLocation']['@Name']
        destinationLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['DestinationLocation']['@Name']                       
        # print "source --",originLocation
        # print "destination --- >", destinationLocation

        journey = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['Journeys']['Journey']

        result_list = []

        for i in journey:
            result_dict = {}

            # print "&&&"*40
            # print i['JourneySegments']['JourneySegment']
            changes = i['JourneySegments']['JourneySegment']
            # print "length of segments", len(changes)
            result_dict['changes'] = len(changes) - 1           

            deptTimeList = []
            arrivalTimeList = [] 
            journeyDetailsList = []           
            for change in changes:
                segment = change['TrainSegment']                
                trainNum = segment['@TrainNumber']
                departDateTime = segment['@DepartureDateTime']
                arrivalDateTime = segment['@ArrivalDateTime']
                departStation = segment['DepartureStation']
                departStationName = departStation['@Name']
                arrivaltStation = segment['ArrivalStation']
                arrivaltStationName = arrivaltStation['@Name']

                depttime = departDateTime.split("T")[-1]
                deptTimeList.append(depttime)

                arrtime = arrivalDateTime.split("T")[-1]
                arrivalTimeList.append(arrtime)
                # print trainNum, departDateTime, arrivalDateTime,departStationName,arrivaltStationName

                journeyDetails = " Train " + trainNum + " Depart "+departStationName+" at "+depttime+" - Arrive "+arrivaltStationName+" at "+ arrtime
                # print "^^^^^^^^^^^^^^^^^^^^^^^^^"
                # print journeyDetails
                journeyDetailsList.append(journeyDetails)
               
            result_dict['departure'] = deptTimeList[0]
            result_dict['arrival'] = arrivalTimeList[-1]
            result_dict['jouney_details'] = journeyDetailsList
            result_list.append(result_dict)
            # break
        print "=============================="
        print result_list,len(result_list),originLocation,destinationLocation
        print "After Successfull request"
        print "Response is ---->",Result

        return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":presentdate, "final_result":result_list})

        # print journey
    else:
        print "Status code error", Result.status_code
        return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":presentdate})
    
    




    
    return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":presentdate})

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
                    <OriginLocation LocationCode="%d"/>
                    <DestinationLocation LocationCode="%d"/>
                    <Departure DepartureDate="2019-01-30T08:00:00.0Z"/>
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
    """%(7000372, 7023060)


    # headers = {'Content-Type': 'application/xml'} # set what your server accepts
    # print requests.post('http://httpbin.org/post', data=xml, headers=headers).text


    # /home/swamy/Documents/python/onlinebooking/booking/views.py

    serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ'
    headers = {'content-type': 'application/xml; charset=utf-8'}
    print "Before request"
    Result = requests.post(serURL, data=xml, headers=headers)
    if Result.status_code == 200:
        response = Result.text
        # with open("/home/swamy/Documents/python/onlinebooking/booking/sample_xml.xml", "w") as dd:
        #     dd.write(str(response))
        # print response
        result = xmltodict.parse(response)        
        # result = json.dumps(result, ensure_ascii=False)
        # print type(result)
        # result = ast.literal_eval(result).encode('utf8')
        try:
            # result = ast.literal_eval(result).encode('utf8')
            result = ast.literal_eval(json.dumps(result, ensure_ascii=False).encode('utf8'))
            
        except:
            pass
        print "^^^"*40
        print type(result)
        # print result
        originLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['OriginLocation']['@Name']
        destinationLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['DestinationLocation']['@Name']
        
        print "$$"*30
        print "From Dictionary"
        print "source --",originLocation
        print "destination --- >", destinationLocation

        journey = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['Journeys']['Journey']

        result_list = []

        for i in journey:
            result_dict = {}

            print "&&&"*40
            # print i['JourneySegments']['JourneySegment']
            changes = i['JourneySegments']['JourneySegment']
            print "length of segments", len(changes)
            result_dict['changes'] = len(changes) - 1           

            deptTimeList = []
            arrivalTimeList = []            
            for change in changes:
                segment = change['TrainSegment']                
                trainNum = segment['@TrainNumber']
                departDateTime = segment['@DepartureDateTime']
                arrivalDateTime = segment['@ArrivalDateTime']
                departStation = segment['DepartureStation']
                departStationName = departStation['@Name']
                arrivaltStation = segment['ArrivalStation']
                arrivaltStationName = arrivaltStation['@Name']

                depttime = departDateTime.split("T")[-1]
                deptTimeList.append(depttime)

                arrtime = arrivalDateTime.split("T")[-1]
                arrivalTimeList.append(arrtime)
                print trainNum, departDateTime, arrivalDateTime,departStationName,arrivaltStationName

                journeyDetails = " Train " + trainNum + " Depart "+departStationName+" at "+depttime+" - Arrive "+arrivaltStationName+" at "+ arrtime
                print "^^^^^^^^^^^^^^^^^^^^^^^^^"
                print journeyDetails

                # print arrtime
                # for key, value in ArrivalStation.items():
                #     print key,value
                # break
                # for key, value in segment.items():
                #     print key,value
                #     trainNum = key['@TrainNumber']
                #     Depart = key['@DepartureDateTime']
                #     Arrival = key['@ArrivalDateTime']
                #     key['DepartureStation']
                #     journeyDetails = "Train" + trainNum + "Depart Chichester at 08:09 - Arrive London Victoria at 09:40" 

            result_dict['departure'] = deptTimeList[0]
            result_dict['arrival'] = arrivalTimeList[-1]
            result_list.append(result_dict)
            break
        print "=============================="
        print result_list
        # print journey
    else:
        print "Status code error", Result.status_code
    print "After request"
    print "Response is ---->",Result
    return HttpResponse("Hi")



