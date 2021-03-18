# Automatically configure Tasmota devices from a script

'''
# Web server commands to Tasmota (Remember to url-encode them):
otaurl  http://192.168.0.15/ota/tasmota-minimal.bin.gz
upgrade 1 
otaurl  http://192.168.0.15/ota/tasmota.bin.gz
upgrade 1
friendlyname1  portico lamp
friendyname2   hall light
http://192.168.4.1/wi?s1=ssid1&p1=pass1&s2=ssid2&p2=pass2&save=   # configure wifi
http://192.168.0.14/cm?cmnd=mqtthost+192.168.0.100                # configure mqtt
http://192.168.0.14/cm?module+0                                   # activate the hard-coded template 
http://192.168.0.14/cm?restart+1                                  # restart tasmota
Online URL encoder:
https://www.urlencoder.org/
'''

import sys
import requests
from time import sleep

LONG_LINE = '-'*65
SHORT_LINE = '-'*40
STAR_LINE = '*'*60

log = None
MAX_ATTEMPTS = 2
DELAY_SEC = 2
CONFIG_FILE = 'config.txt'
LOG_FILE = 'log.txt'

NETWORK_PREFIX = '192.168.'
SLEEP_PREFIX = 'sleep'
COMMENT_PREFIX1 = '//'
COMMENT_PREFIX2 = '#'
COMMENT_START = '/*'
COMMENT_END = '*/'

cmd_url  = None
in_comment = False

device_ip = "localhost:5000"   # run a dummy test server here

def dprint (*args):
    global log
    print (*args)
    log_entry = ' '.join([str(x) for x in args]) + '\n'
    log.write (log_entry)
 
def execute_command (line):
    global device_ip, cmd_url, in_comment
    dprint (line)
    cmd_result = False
    try:
        if (line.startswith (COMMENT_PREFIX1) or line.startswith (COMMENT_PREFIX2)):
            return True
        if (line.startswith (COMMENT_START)):
            in_comment = True
            return True
        if (line.startswith (COMMENT_END)):
            in_comment = False
            return True
        if (in_comment):
            return True            
        if (line.startswith (SLEEP_PREFIX)):
            #sp = line.split(' ')  # multiple spaces spoil the show
            sp = line[len(SLEEP_PREFIX):]
            print (sp)
            sp = sp.strip()
            duration = int(sp)
            if (duration is None or duration < 0 or duration > 120):
                dprint ('Invalid duration.')
            else:
                dprint ('Sleeping for {} seconds.....'.format(duration))
                sleep (duration)
                dprint (SHORT_LINE)
            return True        
        if (line.startswith (NETWORK_PREFIX)):
            device_ip = line  # store it globally for the subsequent commands
            dprint()
            dprint (LONG_LINE)
            dprint ('Device IP: '+device_ip)
            dprint (LONG_LINE)
            cmd_url  = "http://{}/cm".format (device_ip)
            return True
        jcmd = {'cmnd' : line}
        dprint (jcmd)    
        for i in range(MAX_ATTEMPTS):
            try :
                dprint ('(try-{}) connecting to device at {} ..'.format(i+1, device_ip))
                res = requests.get(cmd_url, params=jcmd) 
                #dprint()
                dprint (res.text)
                dprint ('Executed.')
                cmd_result = True
                break
            except Exception as e:
                dprint ('* EXCEPTION: ' + str(e))
                sleep(DELAY_SEC)
        dprint ('\nresult: ' + str(cmd_result))
        dprint ()
        dprint (SHORT_LINE)
    except Exception as e:
        dprint (STAR_LINE)
        dprint ('----->>>>> EXCEPTION !!: '+str(e))
        dprint (STAR_LINE)
    return cmd_result
                            
if (__name__ == '__main__'):
    print ('Opening log file...')
    log = open (LOG_FILE, 'wt')
    if (log is None):
        dprint ('ERROR: could not create log file.')
        sys.exit(1)    
    dprint ('Log file opened.')
 
    script_file = 'script1.txt'
    if len(sys.argv) > 1:
        script_file = sys.argv[1]
    dprint ('Script file: {}'.format(script_file))
    
    lines = None    
    with  open(script_file, 'rt') as f:
        lines = f.readlines() 
    if lines is None:
        dprint ('ERROR: could not read config script {}.'.format(script_file))
        log.flush()
        log.close()     
        sys.exit(1)
    for line in lines:
        line = line.strip()
        if (len(line) == 0):  # ignore blank lines
            continue  
        execute_command (line)
    dprint ('\nClosing log file & signing off.')    
    log.flush()
    log.close()
    print (LONG_LINE) # dprint() will longer work !
    print ('\nConfiguration completed.')
    print ('Please see {} file for issues, if any.'.format(LOG_FILE))
    
    
    