
from twilio.twiml.messaging_response import MessagingResponse
import requests
from flask import Flask, request

import math
import ssl
import httpser
import WebRequest
import WotServerOutBound
import smsParse

web_request = []

#gets webpage's source based on requested url
#returns source hex.
# def get_webpage(requested_url):
#     url = requested_url
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, lik
#return hostname from clientdata

app = Flask(__name__)

# Called when the sms webdirectory is accessed from twillio

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():

    #Create an object for handeling server to client messaging
    SmsHandler = WotServerOutBound.smsSender()
    parseSms = smsParse.smsParse()

    web_request = []
    #extract clients request and phone number
    clientData = request.values.get('Body', None)
    clientNumber = request.values.get('From',None)

    # sends users web request and returns the websites response
    #returns webrequest as a single string
    def constructRequest(self):
        return ''.join(web_request)

    #"parses" each request
    if "[end]" in clientData:
        end = clientData.find('[end]') 
        
        web_request.append(clientData[0:end])

        # Get Hostname
        host_name = parseSms.getHostname(web_request)

        # Get Port
        port = parseSms.getPort(web_request)

        # Get Header Data
        header = parseSms.getRequest(web_request)

        #create web request
        wotRequest = WebRequest

        response = WebRequest.send_request(''.join(web_request),host_name,port)

        resp = MessagingResponse()
        #Add a message
        resp.message(response)

        looptimes = math.ceil(len(WebRequest) / 120)

        for x in range(0,looptimes):

            if len(response) > 0:
                SmsHandler.send(response[0+(120*x):120*(x+1)],clientNumber)
                print(str(x)+': '+response[0:120]+'\n')
                #a = a[120:] 
                # resp.message(a)
        
        return ('')

    else:
        web_request.append(clientData)

    return ''

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')




