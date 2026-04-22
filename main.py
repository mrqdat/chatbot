import pandas as pd
from vnstock3 import Vnstock
import telebot
from ta.trend import MACD
from ta.momentum import RSIIndicator

TOKEN = '8710054775:AAGfKdJIKFQrOXV8xt-gylV0XHpygkUrkiE'
CHAT_ID = '5717162127'
bot = telebot.TeleBot(TOKEN)
stock = Vnstock().stock(source='VCI') # Hoặc TCBS, SSI

def get_advice(symbol):
    # Lấy dữ liệu 50 phiên gần nhất
    df = stock.trading.history(symbol=symbol, period='1y').tail(50)
    
    # Tính toán chỉ báo
    rsi = RSIIndicator(close=df['close']).rsi().iloc[-1]
    
    # Phân tích nến đơn giản
    last_close = df['close'].iloc[-1]
    prev_close = df['close'].iloc[-2]
    
    advice = "GIỮ"
    if rsi > 70: advice = "BÁN (Quá mua)"
    elif rsi < 30: advice = "MUA (Quá bán)"
    elif last_close > prev_close * 1.05: advice = "GIỮ (Đà tăng mạnh)"
    
    return f"Mã {symbol}: Giá {last_close:,}đ. RSI: {rsi:.2f}. Khuyên: {advice}"

def daily_report():
    # Giả sử bạn đọc file portfolio.json ở đây
    portfolio = [{"symbol": "FPT", "buy_price": 120.0}]
    msg = "📊 BÁO CÁO NGÀY:\n"
    for item in portfolio:
        curr_price = stock.trading.price(symbol=item['symbol'])
        pnl = (curr_price - item['buy_price']) / item['buy_price'] * 100
        msg += f"- {item['symbol']}: {pnl:+.2f}%\n"
    return msg

# Lệnh kiểm tra nhanh
@bot.message_id(['/check'])
def send_check(message):
    bot.reply_to(message, daily_report())

bot.polling()