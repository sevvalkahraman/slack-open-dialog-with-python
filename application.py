#!flask/bin/python
import json
from flask import Flask, Response, request, jsonify, make_response
import requests
from flaskrun import flaskrun
from config import SlackConfig 
from slacker import Slacker
import os
import traceback

application = Flask(__name__)

logWebhookUrl = SlackConfig.LOG_CHANNEL_WEBHOOK
retroWebhookUrl = SlackConfig.RETRO_CHANNEL_WEBHOOK

#Sends a message to the slack channel
def sendSlackChannel(logWebhookUrl, message):
    data = {"text": message} #json.loads(data)
    response = requests.post(logWebhookUrl, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    return "Sonuc : "  + str(response.status_code) + ' -- ' + response.text

#Sends a message to the slack retrobox channel
def sendRetroMessage(logWebhookUrl, userName,  messageDetail, username_allowed = "no" ) :
        api_url = '	https://slack.com/api/chat.postMessage'

        data = ''
        with open('message.txt', encoding='utf-8') as json_file:
            data = json.load(json_file)
            if username_allowed == "yes":
                json_format = json.dumps(data).replace("#user_name", userName).replace("#message_detail", messageDetail)
            else :
                json_format = json.dumps(data).replace("#user_name", "Anonymous").replace("#message_detail", messageDetail)

        res = requests.post(logWebhookUrl, data=json_format, headers={'Content-Type': 'application/json'})
        return str(res) + str(res.content)


@application.route('/interactivePost', methods=['POST'])
def interactivePost() :
    try :
        payload = json.loads(request.form["payload"])

        message = ':mega: *Info:* retro command called. *Command: *' +  str(payload["type"])+  '```' + str(request.form) + '```'
        sendSlackChannel(logWebhookUrl, message)

        # Komut ilk defa çalıştırılıyorsa 
        if payload["type"] == "shortcut" : 
            api_url = 'https://slack.com/api/dialog.open'

            trigger_id = request.form.get('trigger_id')

            dialog = {
                "callback_id": "ryde-46e2b0",
                "title": "Retro Box",
                "submit_label": "Request",
                "notify_on_cancel": True,
                "state": "first_place",
                "elements": [
                    {
                        "type": "textarea",
                        "label": "Anything you can throw in our retro box?",
                        "name": "comment",
                        "placeholder": "Let me think...",
                        "hint" : "Allons-y..."
                    },
                    {
                        "type": "select",
                        "label": "How do you feel?",
                        "name": "feeling",
                        "value": "no_comment",
                        "hint" : "I wish you to be happy....",
                        "options": [
                            {
                            "label": "I feel very good",
                            "value": "so_good"
                            },
                            {
                            "label": "I feel good",
                            "value": "good"
                            },
                            {
                            "label": "So so",
                            "value": "so_so"
                            },{
                            "label": "I feel bad.",
                            "value": "bad"
                            },
                            {
                            "label": "No coomment",
                            "value": "no_comment"
                            } 
                        ]
                    },
                    {
                        "type": "select",
                        "label": "Would you like us to post your username?",
                        "name": "username_allowed",
                        "value": "no",
                        "hint" : "If you say no, everything is between us...",
                        "options": [
                            {
                            "label": "Yes",
                            "value": "yes"
                            },
                            {
                            "label": "No",
                            "value": "no"
                            }
                        ]
                    }
                ]
            }

            api_data = {
                "token": SlackConfig.TOKEN,
                "trigger_id": payload["trigger_id"],
                "dialog": json.dumps(dialog)
            }

            res = requests.post(api_url, data=api_data)
            message = ':mega: *res:* ' + str(res.content)
            sendSlackChannel(logWebhookUrl, message)

        elif payload["type"] == "dialog_submission" : 
            sendRetroMessage(logWebhookUrl, str(payload["user"]["name"]), str(payload["submission"]["comment"]),  str(payload["submission"]["username_allowed"]))
            sendRetroMessage(retroWebhookUrl, str(payload["user"]["name"]), str(payload["submission"]["comment"]),  str(payload["submission"]["username_allowed"]))


        elif payload["type"] == "dialog_cancellation" : 
            message = "CANCELLATION"
            sendSlackChannel(logWebhookUrl, message)

        else :
            message = "NOT UNDERSTOOD"
            sendSlackChannel(logWebhookUrl, message)


    except Exception as error:
        return make_response("Error!" + str(error), 200)

    return  make_response("", 200)


if __name__ == '__main__':
    flaskRun(application)