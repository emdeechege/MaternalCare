from __future__ import print_function
from decouple import config, Csv
import africastalking

class SMS:
    def __init__(self):
        self.username=config("USERNAME")
        self.api_key=config("API_KEY")
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