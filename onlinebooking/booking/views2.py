# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import xml.etree.ElementTree as ET
import requests
from django.http import HttpResponse
from django.conf import settings
import datetime

# Create your views here.
def allview(request):
    return render(request,"booking/index.html",{})



def ticket_view(request):
    import os
    # import settings
    # print settings.STATIC_URL
    originLoc = "Chichester"
    destinationLoc = "Delamere"
    date="30-01-2019"
    presentdate=datetime.datetime.today()
    #presentdate=list(presentdate.split(",")[2])
    print presentdate
 
    from xlrd import open_workbook
    #excelpath=settings.STATIC_URL+"media/FE-locations.xlsx"
    wb=open_workbook(os.path.join(settings.MEDIA_ROOT, "FE-locations.xlsx"))
    worksheet = wb.sheet_by_index(0)
    nc = worksheet.ncols
    nr = worksheet.nrows
    ortakes=[]
    desttakes=[]
    fr=[]
    dict1={}
    for cr in range(1, nr):
        firstcol=worksheet.cell_value(cr, 1).encode('utf-8')
        if firstcol == originLoc or firstcol == destinationLoc:
            locCode = int(worksheet.cell_value(cr, 0))
            countryCode = int(worksheet.cell_value(cr, 2))
            print locCode, countryCode,"&&&&"



    
    return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":presentdate})

def traveller_info(request):
    return render(request,"booking/traveller-information.html",{})

def api_call(request):  

    # xml = """<?xml version='1.0' encoding='utf-8'?>
    # <a>б</a>"""
    
    xml = """
         <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <ACP_RailAvailRQ ResponseType="Native-Availability" xmlns="http://www.acprailinternational.com/API/R2">
    <POS>
        <RequestorID>RTG-XML</RequestorID>
    </POS>
    <RailAvailInfo Node="Point to Point Tickets">
        <OriginDestinationSpecifications>
            <OriginLocation LocationCode="%d"/>
            <DestinationLocation LocationCode="%d" />
            <Departure DepartureDate="2019-01-30T08:00:00.0Z"/>
        </OriginDestinationSpecifications>
        <PassengerSpecifications>
            <PassengerType Quantity="1" Age="-1"/>
        </PassengerSpecifications>
        <FareQualifier/>
        <ResponsePtPTypes>
            <ResponsePtPType>TR</ResponsePtPType>
        </ResponsePtPTypes>
    </RailAvailInfo>
    </ACP_RailAvailRQ>
    """ % (7000372, 7023060)


    
    # headers = {'Content-Type': 'application/xml'} # set what your server accepts
    # print requests.post('http://httpbin.org/post', data=xml, headers=headers).text


    serURL =  "https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ"
    headers = {'content-type': 'application/xml; charset=utf-8'}
    #print "Before request"
    Result = requests.post(serURL, data=xml, headers=headers)
    if Result.status_code == 200:
        response = Result.text
        #print "$$$$",response
        #print  "===="*30
        #print type(response)
        with open("/home/sunitha/Desktop/sample_xml.xml", "w") as dd:
            dd.write(str(response))
        with open("/home/sunitha/Desktop/sample_xml.xml", "r") as dd:
            import re
            u=[]
            for i in dd:
                i=i.replace("<","")
                i=i.replace(">","")
                #ser=re.findall(r'TrainNumber="(\d+)"',str(i))
                ser=re.findall(r'TrainNumber="(\d+)"','?xml version="1.0" encoding="UTF-8"?><ACP_RailAvailRS ResponseType="Native-Availability" xmlns="http://www.acprailinternational.co    m/API/R2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.acprailinternational.com/API/R2 ACP_RailAvailRS.xsd" Version="1.001" TimeStamp="2019-01-15T04:46:58" Target="Production"><Success/><OriginDestinationOptions><OriginDestinationOption OptionReference="1" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><Journeys><Journey JourneyDuration="PT5H9M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T08:09:00" ArrivalDateTime="2019-01-30T09:40:00" TrainNumber="0809" JourneyDuration="PT1H31M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000246" Name="London Victoria" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T09:40:00" ArrivalDateTime="2019-01-30T10:40:00" TrainNumber="0940" JourneyDuration="PT1H" TrainServiceType="Tube" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000246" Name="London Victoria" Country="GB"/><ArrivalStation LocationCode="7000021" Name="London Euston" Country="GB"/><RailAmenities><RailAmenity Name="Tube segment"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:40:00" ArrivalDateTime="2019-01-30T12:10:00" TrainNumber="1040" JourneyDuration="PT1H30M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000021" Name="London Euston" Country="GB"/><ArrivalStation LocationCode="7000096" Name="Crewe" Country="GB"/><RailAmenities><RailAmenity Name="VT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T12:23:00" ArrivalDateTime="2019-01-30T12:46:00" TrainNumber="1223" JourneyDuration="PT23M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000096" Name="Crewe" Country="GB"/><ArrivalStation LocationCode="7000168" Name="Chester" Country="GB"/><RailAmenities><RailAmenity Name="AW"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T13:02:00" ArrivalDateTime="2019-01-30T13:18:00" TrainNumber="1302" JourneyDuration="PT16M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000168" Name="Chester" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments></Journey><Journey JourneyDuration="PT5H43M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T08:09:00" ArrivalDateTime="2019-01-30T09:40:00" TrainNumber="0809" JourneyDuration="PT1H31M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000246" Name="London Victoria" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T09:40:00" ArrivalDateTime="2019-01-30T10:20:00" TrainNumber="0940" JourneyDuration="PT40M" TrainServiceType="Tube" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000246" Name="London Victoria" Country="GB"/><ArrivalStation LocationCode="7000021" Name="London Euston" Country="GB"/><RailAmenities><RailAmenity Name="Tube segment"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:20:00" ArrivalDateTime="2019-01-30T12:16:00" TrainNumber="1020" JourneyDuration="PT1H56M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000021" Name="London Euston" Country="GB"/><ArrivalStation LocationCode="7000187" Name="Stockport" Country="GB"/><RailAmenities><RailAmenity Name="VT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T12:52:00" ArrivalDateTime="2019-01-30T13:52:00" TrainNumber="1252" JourneyDuration="PT1H" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000187" Name="Stockport" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments></Journey><Journey JourneyDuration="PT5H39M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T08:39:00" ArrivalDateTime="2019-01-30T10:11:00" TrainNumber="0839" JourneyDuration="PT1H32M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000246" Name="London Victoria" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:11:00" ArrivalDateTime="2019-01-30T11:10:00" TrainNumber="1011" JourneyDuration="PT59M" TrainServiceType="Tube" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000246" Name="London Victoria" Country="GB"/><ArrivalStation LocationCode="7000021" Name="London Euston" Country="GB"/><RailAmenities><RailAmenity Name="Tube segment"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T11:10:00" ArrivalDateTime="2019-01-30T13:11:00" TrainNumber="1110" JourneyDuration="PT2H1M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000021" Name="London Euston" Country="GB"/><ArrivalStation LocationCode="7000168" Name="Chester" Country="GB"/><RailAmenities><RailAmenity Name="VT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T14:02:00" ArrivalDateTime="2019-01-30T14:18:00" TrainNumber="1402" JourneyDuration="PT16M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000168" Name="Chester" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments></Journey><Journey JourneyDuration="PT6H45M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T09:07:00" ArrivalDateTime="2019-01-30T10:05:00" TrainNumber="0907" JourneyDuration="PT58M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000087" Name="Southampton" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:17:00" ArrivalDateTime="2019-01-30T14:13:00" TrainNumber="1017" JourneyDuration="PT3H56M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000087" Name="Southampton" Country="GB"/><ArrivalStation LocationCode="7000187" Name="Stockport" Country="GB"/><RailAmenities><RailAmenity Name="XC"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T14:52:00" ArrivalDateTime="2019-01-30T15:52:00" TrainNumber="1452" JourneyDuration="PT1H" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000187" Name="Stockport" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments><FareRPHs><FareRPH>1</FareRPH><FareRPH>2</FareRPH><FareRPH>3</FareRPH><FareRPH>4</FareRPH><FareRPH>5</FareRPH><FareRPH>6</FareRPH><FareRPH>7</FareRPH></FareRPHs></Journey><Journey JourneyDuration="PT5H9M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T09:09:00" ArrivalDateTime="2019-01-30T10:41:00" TrainNumber="0909" JourneyDuration="PT1H32M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000246" Name="London Victoria" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:41:00" ArrivalDateTime="2019-01-30T11:40:00" TrainNumber="1041" JourneyDuration="PT59M" TrainServiceType="Tube" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000246" Name="London Victoria" Country="GB"/><ArrivalStation LocationCode="7000021" Name="London Euston" Country="GB"/><RailAmenities><RailAmenity Name="Tube segment"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T11:40:00" ArrivalDateTime="2019-01-30T13:11:00" TrainNumber="1140" JourneyDuration="PT1H31M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000021" Name="London Euston" Country="GB"/><ArrivalStation LocationCode="7000096" Name="Crewe" Country="GB"/><RailAmenities><RailAmenity Name="VT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T13:23:00" ArrivalDateTime="2019-01-30T13:46:00" TrainNumber="1323" JourneyDuration="PT23M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000096" Name="Crewe" Country="GB"/><ArrivalStation LocationCode="7000168" Name="Chester" Country="GB"/><RailAmenities><RailAmenity Name="AW"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T14:02:00" ArrivalDateTime="2019-01-30T14:18:00" TrainNumber="1402" JourneyDuration="PT16M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000168" Name="Chester" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments></Journey></Journeys></OriginDestinationOption></OriginDestinationOptions><Fares><Fare FareReference="1" Class="Standard" IsEstimated="false" IsPreBookable="false" TicketingTimeLimit="2019-01-14T23:59:59.0Z" TicketCount="1" CurrencyCode="GBP" ItineraryType="One-Way-Outbound" IncludesProtectionPlan="false" ReservationRequired="true" ProductName="TICKET on DEPARTURE &amp; RESERVATION -OFFPEAK via:ANY PERMITTED - Travel is allowed via any permitted route." RouteDescription="ANY PERMITTED - Travel is allowed via any permitted route." FareType="Regular" Magic="ACC074AD31037DDBC262C21EC95AF132')            
                print ser
                i=i.replace('"',"")
                #print i,"{{{{{{"
                #i=i.replace('"',"")
                #u=re.findall(r'UnitPrice\d+\.\d+',str(i))
                #print u,"{{{{{{{{{"
                
                UnitPrice=re.findall(r'UnitPrice=(\d+\.\d+)',str(i))
                # unit_price = re.findall(r'UnitPrice=(\d+\.\d+)',str(dd))
                u.append(UnitPrice)
            print len(u),len(ser)
                #(print (UnitPrice),"{{{{{{{{{{{{"
                #DepartureDateTime=re.findall(r'DepartureDateTime="\d{4}-d{2}-d{2}.d{2}:\d{2}:\d{2}"',str(i))
                #print DepartureDateTime
            # for i in data:
            #     if "TrainNumber" in i:
            #         #print "######"
            #         data1=i.split("TrainNumber=")[1]
            #         traininfo=data1.split("=")[0]
            #         print traininfo,"{{{{{{{{"
            # data=dd.read()
            # if "TrainNumber" in data:
            #     print (data),"{{"

               #detail=[]
            #print data,"{{{{{{"
            
            #if "TrainNumber" in data:
                #print "######"
            #     data1=data.split("TrainNumber=")[1]
            #     traininfo=data1.split("=")[0]
            #     detail.append(traininfo)
            # print detail,"{{{{{{{{{{{"
        return HttpResponse(response)
    else:
        print "Status code error", Result.status_code
    print "After request"
    print "Response is ---->",Result
    # return "API VIEW"
    return HttpResponse("Get API RESPONSE")
