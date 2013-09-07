#!/usr/bin/python3

from html.parser import HTMLParser
import urllib.request


keyword = ['Roundtrip', 'Elevation Gain','Highest Point','BCRT 2010']

#used with conjuction with python docs
#simple state machine
#state 
#None = SEARCHING for str0,1,2,3
#name0-3 found 0-3. If find other 0-3 thne ERROR
#
class BestHTMLParser(HTMLParser):
    loop = 0
    loop_forward = 0
    state = 'None'
    second_loop = 0
    def handle_data(self, data):
        self.found = False
        self.loop = self.loop+1
        for str_choice in keyword:
            if(str_choice in data):  #check if keyword is located in data
#                print('found ' + str_choice + ' on ' + str(self.loop))
                if(self.state!='None'):
                    raise Exception('State machine choked! found '+ str_choice +'but we were looking for ' + str(self.state))
                #no error
                self.state = str_choice
                if(self.state == keyword[3]):
                    self.loop_forward = 6
                else:
                    self.loop_forward = 3
        if(self.loop_forward == 1):
            #FOUND DATA
            print('found ' + self.state +' ' + data)
            #XXX
            if(self.state is keyword[3]):
                if(self.second_loop==0):
                    self.second_loop=1
                    self.loop_forward=3
                else:
                    self.state='None'
                    self.loop_forward=0
            else:
                self.state = 'None'
                self.loop_forward=0
        if(self.loop_forward!=0):
            self.loop_forward=self.loop_forward-1

my_parser = BestHTMLParser()
print('Opening connection to');
f = urllib.request.urlopen('http://www.wta.org/go-hiking/hikes/rainbow-lake-1')
print('Connection Open')
rec_str = f.read().decode('utf-8')
print('Recieved data ' + str(len(rec_str)))

my_parser.feed(rec_str)
