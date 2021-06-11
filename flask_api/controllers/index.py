from flask import Blueprint, render_template, request, abort
from sqlalchemy.sql import func
from modules.db_controller import DBFunc
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, VideoMessage, StickerMessage, TextSendMessage
)

from config.line_setting import LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN

index_page = Blueprint("index_page", __name__)
db_func = DBFunc()

handler = WebhookHandler(LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

@index_page.route("/")
def index():
    context = {}
    cloud_img_path = db_func.get_latest_img_path()
    cloud_img_time = db_func.get_latest_img_time()
    print(type(cloud_img_time))

    # context["cloud_img_path"] = cloud_img_path.split("./static/")[1]
    context["cloud_img_path"] = cloud_img_path
    context["cloud_img_time"] = cloud_img_time

    return render_template("test.html", **context)


@index_page.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    index_page.logger.info("Request body: " + body)

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