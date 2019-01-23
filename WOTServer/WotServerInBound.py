
from twilio.twiml.messaging_response import MessagingResponse
import requests
from flask import Flask, request

import math
import ssl
import httpser
import WebRequest
import WotServerOutBound
import smsParse

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

        #determine number of text messages required to send all data
        looptimes = math.ceil(len(WebRequest) / 120)

        for x in range(0,looptimes):

            if len(response) > 0:
                SmsHandler.send(response[0+(120*x):120*(x+1)],clientNumber)
                print(str(x)+': '+response[0:120]+'\n')
        return ''

    else:
        web_request.append(clientData)

    return ''

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')




