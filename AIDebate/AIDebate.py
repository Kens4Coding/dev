# Author Kenneth J. Fletcher

DEBUG_FLAG = True
JUST_LIST_AI_AGENTS = False # if true list values for PRO_AGENT/CON_AGENT
MODELS_URL = "https://openrouter.ai/api/v1/models"
CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"

# currently these are both Mixture-of-Experts architecture models
PRO_AGENT = 'google/gemma-4-26b-a4b-it:free'
CON_AGENT = 'openai/gpt-oss-20b:free'

DEBATE_STATEMENT = \
    'The United States should invest heavily in space exploration.'

MAX_LOOPS = 10 # how many back and forths between agents

# Import libraries
import os
import sys
import datetime as dt
import urllib3
import time
import json
import pprint
import random
import warnings
if not DEBUG_FLAG:
    warnings.filterwarnings('ignore')

# Don't request too often (limits for free access)
# also, this will run at a human interface speed
HTTP_THROTTLE = 1 # pause between HTTP GET requests in seconds

global API_KEY

# output txt to the log file and return txt value so that
# all calls to this function can be used to log the values part of
# an assignment statement:
# Example: somvar = o( dataframe[col].mean() , lbl='calc mean of col' )
# Ken!! for this program default echo_print to True
def o( txt , new_line = True  , echo_print=True , lbl=None, \
      new_line_after_lbl = False ):
    global log_file
    if lbl:
        if new_line_after_lbl:
            out = str(lbl) + '\n' + str(txt)
        else:
            out = str(lbl) + ' ' + str(txt)
    else:
        out = str(txt)

    log_file.write( out )
    if (new_line): log_file.write( "\n" )
    if echo_print:
        print( out )
    log_file.flush()
    return(txt)


# setup http communication
http = urllib3.PoolManager()

def http_get(url):
    ret = None
    retry = 2 # retry once
    while retry > 0:
        try:
            ret = http.request('GET',url)
            if HTTP_THROTTLE > 0.0:
                time.sleep(HTTP_THROTTLE)
        except Exception as e:
            o(e,lbl='HTTP GET Exception:',echo_print=True)
            o(url,lbl='URL:',echo_print=True)
        else:
            break
        finally:
            retry -= 1
    return ret

def http_post(url,body,headers):
    ret = None
    retry = 2 # retry once
    while retry > 0:
        try:
            timeout = urllib3.Timeout(connect=5.0,read=20.0)
            ret = http.request('POST',url,body=body,headers=headers,timeout=timeout)
            if HTTP_THROTTLE > 0.0:
                time.sleep(HTTP_THROTTLE)
        except Exception as e:
            o(e,lbl='HTTP POST Exception:',echo_print=True)
            o(url,lbl='URL:',echo_print=True)
        else:
            break
        finally:
            retry -= 1
    return ret


def response_to_dict(response):
    ret = None
    try:
        ret = json.loads(response.data)
    except Exception as e:
        o(e,lbl='Exception:',echo_print=True)
        o(response.data,lbl='Response Data:',echo_print=True)
    return ret

def ask(agent,session,question):
    header = {
        "Authorization":  "Bearer " + API_KEY,
        "Content-Type": "application/json"    
    }

    data = {
        "model" : agent,
        "session_id" : session,
        "messages" : [
            {
                "role" : "user",
                "content" : question
            }
        ]
    }

    response = http_post(CHAT_URL,json.dumps(data),header)
    if response == None:
        raise ValueError('no response in ask: session ' + str(session))
    response = response_to_dict(response)
    ret = response['choices'][0]['message']['content']
    if DEBUG_FLAG:
        o(ret,lbl='Ask Returning')
    return ret



###############################################################################
#__________________ MAIN ______________________________________________________
###############################################################################

# log file name is "executing scripts name" + _log.txt
LOG_FILE_NAME = sys.argv[0].replace('.py','') + '_log.txt'
log_file = open(LOG_FILE_NAME , 'w' ,encoding='utf-8')  

print('Logging output to: ' + LOG_FILE_NAME)

start_script_time = dt.datetime.now()
o("script start time = " + str(start_script_time),echo_print=True)

# My API Key to access openrouter.ai is in a windows enviroment variable

API_KEY = os.environ.get('OPENROUTER_API_KEY', \
    default='No Environmnet Variable Set. This will blow up!')

if API_KEY == 'api_key=No Environmnet Variable Set. This will blow up!':
    print('*********************************')
    print('*********** WARNING *************')
    print('*********************************')
    print('This script uses an API key that must exist in an environment')
    print('variable named OPENROUTER_API_KEY ')
    print('You can obtain your own key for free at openrouter.ai')
    sys.exit(0)


if JUST_LIST_AI_AGENTS:
    response = http_get(MODELS_URL)

    if response == None:
        raise ValueError('no response reading models')
    response_dict = response_to_dict(response)
    response_list = response_dict['data']
    o('Free AI Agents:')
    for agent in response_list:
        if agent['id'].endswith(':free'):
            o('agent =' + agent['id'])
            o('pricing:')
            pprint.pprint(agent['pricing'],stream=log_file)
            o('')
else:
    # lets debate
    o('Debate Statement:')  
    o(DEBATE_STATEMENT)
    pro_session = str(random.randint(10001,10000001))
    con_session = str(random.randint(10001,10000001))
    assert pro_session != con_session,'wow, got same random numbers, start over'

    # prime each agent with the initial question
    pro_response = ask(PRO_AGENT,pro_session, \
        'Why is this statement a good idea?\n' + DEBATE_STATEMENT)
    con_response = ask(CON_AGENT,con_session, \
        'Why is this statement not a good idea?\n' + DEBATE_STATEMENT)

    # for loop in range(MAX_LOOPS):




    


log_file.close()
