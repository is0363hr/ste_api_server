# -*- coding: utf-8 -*-

from flask import Flask, request, abort, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, VideoMessage, StickerMessage, TextSendMessage
)
import os
import sys
import json
from logging import getLogger, config

app = Flask(__name__)

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
with open(ABS_PATH+'/conf.json', 'r') as f:
    CONF_DATA = json.load(f)

CHANNEL_ACCESS_TOKEN = CONF_DATA['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = CONF_DATA['CHANNEL_SECRET']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

config.fileConfig('logging.conf')
logger = getLogger(__name__)

@app.route("/")
def view():
    return render_template("index.html")

@app.route("/test", methods=['GET', 'POST'])
def test():
    return 'I\'m alive!'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Image"))

@handler.add(MessageEvent, message=VideoMessage)
def handle_video(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Video"))

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Sticker"))

if __name__ == "__main__":
    # ポートは今回は9999番を指定
    port = int(os.getenv("PORT", 9999))
    # Flaskはデフォルトだと実行しても外部公開されないので、runの引数にIPとポートを指定する
    app.run(host="0.0.0.0", port=port)