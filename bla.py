call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to="+254792752820",
    from_="+12819904695"
)
print(call.sid)




from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC2e44fb564ebba8182cdaf63567ad1f96"
# Your Auth Token from twilio.com/console
auth_token  = "793ef3e81d5cd992acf2936102017751"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+254792752820",
    from_="+12819904695",
    body="Hello from Amama!")

print(message.sid)

