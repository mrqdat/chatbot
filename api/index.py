from flask import Flask, request, abort
import telebot
import os
import sys

# Đảm bảo mã hóa UTF-8 cho Windows/Vercel log
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Import biến bot từ main.py. Hàm import này sẽ tự động nạp toàn bộ handler (lệnh)
import main

app = Flask(__name__)
bot = main.bot

@app.route('/webhook', methods=['POST'])
def webhook():
    """Nhận tín hiệu Webhook từ Telegram mỗi khi có người nhắn tin"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)

@app.route('/', methods=['GET'])
def index():
    """Kiểm tra server có đang hoạt động hay không"""
    return 'Bot is running on Vercel Serverless!'
