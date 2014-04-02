# modbus2sql.py
# synchronizes the modbus register with sqlite tables in the following relations:
# di registers -> dichannels
# dochannels -> do registers, di register usage needed for feedback
# ai registers -> aichannels
# aochannels -> ao registers (if any), ai register usage needed for feedback
#setup -> setup registers (close to ao in behaviour)
# 02.04.2014 first tests, tables creation


import time, datetime
import sqlite3
import traceback
import sys
from pymodbus.register_read_message import *

def modbus_connect():
    try: # is it android? using modbustcp then
        import android
        droid = android.Android()
        from android_context import Context
        import android_network # android_network.py and android_utils.py must be present!

        import os.path
        from pymodbus.client.sync import ModbusTcpClient as ModbusClient # modbusTCP

        OSTYPE='android'
        
        tcpport=10502 # modbusproxy
        tcpaddr="127.0.0.1" # localhost ip to use for modbusproxy
        client = ModbusClient(host=tcpaddr, port=tcpport)
        
        import BeautifulSoup # ?
        #import gdata.docs.service
        import termios
        os.chdir('/sdcard/sl4a/scripts/d4c')
        
        msg='running on android, current directory '+os.getcwd()
        print(msg)
        syslog(msg)
        
    except: # some linux
        tcpport=0 # modbus rtu
        
        if 'ARCH' in os.uname()[2]: # if os.environ['PWD'] == '/root':   # olinuxino 
            OSTYPE='archlinux'
            from pymodbus.client.sync import ModbusSerialClient as ModbusClient # using serial modbusRTU
            client = ModbusClient(method='rtu', stopbits=1, bytesize=8, parity='E', baudrate=19200, timeout=0.3, port='/dev/ttyAPP0') # 0.2 oli vahe, lollistus vahel ja jai lolliks
            
            print('running on archlinux')
            os.chdir('/root/d4c') # OLINUXINO
            
            from droidcontroller.indata import InData
            from droidcontroller.comm_system import CommSystem
            from droidcontroller.comm_modbus import CommModbus
            from droidcontroller.webserver import WebServer
            
            tcpport=0 # using pyserial
            tcpaddr='' # no modbustcp address given
            
        elif 'techbase' in os.environ['HOSTNAME']: # npe
            OSTYPE='techbaselinux'
            # kumb (rtu voi tcp) importida, vajab katsetamist
            from pymodbus.client.sync import ModbusSerialClient as ModbusClient # using serial modbusRTU
            client = ModbusClient(method='rtu', stopbits=1, bytesize=8, parity='E', baudrate=19200, timeout=0.3, port='/dev/ttyS3') # 0.2 oli vahe, lollistus vahel ja jai lolliks
            
        else: # ei ole ei android, arch ega techbase
            #OSTYPE=os.environ['OSTYPE'] #  == 'linux': # running on linux, not android
            OSTYPE='linux' # generic
            from pymodbus.client.sync import ModbusTcpClient as ModbusClient # modbusTCP
            client = ModbusClient(host=tcpaddr, port=tcpport) # TCP
            #client = ModbusClient(method='rtu', stopbits=1, bytesize=8, parity='E', baudrate=19200, timeout=0.2, port='/dev/ttyS0') # change if needed
            
            print('running on generic linux')   # argumente vaja!

            try:
                print(sys.argv[1],sys.argv[2]) # <addr:ip> <sql_dir>
            except:
                print('parameters (socket and sql_dir) needed to run on linux!')
                #traceback.print_exc()
                sys.exit()

            try:
                tcpport=int(sys.argv[1].split(':')[1]) # tcpport=502 # std modbusTCP port # set before
                tcpaddr=sys.argv[1].split(':')[0] # "10.0.0.11" # ip to use for modbusTCP
                print('using',tcpaddr,tcpport)
            except:
                msg='invalid address:port '+tcpaddr+':'+str(tcpport)+'  '+str(sys.exc_info()[1])
                print(msg)
                syslog(msg)
                #traceback.print_exc()
                sys.exit()

            #from sqlite3 import dbapi2 as sqlite3 # in linux
            os.chdir(sys.argv[2]) # ('/srv/scada/acomm/sql')
            print(os.getcwd())
           
    
    
    
