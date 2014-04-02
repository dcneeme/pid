import sqlite3
import datetime
import string
import sys
import requests
import traceback

# toimib vist nii py2 kuyi 3 jaoks! 01.03.2014

def get_calendar(mac, days = 3): # query to SUPPORTHOST, returning txt. started by cmd:GCAL too for testing
    # example:   http://www.itvilla.ee/cgi-bin/gcal.cgi?mac=000101000001&days=10
    req = 'http://www.itvilla.ee/cgi-bin/gcal.cgi?mac='+mac+'&days='+str(days)+'&format=json'
    headers={'Authorization': 'Basic YmFyaXg6Y29udHJvbGxlcg=='} # Base64$="YmFyaXg6Y29udHJvbGxlcg==" ' barix:controller
    msg='starting gcal query '+req
    print(msg) # debug
    try:
        response = requests.get(req, headers = headers)
    except:
        msg='gcal query '+req+' failed!'
        traceback.print_exc()
        print(msg)
        #syslog(msg)
        return 1

    events = eval(response.content) # string to list
    print(repr(events)) # debug
    Cmd4 = "BEGIN IMMEDIATE TRANSACTION"
    try:
        #conn4.execute(Cmd4)
        Cmd4="delete from calendar"
        #conn4.execute(Cmd4)
        for event in events:
            print('event',event) # debug
            columns=str(list(event.keys())).replace('[','(').replace(']',')')
            values=str(list(event.values())).replace('[','(').replace(']',')')
            #columns=str(list(event.keys())).replace('{','(').replace('}',')')
            #values=str(list(event.values())).replace('{','(').replace('}',')')
            Cmd4 = "insert into calendar"+columns+" values"+values
            print(Cmd4) # debug
            #conn4.execute(Cmd4)
        #conn4.commit()
        return 0
    except:
        msg='insert to calendar table failed!'
        print(msg)
        #syslog(msg)
        traceback.print_exc() # debug
        return 1
        
        
get_calendar('000101000001')  # test
        