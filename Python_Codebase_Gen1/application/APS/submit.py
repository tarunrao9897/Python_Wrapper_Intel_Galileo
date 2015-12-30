# -*- coding: utf-8 -*-

import os
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
import time 
from datetime import datetime

define("port", default=8000, help="run on the given port", type=int)




class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html' )
    def post(self):
        self.render('index.html')
class confirmPageHandler(tornado.web.RequestHandler):
    def post(self):
#        pinsetup('46','out','0')
#        pinsetup('31','out','1')
#        pinsetup('30','out','0')
        strDT = time.strftime('%Y-%m-%d %X',time.localtime()) 
        port = self.get_argument('port')
        state = self.get_argument('state')
        dt = strDT
        if state == "ON":
            pinsetup('3','out','1')
            pinsetup('39','out','1')
        elif state == "OFF":
            pinsetup('3','out','0')
            pinsetup('39','out','0')
#        else:
#            pinsetup('3','out','0')            


        self.render('confirm.html', port=port, state=state,dt=dt )


def pinsetup(pinexp,pindir,pinval):
    strexport=("echo \"%s\" > /sys/class/gpio/export" % pinexp)  
    strdir=("echo \"%s\" > /sys/class/gpio/gpio%s/direction" % (pindir,pinexp))
    strval=("echo \"%s\" > /sys/class/gpio/gpio%s/value" % (pinval,pinexp)) 
    #os.system("echo \"46\" > D:\TEST.TXT") ;
    os.system(strexport)               #write a "30" to the export file, which reserves gpio30 for use
    os.system(strdir)  #sets gpio30 as an output
    os.system(strval)         #sets gpio30 low, enable dir_out
    print strexport
    print strdir
    print strval

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/confirm', confirmPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
