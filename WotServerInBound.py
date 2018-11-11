
from twilio.twiml.messaging_response import MessagingResponse
import requests
from flask import Flask, request
import socket
import re
from twilio.rest import Client
import math
import ssl
import httpser



# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC19db4c54f66c8c11a7bd3d43ec220064'
auth_token = 'd84514af3b6cf09e40c659950ca4b99a'
client = Client(account_sid, auth_token)

def sendyboi(message,outbound_number):
    message = client.messages \
    .create(
         body=str(message),
         from_='+17155046198',
         to=outbound_number
     )


web_request = []

#gets webpage's source based on requested url
#returns source hex.
# def get_webpage(requested_url):
#     url = requested_url
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, lik
#return hostname from clientdata

#
def send_request(requestr,target_url,port):
    print(port)
    result_list = []

    try:

        if int(port) != 443:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_url, int(port)))
            s.send(bytes(requestr +'\r\n\r\n', 'utf8'))
        else: 
            httpsoutput = httpser.requester(requestr,target_url)
            print(httpsoutput)
            return httpsoutput

    except Exception as e:
        print(e)
    
    print("BEGIN DATA DUMP")

    result = s.recv(1024)

    #revieve data and store in list
    while (len(result) > 0):
        result_list.append(result.decode())
        result = s.recv(1024)
    s.close()

    #return recieved data as single string
    print("http:"+str(type(''.join(result_list))))
    return ''.join(result_list)

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

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    web_request = []
    #extract requested
    client_data = request.values.get('Body', None)
    client_number = request.values.get('From',None)

    #"parses" each request
    if "[end]" in client_data:
        end = client_data.find('[end]') 
        web_request.append(client_data[0:end])

        host_name = parse_client_hostname(web_request)

        port = parse_client_port(web_request)

        header = parse_client_request(web_request)

        a = send_request(''.join(web_request),host_name,port)

        # resp = MessagingResponse()
        # Add a message
        # resp.message(a)

        looptimes = math.ceil(len(a) / 120)

        for x in range(0,looptimes):

            if len(a) > 0:
                # sendyboi(str(resp)[0:120],client_number)
                print(str(x)+': '+a[0:120]+'\n')
                a = a[120:] 
        
        return ('')

    else:
        web_request.append(client_data)

    return ''

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')