def xmltest(request):
    xlm2data='''
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ACP_RailAvailRQ ResponseType="Availability" xmlns="http://www.acprailinternational.com/API/R2">
    <POS>
        <RequestorID>fsalort</RequestorID>
    </POS>
    <RailAvailInfo Node="Point to Point Tickets">
        <OriginDestinationSpecifications>
            <OriginLocation LocationCode="7004380"/>
            <DestinationLocation LocationCode="7000075"/>
            <Departure DepartureDate="2019-01-30T08:00:00"/>
            <Journeys>
                <Journey IsSubComponent="false" JourneyDuration="PT1H46M">
                    <OriginLocation Country="GB" Name="Manchester Piccadilly" LocationCode="7000046"/>
                    <DestinationLocation Country="GB" Name="York" LocationCode="7000075"/>
                    <JourneySegments>
                        <JourneySegment>
                            <TrainSegment OperatorName="ATOC" ReservationMode="Optional" CrossBorder="false" TrainServiceType="Regular" JourneyDuration="PT1H" TrainNumber="0545" ArrivalDateTime="2018-12-27T06:45:00" DepartureDateTime="2018-12-27T05:45:00">
                                <DepartureStation Country="GB" Name="Manchester Piccadilly" LocationCode="7000046"/>
                                <ArrivalStation Country="GB" Name="Leeds" LocationCode="7000041"/>
                                <RailAmenities>
                                    <RailAmenity Name="TRANSPENNINE EXPRESS"/>
                                </RailAmenities>
                                <ClassCodes>
                                    <ClassCode ServiceClass="FIRST"/>
                                    <ClassCode ServiceClass="STANDARD"/>
                                </ClassCodes>
                            </TrainSegment>
                        </JourneySegment>
                        <JourneySegment>
                            <TrainSegment OperatorName="ATOC" ReservationMode="Optional" CrossBorder="false" TrainServiceType="Regular" JourneyDuration="PT23M" TrainNumber="0708" ArrivalDateTime="2018-12-27T07:31:00" DepartureDateTime="2018-12-27T07:08:00">
                                <DepartureStation Country="GB" Name="Leeds" LocationCode="7000041"/>
                                <ArrivalStation Country="GB" Name="York" LocationCode="7000075"/>
                                <RailAmenities>
                                    <RailAmenity Name="LONDON NORTH EASTERN RAILWAY"/>
                                </RailAmenities>
                                <ClassCodes>
                                    <ClassCode ServiceClass="FIRST"/>
                                    <ClassCode ServiceClass="STANDARD"/>
                                </ClassCodes>
                            </TrainSegment>
                        </JourneySegment>
                    </JourneySegments>
                </Journey>
                <Journey IsSubComponent="false" JourneyDuration="PT1H45M">
                    <OriginLocation Country="GB" Name="Manchester Piccadilly" LocationCode="7000046"/>
                    <DestinationLocation Country="GB" Name="York" LocationCode="7000075"/>
                    <JourneySegments>
                        <JourneySegment>
                            <TrainSegment OperatorName="ATOC" ReservationMode="Optional" CrossBorder="false" TrainServiceType="Regular" JourneyDuration="PT1H2M" TrainNumber="0644" ArrivalDateTime="2018-12-27T07:46:00" DepartureDateTime="2018-12-27T06:44:00">
                                <DepartureStation Country="GB" Name="Manchester Piccadilly" LocationCode="7000046"/>
                                <ArrivalStation Country="GB" Name="Leeds" LocationCode="7000041"/>
                                <RailAmenities>
                                    <RailAmenity Name="TRANSPENNINE EXPRESS"/>
                                </RailAmenities>
                                <ClassCodes>
                                    <ClassCode ServiceClass="FIRST"/>
                                    <ClassCode ServiceClass="STANDARD"/>
                                </ClassCodes>
                            </TrainSegment>
                        </JourneySegment>
                        <JourneySegment>
                            <TrainSegment OperatorName="ATOC" ReservationMode="Optional" CrossBorder="false" TrainServiceType="Regular" JourneyDuration="PT22M" TrainNumber="0807" ArrivalDateTime="2018-12-27T08:29:00" DepartureDateTime="2018-12-27T08:07:00">
                                <DepartureStation Country="GB" Name="Leeds" LocationCode="7000041"/>
                                <ArrivalStation Country="GB" Name="York" LocationCode="7000075"/>
                                <RailAmenities>
                                    <RailAmenity Name="CROSSCOUNTRY"/>
                                </RailAmenities>
                                <ClassCodes>
                                    <ClassCode ServiceClass="FIRST"/>
                                    <ClassCode ServiceClass="STANDARD"/>
                                </ClassCodes>
                            </TrainSegment>
                        </JourneySegment>
                    </JourneySegments>
                </Journey>
                <Journey IsSubComponent="false" JourneyDuration="PT1H43M">
                    <OriginLocation Country="GB" Name="Manchester Piccadilly" LocationCode="7000046"/>
                    <DestinationLocation Country="GB" Name="York" LocationCode="7000075"/>
                    <JourneySegments>
                        <JourneySegment>
                            <TrainSegment OperatorName="ATOC" ReservationMode="Optional" CrossBorder="false" TrainServiceType="Regular" JourneyDuration="PT58M" TrainNumber="0747" ArrivalDateTime="2018-12-27T08:45:00" DepartureDateTime="2018-12-27T07:47:00">
                                <DepartureStation Country="GB" Name="Manchester Piccadilly" LocationCode="7000046"/>
                                <ArrivalStation Country="GB" Name="Leeds" LocationCode="7000041"/>
                                <RailAmenities>
                                    <RailAmenity Name="TRANSPENNINE EXPRESS"/>
                                </RailAmenities>
                                <ClassCodes>
                                    <ClassCode ServiceClass="FIRST"/>
                                    <ClassCode ServiceClass="STANDARD"/>
                                </ClassCodes>
                            </TrainSegment>
                        </JourneySegment>
                        <JourneySegment>
                            <TrainSegment OperatorName="ATOC" ReservationMode="Optional" CrossBorder="false" TrainServiceType="Regular" JourneyDuration="PT22M" TrainNumber="0908" ArrivalDateTime="2018-12-27T09:30:00" DepartureDateTime="2018-12-27T09:08:00">
                                <DepartureStation Country="GB" Name="Leeds" LocationCode="7000041"/>
                                <ArrivalStation Country="GB" Name="York" LocationCode="7000075"/>
                                <RailAmenities>
                                    <RailAmenity Name="CROSSCOUNTRY"/>
                                </RailAmenities>
                                <ClassCodes>
                                    <ClassCode ServiceClass="FIRST"/>
                                    <ClassCode ServiceClass="STANDARD"/>
                                </ClassCodes>
                            </TrainSegment>
                        </JourneySegment>
                    </JourneySegments>
                </Journey>
            </Journeys>
        </OriginDestinationSpecifications>
        <PassengerSpecifications>
            <PassengerType Quantity="1" Age="-1"/>
        </PassengerSpecifications>
        <FareQualifier/>
        <ResponsePtPTypes>
            <ResponsePtPType>TR</ResponsePtPType>
        </ResponsePtPTypes>
    </RailAvailInfo>
</ACP_RailAvailRQ>



    '''

    serURL =  "https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ"
    headers = {'content-type': 'application/xml; charset=utf-8'}
    print "Before request"
    Result = requests.post(serURL, data=xlm2data, headers=headers)
    if Result.status_code == 200:
        response = Result.text
        print "$$$$",response1
        return HttpResponse(response)
    else:
        print "Status code error", Result.status_code
    print "After request"
    print "Response is ---->",Result
    # return "API VIEW"
    return HttpResponse("Get API RESPONSE")


