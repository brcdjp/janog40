#!/usr/bin/env python

import wiringpi as pi
import requests
import time
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


st2host = 'bwc'
api_key =''

#CATCH_DISTANCE = 5
TRIG_PIN = 23
ECHO_PIN = 24

head_top = 10
body_top = 16
leg_top = 25
leg_bottom =40

def init():
    pi.wiringPiSetupGpio()
    pi.pinMode( TRIG_PIN, pi.OUTPUT )
    pi.pinMode( ECHO_PIN, pi.INPUT )
    pi.digitalWrite( TRIG_PIN, pi.LOW )
    time.sleep( 1 )

def main():
    distance = measure()
    if distance > head_top and distance < body_top:
        hit = 'head'
        send(hit)
        break
    elif distance >= body_top and distance < leg_top:
        hit = 'body'
        send(hit)
        break
    elif distance >= leg_top and distance < leg_bottom:
        hit ='leg'
        send(hit)
        break
    else:
        pass
    time.sleep(0.3)

def measure():
    pi.digitalWrite( TRIG_PIN, pi.HIGH )
    time.sleep(0.00001)
    pi.digitalWrite( TRIG_PIN, pi.LOW )
    while ( pi.digitalRead( ECHO_PIN ) == pi.LOW ):
        sigoff = time.time()
    while ( pi.digitalRead( ECHO_PIN ) == 1 ):
        sigon = time.time()
    return (( sigon - sigoff ) * 34000) / 2

def send(hit):
    print(hit)
    response = requests.post(
        'https://'+st2host+'/api/v1/webhooks/janog40',
        headers={'St2-Api-Key':api_key, 'Content-Type':'application/json'},
        json={'hit':hit},verify=False)

if __name__=='__main__':
    init()
    while True:
        main()
