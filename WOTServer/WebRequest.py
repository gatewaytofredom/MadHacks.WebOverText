
import socket
import requests
import httpser

def send_request(requester,target_url,port):
    print(port)
    data = []

    try:
        # HTTPS Request 
        if int(port) != 443:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_url, int(port)))
            s.send(bytes(requester +'\r\n\r\n', 'utf8'))
        # HTTP Request
        else: 
            httpsOutput = httpser.requester(requester,target_url)
            print(httpsOutput)
            return httpsOutput

    except Exception as e:
        print(e)
    
    print("BEGIN DATA DUMP")

    incomingData = s.recv(1024)

    # Revieve data on socket
    while (len(incomingData) > 0):
        data.append(incomingData.decode())
        incomingData = s.recv(1024)
    s.close()

    # Return concatinated data
    print("http:"+str(type(''.join(data))))
    return ''.join(data)