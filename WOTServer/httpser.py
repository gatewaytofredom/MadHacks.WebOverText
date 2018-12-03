import ssl
import socket

#get https web request
#return website source as single string
def requester(request,hostname):


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # hostname = 'github.com'
    s.connect((hostname, 443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    s.sendall(bytes("GET / HTTP/1.1\r\nHost: "+hostname+"\r\nConnection: close\r\n\r\n", 'utf8'))
    ab = []

    while True:
        new = s.recv(1024)
        if not new:
            s.close()
            break

        ab.append(new.decode())
    s.close()
    return ''.join(ab)


requester('asd','github.com')

