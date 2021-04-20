import requests
def getuser():
    user = {'name': 'pavithra@gmail.com',
            'name': 'pavithra@gmail.com',
            'name': 'pavithra@gmail.com',
            'name': 'pavithra@gmail.com'
            }
    return user

MAILER = {
    "hit_url": "https://api.mailgun.net/v3/xxxxxxx.com/messages",
    "API_KEY": "key-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",                   
    "sender_mail": "AWS_admin@aws.com"
}

main_template = """<html>
<head>
</head>
<body>

<h4>User: {}<br> Access Key: {}<br> Secret Key: {}<br> </h4>

</body>
</html>
"""

def send_mail(user, access_json, user_mail):
    subject = "AWS Access Key and Secret Access Key Update"
    user_name = access_json['AccessKey']['UserName']
    access_key = access_json['AccessKey']['AccessKeyId']
    secret_key = access_json['AccessKey']['SecretAccessKey']
    
    message = main_template.format(user_name,access_key,secret_key)
    
    return requests.post(
        MAILER["hit_url"],
        auth=("api", MAILER["API_KEY"]),
        data={"from": MAILER["sender_mail"],
              "to": user_mail,
              "subject": subject,
              "html": message})
