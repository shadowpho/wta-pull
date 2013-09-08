#!/usr/bin/python3

from html.parser import HTMLParser
import urllib.request,sys,time,math


start_point = [47.643649, -122.142878]
keyword = ['Roundtrip', 'Elevation Gain','Highest Point','Map it']


def haversine(latit1,long1, latit2, long2):
    long1, latit1, long2, latit2 = map(math.radians, [long1, latit1, long2, latit2])
    #some preparation for x,y
    long_d = long2-long1
    latit_d = latit2 - latit1
    a = math.sin(latit_d / 2) ** 2 + math.cos(latit1) * math.cos(latit2) * math.sin(long_d/2)**2
    c = 2 * math.asin(math.sqrt(a))
    dist = 6372.81 * c
    return dist


#used with conjuction with python docs
#simple state machine
#state 
#None = SEARCHING for str0,1,2,3
#name0-3 found 0-3. If find other 0-3 thne ERROR
#
class BestHTMLParser(HTMLParser):
    information = ['','','', '','','','']
    loop = 0
    loop_forward = 0
    state = 'None'
    second_loop = 0
    second_state_machine=0
    def get_info(self):
        return self.information
    def handle_data(self, data):
        self.found = False
        self.loop = self.loop+1
        if(self.loop == 4):
            self.information[0]=data[:-31]
            self.second_state_machine+=1
        for str_choice in keyword:
            if(str_choice in data):  #check if keyword is located in data
#                print('found ' + str_choice + ' on ' + str(self.loop))
                if(self.state!='None'):
                    raise Exception('State machine choked! found '+ str_choice +'but we were looking for ' + str(self.state))
                #no error
                self.state = str_choice
                if(self.state == keyword[3]):
                    self.loop_forward = 9
                else:
                    self.loop_forward = 3
        if(self.loop_forward == 1):
            #FOUND DATA
            #print('found ' + self.state +' ' + data)
            self.information[self.second_state_machine] = data
            self.second_state_machine+=1

            if(self.state is keyword[3]): #found COORDs
                if(self.second_loop==0):
                    self.second_loop=1
                    self.loop_forward=3
                else:                   #found FIRST THREE guys
                    self.state='None'
                    self.loop_forward=0
            else:
                self.state = 'None'
                self.loop_forward=0
        if(self.loop_forward!=0):
            self.loop_forward=self.loop_forward-1

#print('Main')
if(len(sys.argv) < 2):
    print('Usage: ./wta_pull http://etc1 http://etc2')
    sys.exit(5)
full_links = sys.argv[1:]
for http_link in full_links:
    my_parser = BestHTMLParser()
    #print('Opening connection to ' + full_link);
    f = urllib.request.urlopen(http_link)
    #print('Connection Open')
    rec_str = f.read().decode('utf-8')
    #print('Recieved data ' + str(len(rec_str)))
    my_parser.feed(rec_str)
    #print(my_parser.get_info())
    deep_info = my_parser.get_info()

    deep_info[6] = str(0.621371 * haversine(start_point[0], start_point[1],float(deep_info[4]), float(deep_info[5]))) + ' mi'
    print(deep_info)
    time.sleep(1) #don't hammer their site
