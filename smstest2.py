#!/usr/bin/python3
# we import the Twilio client from the dependency we just installed

import smsinfo
from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client(smsinfo.sid,smsinfo.token)

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="+56989178591",
                       from_=smsinfo.number,
                       body="Test message dude, logic is the beginning of wisdom not the end!")
