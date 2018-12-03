
import socket
import requests
import httpser

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