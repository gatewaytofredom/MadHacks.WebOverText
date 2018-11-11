import WotServerOutBound
from twilio.twiml.messaging_response import MessagingResponse
import requests
import binascii
from flask import Flask, request
import socket
import re

web_request = []

print("webserver started \n")

#return hostname from clientdata
def parse_client_hostname(client_data):
    re1='(Host)'	# Word 1
    re2='(:)'	# Any Single Character 1
    re3='(\\s+)'	# White Space 1
    re4='((?:[a-z][a-z\\.\\d\\-]+)\\.(?:[a-z][a-z\\-]+))(?![\\w\\.])'	# Fully Qualified Domain Name 1

    rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
    m = rg.search(str(client_data))
    if m:
        word1=m.group(1)
        c1=m.group(2)
        ws1=m.group(3)
        fqdn1=m.group(4)
    print(str(fqdn1))
    return str(fqdn1)

#return port from client data
def parse_client_port(client_data):

    re1='(Port)'	# Word 1
    re2='.*?'	# Non-greedy match on filler
    re3='(\\d+)'	# Integer Number 1

    rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
    m = rg.search(str(client_data))
    if m:
        word1=m.group(1)
        int1=m.group(2)
        print(int1)
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
def send_request(request,target_url,port):
    result_list = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_url, int(port)))
    print('request: ' + request +'\r\n\r\n')
    s.send(bytes(request +'\r\n\r\n', 'utf8'))

    result = s.recv(10000)
    print("BEGIN DATA DUMP")

    #revieve data and store in list
    while (len(result) > 0):

        result_list.append(str(result))
        result = s.recv(10000)

    for index,text in enumerate(result_list):

        #convert recieved bytes to utf-8
        result_list[index] = text.decode("utf-8")

    print(''.join(result_list))
    print("END DATA DUMP")

    #return recieved data as single string
    return ''.join(result_list)

#returns webrequest as a single string
def construct_request():
    return ''.join(web_request)

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    print('hello\n')
    #extract requested
    client_data = request.values.get('Body', None)
    print(client_data)

    #"parses" each request
    if "[end]" in client_data:
        end = client_data.find('[end]') -1
        web_request.append(client_data[0:end])

        host_name = parse_client_hostname(web_request)
        print('hostname: '+host_name)

        port = parse_client_port(web_request)
        print('port: '+port)

        header = parse_client_request(web_request)
        print(str(header))

        a = send_request(''.join(web_request),host_name,port)

        resp = MessagingResponse()
        # Add a message
        resp.message(a)

        return str(resp)

    else:
        web_request.append(client_data)

    return ''

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
    print('flask server worky maybe')






