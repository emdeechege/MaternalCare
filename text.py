from __future__ import print_function

import africastalking

class SMS:
    def __init__(self):
        self.username="sandbox"
        self.api_key="95b80a0ea78f7fade739b827fa7d21cdaf2c456d4be794c9a21a623827b9cbff"
        africastalking.initialize(self.username, self.api_key)
        self.sms = africastalking.SMS

    def send_sms_sync(self):
        # Set the numbers you want to send to in international format
        recipients = ["+254792752820"]
        # Set your message
        message = "I'm a lumberjack and it's ok, I sleep all night and I work all day"
        # And send the SMS
        try:
            response = self.sms.send(message, recipients)
            print (response)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))


if __name__ == '__main__':
    SMS().send_sms_sync()