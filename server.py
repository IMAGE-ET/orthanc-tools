import SimpleHTTPServer
import SocketServer
import logging
import urlparse
import cgi
import BaseHTTPServer
import time
import urllib
import string
import operator
import threading
import subprocess

HOST_NAME = ''
PORT_NUMBER = 8043
CC_SERVER = 'http://192.168.50.123:8042'
PORT_NUMBER_WADO_TRANS = 8044
WADO_SERVER = 'http://192.168.50.105:1000'

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.error(self.headers)
        # whatever else you would like to log here
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(sock):
        logging.error(sock.headers)
        logging.error("--------------------BODY-----------------")
        length = int(sock.headers['Content-Length'])
        logging.error(length)
        logging.error(sock)
        #post_data = urlparse.parse_qs(sock.rfile.read(length).decode('utf-8'))
        #logging.error(post_data)
        form = cgi.parse_qs(sock.rfile.read(length), keep_blank_values=1)
        logging.error(form)
        logging.error("----------form--------")
        #for field in form.keys():
        #      print "%s=%s" % (field,form[field].value)

class ServerHandler2(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):
        print s.path
        split_path = string.split(s.path,'?')
        params = {}
        if len(split_path) > 1:
            split_params = string.split(split_path[1],'&')
            print map(lambda x: string.split(x,'='),split_params)
            try:
                params = dict(map(lambda x: string.split(x,'='), split_params))
            except ValueError:
                params = {}
            if (params.has_key('_')):
                del params['_']
#        patient_map = operator.itemgetter('PatientID')(params)
        post_data = string.replace(str(params), '\'', '"')
        print post_data
        answer = urllib.urlopen(CC_SERVER + split_path[0], post_data).read()
        print answer
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        s.wfile.write(answer)

class ServerHandler3(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):
        print "AAAAAAA"
        print type(s)
        url = WADO_SERVER + s.path
        print "downloading " + url
        urllib.urlretrieve(url, "/tmp/name.dcm")
        print "downloaded"
        subprocess.call("dcmscale --scale-x-factor 0.2 /tmp/name.dcm /tmp/name0.2.dcm", shell=True)
        print "transformed"
        s.send_response(200)
        s.send_header("Content-type", "application/dicom")
        s.end_headers()
        s.wfile.write(open("/tmp/name0.2.dcm").read())
        print "sent"


#        print s.path
#        split_path = string.split(s.path,'?')
#        params = {}
#        if len(split_path) > 1:
#            split_params = string.split(split_path[1],'&')
#            print map(lambda x: string.split(x,'='),split_params)
#            try:
#                params = dict(map(lambda x: string.split(x,'='), split_params))
#            except ValueError:
#                params = {}
#            if (params.has_key('_')):
#                del params['_']
##        patient_map = operator.itemgetter('PatientID')(params)
#        post_data = string.replace(str(params), '\'', '"')
#        print post_data
#        answer = urllib.urlopen(CC_SERVER + split_path[0], post_data).read()
#        print answer
#        s.send_response(200)
#        s.send_header("Content-type", "application/json")
#        s.end_headers()
#        s.wfile.write(answer)


#Handler = ServerHandler2

#httpd = SocketServer.TCPServer(("", 8043), Handler)

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ServerHandler2)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    server_class3 = BaseHTTPServer.HTTPServer
    httpd3 = server_class3((HOST_NAME, PORT_NUMBER_WADO_TRANS), ServerHandler3)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER_WADO_TRANS)
    try:
        print "A"
        t1 = threading.Thread(target=httpd.serve_forever)
        t1.start()
        print "B"
        httpd3.serve_forever()
        print "C"
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
    httpd3.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER_WADO_TRANS)