import os
import sys
import json
from random import randint

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    if sender_id == "1373249122789442":
                        send_message(sender_id,"She tells me to stop. It's her father's business. She's Tiffany.I say no.We make love all night.In the morning,the cops come and I escape in one of their uniforms.I tell her to meet me in Mexico,but I go to Canada.I don't trust her.Besides,I like the cold.Thirty years later, I get a postcard.I have a son and he's the chief of police.This is where the story gets interesting.I tell Tiffany to meet me in Paris by the Trocadero.Shes been waiting for me all these years.She's never taken another lover.I don't care. I don't show up.I go to Berlin.That's where I stashed the chandelier.")
                    elif sender_id =="1810559528961492":
                        send_message(sender_id,"fk u Vinay doctor ass")
                    elif sender_id == "1703699106325831":
                        send_message(sender_id," Erlich: You know Aviato? Jack Barker: Yes. Aviato Erlich: My Aviato? Jack Barker: Is there any other Aviato? Erlich: Well, legally, there cannot be.")
                    elif sender_id == "1762176847130980":
                        A = ["I just motor cycled Divya's ass","Fk ur ass Ajay","Meelo,Milo,Moolo","Goddamn Toon Link Lookin Ass"]
                        send_message(sender_id,A[randint(0,len(A)-1)])
                    elif sender_id == "1279391828825420" :
                        A = ["Why Can't You just be nice to me","you have weird hair","your goals in life are pointless","you are a disinteresting person Meghana"]
                        B = ["https://pbs.twimg.com/media/CaEi465VIAARWY2.jpg", "https://pbs.twimg.com/media/C5D-zOAUYAAYOju.jpg", "https://pbs.twimg.com/media/CeB9OzMVIAAO0jH.jpg:large"]
                        send_message(sender_id,A[randint(0,len(A)-1)])
                        send_image(sender_id, B[randint(0,len(B)-1)])
                    else:
                        send_message(sender_id,"LOL lmao " + str(sender_id))
                        
                    pics = ["https://i.ytimg.com/vi/568HWWIfw2Q/maxresdefault.jpg","https://img.haikudeck.com/mg/BE142A84-75ED-402A-BC21-886236F65702.jpg"]
                    prob = randint(0,3)
                    if prob == 1:
                        send_image(sender_id,pics[randint(0,len(pics)-1)])

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)



def send_image(recipient_id, image_url):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=image_url))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"image",
                "payload": {
                    "url": image_url ,
                    "is_reusable":1,
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)



def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
