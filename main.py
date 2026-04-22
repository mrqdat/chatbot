import os
import json
import pandas as pd
from dotenv import load_dotenv
from vnstock import Vnstock
import telebot
from ta.momentum import RSIIndicator

# --- Load environment variables ---
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise EnvironmentError(
        "Thiếu biến môi trường. Hãy copy .env.example thành .env và điền giá trị."
    )

bot = telebot.TeleBot(TOKEN)
stock = Vnstock().stock(source="VCI")

# --- Portfolio ---

PORTFOLIO_FILE = os.path.join(os.path.dirname(__file__), "portfolio.json")


def load_portfolio() -> list[dict]:
    """Đọc danh mục cổ phiếu từ portfolio.json."""
    with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# --- Analysis ---

def get_advice(symbol: str) -> str:
    """Phân tích kỹ thuật đơn giản cho mã cổ phiếu."""
    df = stock.trading.history(symbol=symbol, period="1y").tail(50)

    rsi = RSIIndicator(close=df["close"]).rsi().iloc[-1]
    last_close = df["close"].iloc[-1]
    prev_close = df["close"].iloc[-2]

    advice = "GIỮ"
    if rsi > 70:
        advice = "BÁN (Quá mua)"
    elif rsi < 30:
        advice = "MUA (Quá bán)"
    elif last_close > prev_close * 1.05:
        advice = "GIỮ (Đà tăng mạnh)"

    return f"Mã {symbol}: Giá {last_close:,.0f}đ | RSI: {rsi:.2f} | Khuyến nghị: {advice}"


def daily_report() -> str:
    """Tổng hợp báo cáo lãi/lỗ cho toàn bộ danh mục."""
    portfolio = load_portfolio()
    msg = "📊 BÁO CÁO NGÀY:\n"
    for item in portfolio:
        symbol = item["symbol"]
        buy_price = item["buy_price"]
        volume = item.get("volume", 0)

        curr_price = stock.trading.price(symbol=symbol)
        pnl_pct = (curr_price - buy_price) / buy_price * 100
        pnl_vnd = (curr_price - buy_price) * volume

        msg += f"- {symbol}: {pnl_pct:+.2f}% ({pnl_vnd:+,.0f}đ)\n"

    return msg


# --- Telegram handlers ---

@bot.message_handler(commands=["check"])
def send_check(message):
    """Gửi báo cáo danh mục khi nhận lệnh /check."""
    bot.reply_to(message, daily_report())


@bot.message_handler(commands=["advice"])
def send_advice(message):
    """Phân tích mã cổ phiếu. Cú pháp: /advice FPT"""
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "Cú pháp: /advice <MÃ_CK> (ví dụ: /advice FPT)")
        return
    symbol = parts[1].upper()
    bot.reply_to(message, get_advice(symbol))


# --- Entry point ---

if __name__ == "__main__":
    print("🤖 Bot đang chạy...")
    bot.polling(none_stop=True)