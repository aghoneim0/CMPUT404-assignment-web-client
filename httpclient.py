#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle,Ahmed Ghoneim
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    
    #Creates the Request to be sent 
    def get_header(self,method,data):

        url  = data[0]
        host = data[1]
        port = data[2]
        content_type = data[3]
        content_length = data[4]
        contnet= data[6]
        line = "\r\n"
        request = [
            method+' /'+url+'  HTTP/1.1',
            'Host: '+host,
            'Connection: keep-alive',
            content_type,
            content_length,
            "",
            contnet,
            "",
                ]
        
        return line.join(request)

    # Returns the Host/Port number for the socket to connect to 
    def get_config(self, url):

        result=[]
        if '127.0.0.1' in url:
            temp  = url.split('/')
            host = temp[2].split(':')[0]
            port = temp[2].split(':')[1]
            del temp[0],temp[0],temp[0]
            temp = '/'.join(temp)
            result.extend([temp,host,int(port)])
        else:
            print url
            host = url.split('/')[2]
            url=''
            port=80
            result.extend([url,host,port])

        return result

    def get_code(self,data):
        data=data.split(' ')
        data=int(data[1])
        return data

    def GET(self, url, args=None):
        code = 500
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        data= self.get_config(url) # Get Host/Port number to connect to 
        url = data[0]
        host= data[1]
        port= data[2]
        s.connect((host,port))
        data.extend(["","","",""])

        request=self.get_header('GET',data)
        print '====================================GET Request================================='
      
        s.send(request)
        body=''
        buffer = s.recv(1024)
        while buffer:
            body += buffer
            buffer = s.recv(1024)
        print '====================================GET Response================================='
        print body
        code=self.get_code(body) # Replace Code 500 with response code
        return HTTPRequest(code, body)
       
    def POST(self, url, args=None):
        code = 500
        print url
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        data=self.get_config(url) 
        url = data[0]
        host= data[1]
        port= data[2]

        s.connect((host,port)) # Get Host/Port number to connect to 
       
        if args == None:

            data.extend(['Content-Type: application/x-www-form-urlencoded',
            	"",
            	"",""])

        else:
        	args=urllib.urlencode(args)
        	data.extend(['Content-Type: application/x-www-form-urlencoded',
        	 'Content-Length: %s' % (len(args)),
        	 	"",
        	 	args,
        	 	"",
        	 	])
        request=self.get_header('POST',data)
        print '====================================POST Request================================='
        s.send(request)
        buffer = s.recv(1024)
        response=''
        while buffer:
            response += buffer
            buffer = s.recv(1024)
        code=response
        print '====================================POST Response================================='
        print response
        code=self.get_code(response) # Replace Code 500 with response code
        response=response.splitlines()
        response= response[len(response)-1]  #Json Last Line 
        body=response
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        
        print client.command( sys.argv[1],command)    