def xmlt_to_dict(request):
    import xmltodict
    import json
    # import pprint


    xml_data = """<?xml version="1.0" encoding="UTF-8"?><ACP_RailAvailRS ResponseType="Native-Availability" xmlns="http://www.acprailinternational.com/API/R2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.acprailinternational.com/API/R2 ACP_RailAvailRS.xsd" Version="1.001" TimeStamp="2019-01-17T20:35:00" Target="Production"><Success/><OriginDestinationOptions><OriginDestinationOption OptionReference="1" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><Journeys><Journey JourneyDuration="PT5H9M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T08:09:00" ArrivalDateTime="2019-01-30T09:40:00" TrainNumber="0809" JourneyDuration="PT1H31M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000246" Name="London Victoria" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T09:40:00" ArrivalDateTime="2019-01-30T10:40:00" TrainNumber="0940" JourneyDuration="PT1H" TrainServiceType="Tube" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000246" Name="London Victoria" Country="GB"/><ArrivalStation LocationCode="7000021" Name="London Euston" Country="GB"/><RailAmenities><RailAmenity Name="Tube segment"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:40:00" ArrivalDateTime="2019-01-30T12:10:00" TrainNumber="1040" JourneyDuration="PT1H30M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000021" Name="London Euston" Country="GB"/><ArrivalStation LocationCode="7000096" Name="Crewe" Country="GB"/><RailAmenities><RailAmenity Name="VT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T12:23:00" ArrivalDateTime="2019-01-30T12:46:00" TrainNumber="1223" JourneyDuration="PT23M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000096" Name="Crewe" Country="GB"/><ArrivalStation LocationCode="7000168" Name="Chester" Country="GB"/><RailAmenities><RailAmenity Name="AW"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T13:02:00" ArrivalDateTime="2019-01-30T13:18:00" TrainNumber="1302" JourneyDuration="PT16M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000168" Name="Chester" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments></Journey><Journey JourneyDuration="PT5H43M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T08:09:00" ArrivalDateTime="2019-01-30T09:40:00" TrainNumber="0809" JourneyDuration="PT1H31M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000246" Name="London Victoria" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T09:40:00" ArrivalDateTime="2019-01-30T10:20:00" TrainNumber="0940" JourneyDuration="PT40M" TrainServiceType="Tube" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000246" Name="London Victoria" Country="GB"/><ArrivalStation LocationCode="7000021" Name="London Euston" Country="GB"/><RailAmenities><RailAmenity Name="Tube segment"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:20:00" ArrivalDateTime="2019-01-30T12:16:00" TrainNumber="1020" JourneyDuration="PT1H56M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000021" Name="London Euston" Country="GB"/><ArrivalStation LocationCode="7000187" Name="Stockport" Country="GB"/><RailAmenities><RailAmenity Name="VT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T12:52:00" ArrivalDateTime="2019-01-30T13:52:00" TrainNumber="1252" JourneyDuration="PT1H" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000187" Name="Stockport" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments></Journey><Journey JourneyDuration="PT5H39M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T08:39:00" ArrivalDateTime="2019-01-30T10:11:00" TrainNumber="0839" JourneyDuration="PT1H32M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000246" Name="London Victoria" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:11:00" ArrivalDateTime="2019-01-30T11:10:00" TrainNumber="1011" JourneyDuration="PT59M" TrainServiceType="Tube" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000246" Name="London Victoria" Country="GB"/><ArrivalStation LocationCode="7000021" Name="London Euston" Country="GB"/><RailAmenities><RailAmenity Name="Tube segment"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T11:10:00" ArrivalDateTime="2019-01-30T13:11:00" TrainNumber="1110" JourneyDuration="PT2H1M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000021" Name="London Euston" Country="GB"/><ArrivalStation LocationCode="7000168" Name="Chester" Country="GB"/><RailAmenities><RailAmenity Name="VT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T14:02:00" ArrivalDateTime="2019-01-30T14:18:00" TrainNumber="1402" JourneyDuration="PT16M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000168" Name="Chester" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments></Journey><Journey JourneyDuration="PT6H45M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T09:07:00" ArrivalDateTime="2019-01-30T10:05:00" TrainNumber="0907" JourneyDuration="PT58M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000087" Name="Southampton" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:17:00" ArrivalDateTime="2019-01-30T14:13:00" TrainNumber="1017" JourneyDuration="PT3H56M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000087" Name="Southampton" Country="GB"/><ArrivalStation LocationCode="7000187" Name="Stockport" Country="GB"/><RailAmenities><RailAmenity Name="XC"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T14:52:00" ArrivalDateTime="2019-01-30T15:52:00" TrainNumber="1452" JourneyDuration="PT1H" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000187" Name="Stockport" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments><FareRPHs><FareRPH>1</FareRPH><FareRPH>2</FareRPH><FareRPH>3</FareRPH><FareRPH>4</FareRPH><FareRPH>5</FareRPH><FareRPH>6</FareRPH><FareRPH>7</FareRPH></FareRPHs></Journey><Journey JourneyDuration="PT5H9M" IsSubComponent="false"><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><JourneySegments><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T09:09:00" ArrivalDateTime="2019-01-30T10:41:00" TrainNumber="0909" JourneyDuration="PT1H32M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000372" Name="Chichester" Country="GB"/><ArrivalStation LocationCode="7000246" Name="London Victoria" Country="GB"/><RailAmenities><RailAmenity Name="SN"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T10:41:00" ArrivalDateTime="2019-01-30T11:40:00" TrainNumber="1041" JourneyDuration="PT59M" TrainServiceType="Tube" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000246" Name="London Victoria" Country="GB"/><ArrivalStation LocationCode="7000021" Name="London Euston" Country="GB"/><RailAmenities><RailAmenity Name="Tube segment"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T11:40:00" ArrivalDateTime="2019-01-30T13:11:00" TrainNumber="1140" JourneyDuration="PT1H31M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000021" Name="London Euston" Country="GB"/><ArrivalStation LocationCode="7000096" Name="Crewe" Country="GB"/><RailAmenities><RailAmenity Name="VT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T13:23:00" ArrivalDateTime="2019-01-30T13:46:00" TrainNumber="1323" JourneyDuration="PT23M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000096" Name="Crewe" Country="GB"/><ArrivalStation LocationCode="7000168" Name="Chester" Country="GB"/><RailAmenities><RailAmenity Name="AW"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment><JourneySegment><TrainSegment DepartureDateTime="2019-01-30T14:02:00" ArrivalDateTime="2019-01-30T14:18:00" TrainNumber="1402" JourneyDuration="PT16M" TrainServiceType="Train" CrossBorder="false" OperatorName="ATOC"><DepartureStation LocationCode="7000168" Name="Chester" Country="GB"/><ArrivalStation LocationCode="7023060" Name="Delamere" Country="GB"/><RailAmenities><RailAmenity Name="NT"/></RailAmenities><ClassCodes/></TrainSegment></JourneySegment></JourneySegments></Journey></Journeys></OriginDestinationOption></OriginDestinationOptions><Fares><Fare FareReference="1" Class="First" IsEstimated="false" IsPreBookable="false" TicketingTimeLimit="2019-01-17T23:59:59.0Z" TicketCount="1" CurrencyCode="GBP" ItineraryType="One-Way-Outbound" IncludesProtectionPlan="false" ReservationRequired="true" ProductName="TICKET on DEPARTURE &amp; RESERVATION -ANYTIME via:ANY PERMITTED - Travel is allowed via any permitted route." RouteDescription="ANY PERMITTED - Travel is allowed via any permitted route." FareType="Regular" Magic="C81D4F20AED3C34BC033C93484779E0E
789C6D50CB4EC33010BCFB2B427B4EB57E25766F7E45E20002A59CAA1CD2C642
41695C35068110FF8E090F5184E5833D3BBB333BCB6DD83DF87DBCC8B6E8E48F
431EBA708C7D18A775B66D50DB757F90FA38F431BF39F57BBFCE96BFBA3721B6
C33F78D59E124271B102B4A9CD3A83F45087F038C66FD884C3A19FA6A4B1CE30
5F0974ED3F6A002B826A7F7A4A332BEF3F3B9B06DDB4CFD6C7B61FCE85EA21F1
2E6D1A91067689BE5076B340EDFD6C680CA36FD0ED633BC63EBE7C90EEC63E7E
F9FDE36E5E651E77EEB3AE3E755312AFCB57540A693815CE385619C514B3C471
CC9910AE0065ACD1C494D8385211A731271434A1CC02A58E03D11849CBB4D042
51237445A5E55419CC24B3465A20321505611A34A8925092A434034994C3DC48
2C19460C1C1745A9A0E046638D01D2AFC0A52A53DB7CD0DB1BBAEA9F7F7C6F73
DCA07C1FA6B41491B0E228DFB5D3AF84F26E370D7328F82C7BC21337853FDF77
AB299D4236020000
" UseAfterTL="2019-01-30" UseByTL="2019-01-29" TravelDate="2019-01-30" PaxUnits="1" PricingOnRequest="false" BookingOnRequest="false" TicketOption="ETK" PassportRequired="false" DateOfBirthRequired="false" PaxNameRequested="true" CntryResidenceRequired="false" NationalityRequired="false" PlaceOfBirthRequired="false" EmailRequired="false" TicketType="TicketAndReser"><ProdMarketingName><![CDATA[<div id="DisplayName">TICKET on DEPARTURE & RESERVATION -ANYTIME</div>]]></ProdMarketingName><PassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="316.00" TSC="0.00" TotalSliceAmount="316.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB15230B234D033E502B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
40E5867A065CB1B100867617A74B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></PassengerTypePrices><TotalPrice Fare="316.00" TSC="0.00" Amount="316.00" Commission="15.80" Net="300.20" ServiceFee="25.5"/><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><SubComponents/><IntegratedTotalPrice Fare="316.00" TSC="0.00" Amount="316.00" Commission="15.80" Net="300.20" ServiceFee="25.5"/><IntegratedPassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="316.00" TSC="0.00" TotalSliceAmount="316.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB15230B234D033E502B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
40E5867A065CB1B100867617A74B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></IntegratedPassengerTypePrices><PossiblePlacePrefs><PossibleSpecialRequests><SpecialRequest>Unspecified</SpecialRequest></PossibleSpecialRequests><PossibleCompartmentTypes><CompartmentType>Unspecified</CompartmentType></PossibleCompartmentTypes><PossiblePositions><Position>Unspecified</Position></PossiblePositions></PossiblePlacePrefs><SalesConditions RefundPolicy="Non-Refundable"><TermsAndConditions MustAcknowledge="true" URL="http://www.acprail.com/railways-terms-and-conditions/TTL-tod-ow-withres-anytime.html"/><RefundRules><RefundRule Sequence="1" DateBasis="Issue" WithinDateBasis="P0D" PenaltyRate="100.0" MinimumPenalty="0.0"/></RefundRules></SalesConditions></Fare><Fare FareReference="2" Class="Standard" IsEstimated="false" IsPreBookable="false" TicketingTimeLimit="2019-01-17T23:59:59.0Z" TicketCount="1" CurrencyCode="GBP" ItineraryType="One-Way-Outbound" IncludesProtectionPlan="false" ReservationRequired="true" ProductName="TICKET on DEPARTURE &amp; RESERVATION -ANYTIME via:ANY PERMITTED - Travel is allowed via any permitted route." RouteDescription="ANY PERMITTED - Travel is allowed via any permitted route." FareType="Regular" Magic="B6C04DE921232C86D97DF7219060144E
789C6D50C96EC23014BCFB2B523827F24A6C6EDE22F5D08A2AF4847208C4AA52
851811535121FEBD265D04A8960FD678DECCBC99AEFCFADD6DC243B2027BB7EB
52DFF85D687D3FCC935505EAA6B943CA5DD78674B16F376E9E4CAFA6973ED4DD
3F7851EF2382E92C836059EA7902E3436EFDA10FBFB0F6DB6D3B0CD1639E209C
11F0EC2E7F84643928DDFE236A16CE7D4F561558D447E342DD76B7466517798F
264A44C126D227D22C27A07E1B03F5BE77157839D47D68C3E785F4DAB7E127EF
5DBA719551EE3667597CFBC6264ED313C8B9D08C70AB2D2DB4A4921A6C196294
733B83521BADB0CE91B6B8C0562186092498600309B10C628580305471C525D1
5C15441846A4465450A3858158C44F8EA9820ACA3C0E462B45A1C0D222A60512
14010A2DE3B35CC219D30A2904216750A208C4B1F180F3193CB5C7BFDCAB1455
20DDF8E1B214861903E9BA1EAE1A4A9BF5D08DA5A09BEE318BDC58FE78BF00A9
369D3036020000
" UseAfterTL="2019-01-30" UseByTL="2019-01-29" TravelDate="2019-01-30" PaxUnits="1" PricingOnRequest="false" BookingOnRequest="false" TicketOption="ETK" PassportRequired="false" DateOfBirthRequired="false" PaxNameRequested="true" CntryResidenceRequired="false" NationalityRequired="false" PlaceOfBirthRequired="false" EmailRequired="false" TicketType="TicketAndReser"><ProdMarketingName><![CDATA[<div id="DisplayName">TICKET on DEPARTURE & RESERVATION -ANYTIME</div>]]></ProdMarketingName><PassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="246.00" TSC="0.00" TotalSliceAmount="246.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB152303232D033E502B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
40E5867A065CB1B100850A17A04B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></PassengerTypePrices><TotalPrice Fare="246.00" TSC="0.00" Amount="246.00" Commission="12.30" Net="233.70" ServiceFee="25.5"/><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><SubComponents/><IntegratedTotalPrice Fare="246.00" TSC="0.00" Amount="246.00" Commission="12.30" Net="233.70" ServiceFee="25.5"/><IntegratedPassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="246.00" TSC="0.00" TotalSliceAmount="246.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB152303232D033E502B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
40E5867A065CB1B100850A17A04B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></IntegratedPassengerTypePrices><PossiblePlacePrefs><PossibleSpecialRequests><SpecialRequest>Unspecified</SpecialRequest></PossibleSpecialRequests><PossibleCompartmentTypes><CompartmentType>Unspecified</CompartmentType></PossibleCompartmentTypes><PossiblePositions><Position>Unspecified</Position></PossiblePositions></PossiblePlacePrefs><SalesConditions RefundPolicy="Non-Refundable"><TermsAndConditions MustAcknowledge="true" URL="http://www.acprail.com/railways-terms-and-conditions/TTL-tod-ow-withres-anytime.html"/><RefundRules><RefundRule Sequence="1" DateBasis="Issue" WithinDateBasis="P0D" PenaltyRate="100.0" MinimumPenalty="0.0"/></RefundRules></SalesConditions></Fare><Fare FareReference="3" Class="First" IsEstimated="false" IsPreBookable="false" TicketingTimeLimit="2019-01-17T23:59:59.0Z" TicketCount="1" CurrencyCode="GBP" ItineraryType="One-Way-Outbound" IncludesProtectionPlan="false" ReservationRequired="true" ProductName="TICKET on DEPARTURE &amp; RESERVATION -ANYTIME via:VIA BANBURY - Valid only for travel via (changing trains or passing through) Banbury." RouteDescription="VIA BANBURY - Valid only for travel via (changing trains or passing through) Banbury." FareType="Regular" Magic="5A95C168159EC72FB3C34AB5E44DEC6A
789C6D50CB6AC33010BCEB2BDCE66CA3A72DE5A697A1879614A7A7E083138BE2
E25821564A4BC9BF57761F24A5620F6276776676161BBF7D71BB70936CC0D11D
FAD4B7FE103A3F8CCB645383A66DFF20D5A1EF42BA3A763BB74C1617DB6B1F9A
FE1FBC6C8E1121B8C82058577A99C0F8917B7F1AC20FACFD7EDF8D63D4582628
CF08030F6E6A2298E50C54EEF81A594BE7BE76EB1AAC9A37E342D3F5D752551F
E7EE4C2489946D1CBF95667D0B9AE7D9D2E0075783C75333842EBC4F434F4317
BE1DFFF1371F33D35D3BADCA2FDD98C5C7E203145C6846B8D596965A52490DB6
0C31CAB9CDA1D4462BAC0BA42D2EB155886102494EA0A184D802628580305471
C525D15C95441846A4465450A3858158C426C75441056581098E528A4281A545
4C0B242802145AC6F342C29C6985148290B35CA3424E6BF303E733B8EFDE7E7D
6F52548374E7C7E92888B202A4DB66BC48286DB7633F8782AEB2C72C2353F873
7D02BCF39DAB38020000
" UseAfterTL="2019-01-30" UseByTL="2019-01-29" TravelDate="2019-01-30" PaxUnits="1" PricingOnRequest="false" BookingOnRequest="false" TicketOption="ETK" PassportRequired="false" DateOfBirthRequired="false" PaxNameRequested="true" CntryResidenceRequired="false" NationalityRequired="false" PlaceOfBirthRequired="false" EmailRequired="false" TicketType="TicketAndReser"><ProdMarketingName><![CDATA[<div id="DisplayName">TICKET on DEPARTURE & RESERVATION -ANYTIME</div>]]></ProdMarketingName><PassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="327.00" TSC="0.00" TotalSliceAmount="327.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB152303630D433E702B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
40E5867A065CB1B100856C17A24B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></PassengerTypePrices><TotalPrice Fare="327.00" TSC="0.00" Amount="327.00" Commission="16.35" Net="310.65" ServiceFee="25.3"/><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><SubComponents/><IntegratedTotalPrice Fare="327.00" TSC="0.00" Amount="327.00" Commission="16.35" Net="310.65" ServiceFee="25.3"/><IntegratedPassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="327.00" TSC="0.00" TotalSliceAmount="327.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB152303630D433E702B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
40E5867A065CB1B100856C17A24B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></IntegratedPassengerTypePrices><PossiblePlacePrefs><PossibleSpecialRequests><SpecialRequest>Unspecified</SpecialRequest></PossibleSpecialRequests><PossibleCompartmentTypes><CompartmentType>Unspecified</CompartmentType></PossibleCompartmentTypes><PossiblePositions><Position>Unspecified</Position></PossiblePositions></PossiblePlacePrefs><SalesConditions RefundPolicy="Non-Refundable"><TermsAndConditions MustAcknowledge="true" URL="http://www.acprail.com/railways-terms-and-conditions/TTL-tod-ow-withres-anytime.html"/><RefundRules><RefundRule Sequence="1" DateBasis="Issue" WithinDateBasis="P0D" PenaltyRate="100.0" MinimumPenalty="0.0"/></RefundRules></SalesConditions></Fare><Fare FareReference="4" Class="Standard" IsEstimated="false" IsPreBookable="false" TicketingTimeLimit="2019-01-17T23:59:59.0Z" TicketCount="1" CurrencyCode="GBP" ItineraryType="One-Way-Outbound" IncludesProtectionPlan="false" ReservationRequired="true" ProductName="TICKET on DEPARTURE &amp; RESERVATION -ANYTIME via:VIA BANBURY - Valid only for travel via (changing trains or passing through) Banbury." RouteDescription="VIA BANBURY - Valid only for travel via (changing trains or passing through) Banbury." FareType="Regular" Magic="FD2452892D95E83483C00762AA62AC42
789C6D50CB4EC33010BCFB2B427B4EE46762F766AF138903089472AA72481B0B
05A571D5180442FC3B6E0A8822563E58B3BB33B3B3DCF8ED93DB85AB64838EEE
30A4BEF387D0FB715A259B06B55DF707A90F431FD2BB63BF73AB64F96B7BED43
3BFC8357ED312224A71946EB1A56098E1FBDF7CF63F886C1EFF7FD34458D5522
33826EDDA92558A650ED8E2F91B272EEBCD834E8AE7DB52EB4FD70A9530F71EE
DAC6C5C8D7C5F185B6EB056A1F673FA31F5D83EE9FDB31F4E1ED34F430F6E1CB
EE1F73F32533DDA5CDBA3AEBC620DE97EFA8900A04932594BC02CD35B7B41444
7029CB1C6BB0602814044A5AD1D2104119669CE596C512A5C01415440137D248
CD409A8A292B9806C215B7A02CA62A3625E5061BAC0BCA6814331C2BAA4B2240
118538A1B81285C6B900430CC1584909A4B086039E0B7D7CA09BFEF5C7F72625
0D4A777E3A1DC5F24C08946EDBE9574469B79D86732A17E1539171718A7F7E9F
61C19D8337020000
" UseAfterTL="2019-01-30" UseByTL="2019-01-29" TravelDate="2019-01-30" PaxUnits="1" PricingOnRequest="false" BookingOnRequest="false" TicketOption="ETK" PassportRequired="false" DateOfBirthRequired="false" PaxNameRequested="true" CntryResidenceRequired="false" NationalityRequired="false" PlaceOfBirthRequired="false" EmailRequired="false" TicketType="TicketAndReser"><ProdMarketingName><![CDATA[<div id="DisplayName">TICKET on DEPARTURE & RESERVATION -ANYTIME</div>]]></ProdMarketingName><PassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="162.00" TSC="0.00" TotalSliceAmount="162.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB152303436D33335E502
719C4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C919
4120F57A065CB1B100988C17DB4C000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></PassengerTypePrices><TotalPrice Fare="162.00" TSC="0.00" Amount="162.00" Commission="8.10" Net="153.90" ServiceFee="25.45"/><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><SubComponents/><IntegratedTotalPrice Fare="162.00" TSC="0.00" Amount="162.00" Commission="8.10" Net="153.90" ServiceFee="25.45"/><IntegratedPassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="162.00" TSC="0.00" TotalSliceAmount="162.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB152303436D33335E502
719C4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C919
4120F57A065CB1B100988C17DB4C000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></IntegratedPassengerTypePrices><PossiblePlacePrefs><PossibleSpecialRequests><SpecialRequest>Unspecified</SpecialRequest></PossibleSpecialRequests><PossibleCompartmentTypes><CompartmentType>Unspecified</CompartmentType></PossibleCompartmentTypes><PossiblePositions><Position>Unspecified</Position></PossiblePositions></PossiblePlacePrefs><SalesConditions RefundPolicy="Non-Refundable"><TermsAndConditions MustAcknowledge="true" URL="http://www.acprail.com/railways-terms-and-conditions/TTL-tod-ow-withres-anytime.html"/><RefundRules><RefundRule Sequence="1" DateBasis="Issue" WithinDateBasis="P0D" PenaltyRate="100.0" MinimumPenalty="0.0"/></RefundRules></SalesConditions></Fare><Fare FareReference="5" Class="First" IsEstimated="false" IsPreBookable="false" TicketingTimeLimit="2019-01-17T23:59:59.0Z" TicketCount="1" CurrencyCode="GBP" ItineraryType="One-Way-Outbound" IncludesProtectionPlan="false" ReservationRequired="true" ProductName="TICKET on DEPARTURE &amp; RESERVATION -OFFPEAK via:ANY PERMITTED - Travel is allowed via any permitted route." RouteDescription="ANY PERMITTED - Travel is allowed via any permitted route." FareType="Regular" Magic="CF66C085AF839D7A3C7CD476FA1A7BDF
789C6D50C96EC23014BCFB2B523827F24A6C6EDE22F5D08A2AF4847208C4AA52
851811535121FEBD265D04A8960FD6BC9937E399AEFCFADD6DC243B2027BB7EB
52DFF85D687D3FCC935505EAA6B943CA5DD78674B16F376E9E4CAFD44B1FEAEE
1FBCA8F711C19067102C4B3D4F607CC8AD3FF4E117D67EBB6D87217ACC130433
0A9E5D9C2191673350BAFD47DC5938F7ADAC2AB0A88FC685BAED6E8DCA2EF21E
4D14C6854DA44FA4594E40FD3606EA7DEF2AF072A8FBD086CF0BE9B56FC34FDE
BB74E357C675B739CBE2DB3736719A9E40CE8566845B6D69A12595D460CB10A3
9CDB1994DA6885758EB4C505B60A314CA0A2041A4C8865102B0484A18A2B2E89
E6AA20C2302235A2821A2D0CC4220E39A60A2A28734C70B452140A2C2D625A20
4111C0D0B25CC219D30A2904219FE504E5328FA2F180F3193CB5C7BFD4AB1455
20DDF8E1522FC71903E9BA1EAEFA499BF5D08D95A09BE6318BDC58FD78BF008A
3F9CD834020000
" UseAfterTL="2019-01-30" UseByTL="2019-01-29" TravelDate="2019-01-30" PaxUnits="1" PricingOnRequest="false" BookingOnRequest="false" TicketOption="ETK" PassportRequired="false" DateOfBirthRequired="false" PaxNameRequested="true" CntryResidenceRequired="false" NationalityRequired="false" PlaceOfBirthRequired="false" EmailRequired="false" TicketType="TicketAndReser"><ProdMarketingName><![CDATA[<div id="DisplayName">TICKET on DEPARTURE & RESERVATION -OFFPEAK</div>]]></ProdMarketingName><PassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="208.00" TSC="0.00" TotalSliceAmount="208.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB15230B430D233E502B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
20E57A065CB1B100867317A74B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></PassengerTypePrices><TotalPrice Fare="208.00" TSC="0.00" Amount="208.00" Commission="10.40" Net="197.60" ServiceFee="25.5"/><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><SubComponents/><IntegratedTotalPrice Fare="208.00" TSC="0.00" Amount="208.00" Commission="10.40" Net="197.60" ServiceFee="25.5"/><IntegratedPassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="208.00" TSC="0.00" TotalSliceAmount="208.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB15230B430D233E502B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
20E57A065CB1B100867317A74B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></IntegratedPassengerTypePrices><PossiblePlacePrefs><PossibleSpecialRequests><SpecialRequest>Unspecified</SpecialRequest></PossibleSpecialRequests><PossibleCompartmentTypes><CompartmentType>Unspecified</CompartmentType></PossibleCompartmentTypes><PossiblePositions><Position>Unspecified</Position></PossiblePositions></PossiblePlacePrefs><SalesConditions RefundPolicy="Non-Refundable"><TermsAndConditions MustAcknowledge="true" URL="http://www.acprail.com/railways-terms-and-conditions/TTL-tod-ow-withres-offpeak.html"/><RefundRules><RefundRule Sequence="1" DateBasis="Issue" WithinDateBasis="P0D" PenaltyRate="100.0" MinimumPenalty="0.0"/></RefundRules></SalesConditions></Fare><Fare FareReference="6" Class="Standard" IsEstimated="false" IsPreBookable="false" TicketingTimeLimit="2019-01-17T23:59:59.0Z" TicketCount="1" CurrencyCode="GBP" ItineraryType="One-Way-Outbound" IncludesProtectionPlan="false" ReservationRequired="true" ProductName="TICKET on DEPARTURE &amp; RESERVATION -OFFPEAK via:ANY PERMITTED - Travel is allowed via any permitted route." RouteDescription="ANY PERMITTED - Travel is allowed via any permitted route." FareType="Regular" Magic="6A97506BF2C511E7735C21EC8A68ADD5
789C6D503B6FC23018DCFD2B529883FC6CEC6C7E45EAD08A2A74421902B1AA54
2146C4545488FF5E13DA0A502D0FD67D77DF9D6FBAF4AB0FB70E0FC912ECDCB6
4B7DE3B7A1F5FD9027CB0AD44D738794DBAE0DE97CD7AE5D9E4CAFD40B1FEAEE
1FBCA877114114CD2058943A4F607CC88DDFF7E117D67EB36987217AE4493683
0CBCB8F38C909960A074BBCFB8B470EE22AD2A30AF0FC685BAED6E9DCA2EF29E
4C54C68D4DA44FA4594C40FD3E26EA7DEF2AF0BAAFFBD086AF33E9AD6FC34FE0
BB78E35FC675B741CBE2E21BAB384E8F20E34233C2ADB6B4D0924A6AB0658851
CEED2394DA68857586B4C505B60A314C20A1841A468865102B0484A18A2B2E89
E6AA20224EA4465450A3858158C421C75441056586098E568A4281A5454C0B24
2802185A9649F8C8B4420A41C899842893248AC6034E27F0DC1EFE522F535481
74ED87F397109B3190AEEAE1AA9FB4590DDDA5929BE6F1991BAB1FEF37F2609C
F335020000
" UseAfterTL="2019-01-30" UseByTL="2019-01-29" TravelDate="2019-01-30" PaxUnits="1" PricingOnRequest="false" BookingOnRequest="false" TicketOption="ETK" PassportRequired="false" DateOfBirthRequired="false" PaxNameRequested="true" CntryResidenceRequired="false" NationalityRequired="false" PlaceOfBirthRequired="false" EmailRequired="false" TicketType="TicketAndReser"><ProdMarketingName><![CDATA[<div id="DisplayName">TICKET on DEPARTURE & RESERVATION -OFFPEAK</div>]]></ProdMarketingName><PassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="141.00" TSC="0.00" TotalSliceAmount="141.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB152303434D533E502B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
20E57A065CB1B10085A017A34B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></PassengerTypePrices><TotalPrice Fare="141.00" TSC="0.00" Amount="141.00" Commission="7.05" Net="133.95" ServiceFee="25.5"/><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><SubComponents/><IntegratedTotalPrice Fare="141.00" TSC="0.00" Amount="141.00" Commission="7.05" Net="133.95" ServiceFee="25.5"/><IntegratedPassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="141.00" TSC="0.00" TotalSliceAmount="141.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB152303434D533E502B1
9D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C91941
20E57A065CB1B10085A017A34B000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></IntegratedPassengerTypePrices><PossiblePlacePrefs><PossibleSpecialRequests><SpecialRequest>Unspecified</SpecialRequest></PossibleSpecialRequests><PossibleCompartmentTypes><CompartmentType>Unspecified</CompartmentType></PossibleCompartmentTypes><PossiblePositions><Position>Unspecified</Position></PossiblePositions></PossiblePlacePrefs><SalesConditions RefundPolicy="Non-Refundable"><TermsAndConditions MustAcknowledge="true" URL="http://www.acprail.com/railways-terms-and-conditions/TTL-tod-ow-withres-offpeak.html"/><RefundRules><RefundRule Sequence="1" DateBasis="Issue" WithinDateBasis="P0D" PenaltyRate="100.0" MinimumPenalty="0.0"/></RefundRules></SalesConditions></Fare><Fare FareReference="7" Class="Standard" IsEstimated="false" IsPreBookable="false" TicketingTimeLimit="2019-01-17T23:59:59.0Z" TicketCount="1" CurrencyCode="GBP" ItineraryType="One-Way-Outbound" IncludesProtectionPlan="false" ReservationRequired="true" ProductName="TICKET on DEPARTURE &amp; RESERVATION -ADVANCE via:XC  &amp;CONNECTIONS - Only valid on booked CrossCountry services and required connecting services." RouteDescription="XC  &amp;CONNECTIONS - Only valid on booked CrossCountry services and required connecting services." FareType="Regular" Magic="977BDEC95EE6DA98D46C6F54DF326434
789C6D50CB6EC23010BCFB2B523807F949ECDCFC48A41E5A51859EA21C02B1AA
54214689A9A810FF5E13500555AD3D58B3BB33B3332FDDE6D36EFD535482C1EE
BBD8356EEF5BD78F695456A06E9A3F48B1EF5A1FAF86766BD3687EB7BD76BEEE
FEC1F37A08084D1610AC0B9D46307CE4CE1D7A7F43B5DBEDDA710C0A69841784
81577B69D1C59281C20E5F8131B7F6BA585560551F8DF575DB3DCA145D987B36
6984026113C667D2AC67A0FE98ECF4AEB715783BD4BD6FFDF765E8BD6FFDCDED
A3B7E98E89EDC165915F55430AA7F909245C684678A6339A6B49253538638851
CEB32594DA688575827486739C29C430816A692021198498206100555C714934
5739118611A91115D468612016A1C9315550419960828390A250609921A60512
1451080CE34B0A355348210813CA384A124C259C1E389FC14B7BFCF55CC6A802
F1D68DE11EC2C33DF1A61EEFA2899BCDD84D69A087D0C535F4A97E001E469B23
2C020000
" UseAfterTL="2019-01-30" UseByTL="2019-01-29" TravelDate="2019-01-30" PaxUnits="1" PricingOnRequest="false" BookingOnRequest="false" TicketOption="ETK" PassportRequired="false" DateOfBirthRequired="false" PaxNameRequested="true" CntryResidenceRequired="false" NationalityRequired="false" PlaceOfBirthRequired="false" EmailRequired="false" TicketType="TicketAndReser"><ProdMarketingName><![CDATA[<div id="DisplayName">TICKET on DEPARTURE & RESERVATION -ADVANCE</div>]]></ProdMarketingName><PassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="47.00" TSC="0.00" TotalSliceAmount="47.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB15230B6D033E002319D
4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C9194140
D58640C5B1B100745817724A000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></PassengerTypePrices><TotalPrice Fare="47.00" TSC="0.00" Amount="47.00" Commission="2.35" Net="44.65" ServiceFee="9.0"/><OriginLocation LocationCode="7000372" Name="Chichester" Country="GB"/><DestinationLocation LocationCode="7023060" Name="Delamere" Country="GB"/><SubComponents/><IntegratedTotalPrice Fare="47.00" TSC="0.00" Amount="47.00" Commission="2.35" Net="44.65" ServiceFee="9.0"/><IntegratedPassengerTypePrices><PassengerMixSlice SliceID="1" Code="ADT" Quantity="1" UnitPrice="47.00" TSC="0.00" TotalSliceAmount="47.00" SFDetails="#{
789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB15230B6D033E002319D
4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C9194140
D58640C5B1B100745817724A000000
}"><MixDetails><PassengerPlaceholder Age="-1"/></MixDetails></PassengerMixSlice></IntegratedPassengerTypePrices><PossiblePlacePrefs><PossibleSpecialRequests><SpecialRequest>Unspecified</SpecialRequest></PossibleSpecialRequests><PossibleCompartmentTypes><CompartmentType>Unspecified</CompartmentType></PossibleCompartmentTypes><PossiblePositions><Position>Unspecified</Position></PossiblePositions></PossiblePlacePrefs><SalesConditions RefundPolicy="Non-Refundable"><TermsAndConditions MustAcknowledge="true" URL="http://www.acprail.com/railways-terms-and-conditions/TTL-tod-ow-withres-advance.html"/><RefundRules><RefundRule Sequence="1" DateBasis="Issue" WithinDateBasis="P0D" PenaltyRate="100.0" MinimumPenalty="0.0"/></RefundRules></SalesConditions></Fare></Fares><CountryLists/></ACP_RailAvailRS>
    """

    result = xmltodict.parse(xml_data)
    print (result)
    print "**"*30
    print result['ACP_RailAvailRS']['OriginDestinationOptions']
    # print result['ACP_RailAvailRQ']['POS']['RequestorID']

    return HttpResponse("tested")
