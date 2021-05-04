#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 08:20:01 2021

@author: Deepak Dhole
"""

import requests
import time
from twilio.rest import Client
import datetime

def getStateId(state_name):
    URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    param = {"Accept-Language": "hi_IN"}
    try:
        response = requests.get(url = URL, params = param, verify=False)
        state_details = next(item for item in response.json()['states'] if item["state_name"] == state_name)
        return state_details['state_id']
    except requests.exceptions.RequestException as e:
        print("Error while finding the stateId :", e)

def getDistrictId(state_id, district):
    URL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(state_id)
    param = {"Accept-Language": "hi_IN" }
    try:
        response = requests.get(url = URL, params = param, verify=False)
        district_details = next(item for item in response.json()['districts'] if item['district_name'] == district)
        return district_details['district_id']
    except requests.exceptions.RequestException as e:
        print("Error while finding the districtId:", e)

def findAppointMentByDistrict(district_id, date, age_limit):
    availableSessions = []
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=" +str(district_id) + "&" + "date="+date
    param = {"Accept-Language": "hi_IN" }
    try:
        response = requests.get(url = URL, params = param, verify=False)
        for session in response.json()['sessions']:
            if(session['min_age_limit'] == age_limit):
                availableSessions.append(session)
        return availableSessions
    except requests.exceptions.RequestException as e:
        print("Error while finding the slot :", e)

def sendMessage(msg):
    try:
        client.messages.create(body=str(msg), from_ ="whatsapp:<YOUR TWILIO WHATSAPP NUMBER>", to="whatsapp:<YOUR WHATSAPP NUMBER>" )
    except:
        print("Somenthing went wrong while sending the whatsapp msg")
    
    

state='Maharashtra'
district='Aurangabad '
date="04-05-2021"
age_limit=18

state_id = getStateId(state)
print("The state Id is ",state_id)

district_id = getDistrictId(state_id, district)
print("The district Id is ",district_id)


client = Client("<YOUR TWILIO CLIENT ID>","<YOUR TWILIO AUTH TOKEN>")
while(1):
    print(datetime.datetime.now())
    sendMessage("Trying to find the available slots for Vaccination in " + district )
    availableSessions = []
    availableSessions = findAppointMentByDistrict(district_id, date, age_limit)
    print("Sessions found: ",len(availableSessions))
    msg = []
    if len(availableSessions) > 1:
        for sessions in availableSessions:
            msg.append({'name' : sessions['name'], 'vaccine' : sessions['vaccine'], 'age limit': sessions['min_age_limit'], 'slots': sessions['slots'], 'capacity':sessions['available_capacity']})
        try:
            sendMessage("Finally, slots found!!!")
            for center in msg:
                sendMessage(center)
                time.sleep(10)
        except:
            print("Somenthing went wrong while sending a whatsapp msg")
    else:
        try:
            sendMessage("No slots found, will try again in 20 mins")
        except:
            print("Somenthing went wrong while sending a whatsapp msg")
    
    time.sleep(20*60)