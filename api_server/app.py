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


app = Flask(__name__)


# ファイルから環境変数を取得
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
with open(ABS_PATH+'/.env', 'r') as f:
    CONF_DATA = json.load(f)

channel_secret = CONF_DATA['LINE_CHANNEL_SECRET']
channel_access_token = CONF_DATA['LINE_CHANNEL_ACCESS_TOKEN']


# 環境変数からchannel_secret・channel_access_tokenを取得
# channel_secret = os.environ['LINE_CHANNEL_SECRET']
# channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


# @app.route("/")
# def hello_world():
#     return "hello world!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

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


if __name__ == "__main__":
    app.run()
