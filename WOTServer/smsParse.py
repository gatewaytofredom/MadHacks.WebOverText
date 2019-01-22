import re

class smsParse:

    def getHostname(self,client_data):
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
    def getPort(self,client_data):

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
    def getRequest(self,client_data):
        sub = 'GET'
        sub2 = '1.1'
        request_start = str(client_data).find(sub,0)
        request_end = str(client_data).find(sub2,0) + 3
        return str(client_data)[request_start:request_end]