class Achannels: # also Dchannels and Cchannels below
    ''' Access to io by modbus slave/register addresses and also via services. modbus client must be opened before.
        able to sync input and output channels and accept changes to service members by their sta_reg code
    '''
    def __init__(self, in_sql = 'aichannels.sql', out_sql = 'aochannels.sql', period = 10):
        self.setPeriod(period)
        self.in_sql = in_sql.split('.')[0]
        self.out_sql = out_sql.split('.')[0]
        self.Initialize()

    def setPeriod(self, invar):
        ''' Set the refresh period, executes sync if time from last read was earlier than period ago '''
        self.period = invar

    def Initialize(self):
        ''' initialize delta t variables  '''
        self.ts = time.time()
        self.ts_ai = self.ts
        self.conn = sqlite3.connect(':memory:')
        self.sqlread(self.in_sql) # read aichannels
        self.sqlread(self.out_sql) # read aochannels if exist


    def sqlread(self,table): # drops table and reads from file table.sql that must exist
        if table == self.in_sql or table == self.out_sql: # this table is in this instance
            Cmd='drop table if exists '+table
            filename=table+'.sql' # the file to read from
            try:
                sql = open(filename).read()
            except:
                msg='FAILURE in sqlread: '+str(sys.exc_info()[1]) # aochannels ei pruugi olemas olla alati!
                print(msg)
                #syslog(msg)
                #traceback.print_exc()
                time.sleep(1)
                return 1

            try:
                self.conn.execute(Cmd) # drop the table if it exists
                self.conn.executescript(sql) # read table into database
                self.conn.commit()
                msg='sqlread: successfully recreated table '+table
                print(msg)
                #syslog(msg)
                time.sleep(0.5)
                return 0
            except:
                msg='sqlread: '+str(sys.exc_info()[1])
                print(msg)
                #syslog(msg)
                #traceback.print_exc()
                time.sleep(1)
                return 1


    def dump_table(self,table):
        ''' reads the content of the table, debugging needs only '''
        Cmd ="SELECT * from "+table
        cur = self.conn.cursor()
        cur.execute(Cmd)
        for row in cur:
            print(repr(row))

    def socket_restart(): # close and open tcpsocket
        try: # close if opened
            #print 'closing tcp socket'
            tcpsocket.close()
            time.sleep(1)

        except:
            msg='tcp socket was not open '+str(sys.exc_info()[1])
            print(msg)
            syslog(msg)
            #traceback.print_exc() # debug

        # open a new socket
        try:
            print('opening tcp socket to modbusproxy,',tcpaddr, tcpport)
            tcpsocket = socket(AF_INET,SOCK_STREAM) # tcp / must be reopened if pipe broken, no reusage
            #tcpsocket = socket.socket(AF_INET,SOCK_STREAM) # tcp / must be reopened if pipe broken, no reusage
            tcpsocket.settimeout(5) #  conn timeout for modbusproxy. ready defines another (shorter) timeout after sending!
            tcpsocket.connect((tcpaddr, tcpport)) # leave it connected
            msg='modbusproxy (re)connected at '+str(int(ts))
            print(msg)
            sys.stdout.flush()
            syslog(msg) # log message to file
            #tcperr=0
            return 0

        except:
            msg='modbusproxy reconnection failed '+str(sys.exc_info()[1])
            print(msg)
            syslog(msg) # log message to file
            time.sleep(1)
            return 1


    def read_ai(self): # analogue input readings to sqlite, to be executed regularly.
        locstring="" # local
        mba=0 # lokaalne siin
        val_reg=''
        desc=''
        comment=''
        mcount=0
        block=0 # vigade arv
        self.ts = time.time()
        ts_created=self.ts # selle loeme teenuse ajamargiks
        value=0
        Cmd = ''
        Cmd3= ''

        try:
            Cmd="BEGIN IMMEDIATE TRANSACTION" # hoiab kinni kuni mb suhtlus kestab? teised seda ei kasuta samal ajal nagunii. iga tabel omaette.
            self.conn.execute(Cmd)

            Cmd="select val_reg,count(member) from "+self.in_sql+" group by val_reg"
            cur = self.conn.cursor()
            cur3 = self.conn.cursor()
            cur.execute(Cmd)

            for row in cur: # services
                lisa='' # vaartuste joru
                val_reg=''
                sta_reg=''
                status=0 # esialgu

                val_reg=row[0] # teenuse nimi
                mcount=int(row[1])
                sta_reg=val_reg[:-1]+"S" # nimi ilma viimase symbolita ja S - statuse teenuse nimi, analoogsuuruste ja temp kohta
                svc_name='' # mottetu komment puhvri reale?
                #print 'reading "+self.in_sql+"  values for val_reg',val_reg,'with',mcount,'members' # ajutine
                Cmd3="select * from "+self.in_sql+"  where val_reg='"+val_reg+"'" # loeme yhe teenuse kogu info
                #print Cmd3 # ajutine

                cur3.execute(Cmd3) # another cursor to read the same table

                for srow in cur3: # service members
                    #print repr(srow) # debug
                    mba=-1 #
                    regadd=-1
                    member=0
                    cfg=0
                    x1=0
                    x2=0
                    y1=0
                    y2=0
                    outlo=0
                    outhi=0
                    ostatus=0 # eelmine
                    #tvalue=0 # test, vordlus
                    oraw=0
                    ovalue=0 # previous (possibly averaged) value
                    ots=0 # eelmine ts value ja status ja raw oma
                    avg=0 # keskmistamistegur, mojub alates 2
                    desc=''
                    comment=''
                    # 0       1     2     3     4   5  6  7  8  9    10     11  12    13  14   15     16  17    18
                    #mba,regadd,val_reg,member,cfg,x1,x2,y1,y2,outlo,outhi,avg,block,raw,value,status,ts,desc,comment  # "+self.in_sql+"
                    if srow[0] != '':
                        mba=int(srow[0]) # must be int! will be -1 if empty (setpoints)
                    if srow[1] != '':
                        regadd=int(srow[1]) # must be int! will be -1 if empty
                    val_reg=srow[2] # see on string
                    if srow[3] != '':
                        member=int(srow[3])
                    if srow[4] != '':
                        cfg=int(srow[4]) # konfibait nii ind kui grp korraga, esita hex kujul hiljem
                    if srow[5] != '':
                        x1=int(srow[5])
                    if srow[6] != '':
                        x2=int(srow[6])
                    if srow[7] != '':
                        y1=int(srow[7])
                    if srow[8] != '':
                        y2=int(srow[8])
                    if srow[9] != '':
                        outlo=int(srow[9])
                    if srow[10] != '':
                        outhi=int(srow[10])
                    if srow[11] != '':
                        avg=int(srow[11])  #  averaging strength, values 0 and 1 do not average!
                    if srow[12] != '': # block - loendame siin vigu, kui kasvab yle 3? siis enam ei saada
                        block=int(srow[12])  #
                    if srow[13] != '': #
                        oraw=int(srow[13])
                    if srow[14] != '':
                        ovalue=int(float(srow[14])) # ovalue=int(srow[14])
                    if srow[15] != '':
                        ostatus=int(srow[15])
                    if srow[16] != '':
                        ots=int(srow[16])
                    desc=srow[17]
                    comment=srow[18]


                    if mba>=0 and mba<256 and regadd>=0 and regadd<65536:  # valid mba and regaddr, let's read to update value in "+self.in_sql+"  table
                        msg='reading ai '+str(mba)+'.'+str(regadd)+' for '+val_reg+' m '+str(member) # 'temp skip!'  # ajutine

                        #if respcode == 0: # got  tcpdata as register content. convert to scale.
                        try:
                            result = client.read_holding_registers(address=regadd, count=1, unit=mba)
                            tcpdata = result.registers[0] # reading modbus slave
                            msg=msg+' raw '+str(tcpdata)
                            if mba<5:
                                MBerr[mba]=0

                            if x1 != x2 and y1 != y2: # konf normaalne
                                value=(tcpdata-x1)*(y2-y1)/(x2-x1) # lineaarteisendus
                                value=y1+value

                                #if value == y2: # ebanormaalne analoogsignaali kyllastus
                                #    print 'skipping invalid value, equal to y2',y1
                                #    return 1  # see oli jama!! kp24 hvv naiteks

                                #print 'raw',tcpdata,', ovalue',ovalue, # debug
                                if avg>1 and abs(value-ovalue)<value/2: # keskmistame, hype ei ole suur
                                #if avg>1:  # lugemite keskmistamine vajalik, kusjures vaartuse voib ju ka komaga sailitada!
                                    value=((avg-1)*ovalue+value)/avg # averaging
                                    msg=msg+', averaged '+str(int(value))
                                else: # no averaging for big jumps
                                    if tcpdata == 4096: # this is error result from 12 bit 1wire temperature sensor
                                        value=ovalue # repeat the previous value. should count the errors to raise alarm in the end! counted error result is block, value 3 stps sending.
                                    else: # acceptable non-averaged value
                                        msg=msg+', nonavg value '+str(int(value))

                            else:
                                print("val_reg",val_reg,"member",member,"ai2scale PARAMETERS INVALID:",x1,x2,'->',y1,y2,'value not used!')
                                value=0
                                status=3 # not to be sent status=3! or send member as NaN?

                            print(msg) # temporarely off SIIN YTLEB RAW LUGEMI AI jaoks
                            syslog(msg)

                        except: # else: # failed reading register, respcode>0
                            if mba<5:
                                MBerr[mba]=MBerr[mba]+1 # increase error counter
                            print('failed to read ai mb register', mba,regadd,'skipping "+self.in_sql+"  table update')
                            return 1 # skipping "+self.in_sql+"  update below

                    else:
                        value=ovalue # possible setpoint, ovalue from "+self.in_sql+"  table, no modbus reading for this
                        status=0
                        #print 'setpoint value',value


                    # check the value limits and set the status, acoording to configuration byte cfg bits values
                    # use hysteresis to return from non-zero status values
                    status=0 # initially for each member
                    if value>outhi: # above hi limit
                        if (cfg&4) and status == 0: # warning
                            status=1
                        if (cfg&8) and status<2: # critical
                            status=2
                        if (cfg&12) == 12: #  not to be sent
                            status=3
                            block=block+1 # error count incr
                    else: # return with hysteresis 5%
                        if value>outlo and value<outhi-0.05*(outhi-outlo): # value must not be below lo limit in order for status to become normal
                            status=0 # back to normal
                            block=0 # reset error counter

                    if value<outlo: # below lo limit
                        if (cfg&1) and status == 0: # warning
                            status=1
                        if (cfg&2) and status<2: # critical
                            status=2
                        if (cfg&3) == 3: # not to be sent, unknown
                            status=3
                            block=block+1 # error count incr
                    else: # back with hysteresis 5%
                        if value<outhi and value>outlo+0.05*(outhi-outlo):
                            status=0 # back to normal
                            block=0

                    #print 'status for AI val_reg, member',val_reg,member,status,'due to cfg',cfg,'and value',value,'while limits are',outlo,outhi # debug
                    #"+self.in_sql+"  update with new value and sdatus
                    Cmd3="UPDATE "+self.in_sql+"  set status='"+str(status)+"', value='"+str(value)+"', ts='"+str(int(ts))+"' where val_reg='"+val_reg+"' and member='"+str(member)+"'" # meelde
                    #print Cmd3
                    self.conn.execute(Cmd3) # kirjutamine

            
            self.conn.commit() # "+self.in_sql+"  transaction end
            return 0

        except:
            msg='PROBLEM with "+self.in_sql+"  reading or processing: '+str(sys.exc_info()[1])
            print(msg)
            #syslog(msg)
            traceback.print_exc() # peatub kui sisse jatta
            sys.stdout.flush()
            time.sleep(0.5)

            return 1
        #read_"+self.in_sql+"  end