
from twilio.twiml.messaging_response import MessagingResponse
import requests
from flask import Flask, request
import re
import math
import ssl
import httpser
import WebRequest
import WotServerOutBound

web_request = []

#gets webpage's source based on requested url
#returns source hex.
# def get_webpage(requested_url):
#     url = requested_url
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, lik
#return hostname from clientdata


def parse_client_hostname(client_data):
    re1='(Host)'	# Word 1
    re2='(:)'	# Any Single Character 1
    re3='(\\s+)'	# White Space 1
    re4='((?:[a-z][a-z\\.\\d\\-]+)\\.(?:[a-z][a-z\\-]+))(?![\\w\\.])'	# Fully Qualified Domain Name 1

    rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
    m = rg.search(str(client_data))
    if m:
        fqdn1=m.group(4)
    return str(fqdn1)

#return port from client data
def parse_client_port(client_data):

    re1='(Port)'	# Word 1
    re2='.*?'	# Non-greedy match on filler
    re3='(\\d+)'	# Integer Number 1

    rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
    m = rg.search(str(client_data))
    if m:
        int1=m.group(2)
        return int1
    pass

#Return request from client data
def parse_client_request(client_data):
    sub = 'GET'
    sub2 = '1.1'
    request_start = str(client_data).find(sub,0)
    request_end = str(client_data).find(sub2,0) + 3
    return str(client_data)[request_start:request_end]

# sends users web request and returns the websites response
#returns webrequest as a single string
def construct_request():
    return ''.join(web_request)

app = Flask(__name__)



# Called when the sms webdirectory is accessed from twillio

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():

    #Create an object for handeling server to client messaging
    SmsHandler = WotServerOutBound.smsSender()

    web_request = []
    #extract clients request and phone number
    clientData = request.values.get('Body', None)
    clientNumber = request.values.get('From',None)

    #"parses" each request
    if "[end]" in clientData:
        end = clientData.find('[end]') 
        web_request.append(clientData[0:end])

        # Get Hostname
        host_name = parse_client_hostname(web_request)

        # Get Port
        port = parse_client_port(web_request)

        # Get Header Data
        header = parse_client_request(web_request)

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




