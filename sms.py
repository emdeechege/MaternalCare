#!/usr/bin/env python
import os
import africastalking


def main():
    africastalking.initialize(os.getenv('USERNAME', 'sandbox'), os.getenv('API_KEY', '95b80a0ea78f7fade739b827fa7d21cdaf2c456d4be794c9a21a623827b9cbff'))
    sms = africastalking.SMS

    def on_finish(error, data):
        if error is not None:
            raise error

        print('\nAsync Done with -> ' + str(data['SMSMessageData']['Message']))

    # Send SMS asynchronously
    sms.send('Hello Async', ['+254724361712'], callback=on_finish)
    print('Waiting for async result....')
    # Send SMS synchronously
    result = sms.send('Hello Sync Test', ['+254724361712'])
    print('\nSync Done with -> ' + result['SMSMessageData']['Message'])


if __name__ == "__main__":
    main()