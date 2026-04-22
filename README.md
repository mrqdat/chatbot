# 📈 VN Stock Telegram Bot

Bot Telegram phân tích cổ phiếu Việt Nam theo thời gian thực, sử dụng dữ liệu từ **vnstock3** và các chỉ báo kỹ thuật (RSI).

---

## ✨ Tính năng

| Lệnh | Mô tả |
|---|---|
| `/check` | Báo cáo lãi/lỗ toàn bộ danh mục trong `portfolio.json` |
| `/advice <MÃ>` | Phân tích kỹ thuật nhanh (RSI, xu hướng giá) cho một mã cổ phiếu |

---

## 🚀 Cài đặt

### 1. Clone repo

```bash
git clone https://github.com/<your-username>/chatbot.git
cd chatbot
```

### 2. Tạo virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Cài dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình biến môi trường

```bash
cp .env.example .env
```

Mở `.env` và điền thông tin:

```env
TELEGRAM_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

> **Lấy token:** Nhắn tin với [@BotFather](https://t.me/BotFather) trên Telegram → `/newbot`  
> **Lấy Chat ID:** Nhắn tin với [@userinfobot](https://t.me/userinfobot)

### 5. Cấu hình danh mục

Chỉnh sửa `portfolio.json` theo danh mục của bạn:

```json
[
    {"symbol": "FPT", "buy_price": 120.0, "volume": 100},
    {"symbol": "PVT", "buy_price": 24.4,  "volume": 200}
]
```

### 6. Chạy bot

```bash
python main.py
```

---

## 📦 Dependencies

- [vnstock3](https://github.com/thinh-vu/vnstock) — Dữ liệu chứng khoán Việt Nam
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) — Telegram Bot API
- [ta](https://github.com/bukosabino/ta) — Technical Analysis indicators
- [pandas](https://pandas.pydata.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## ⚠️ Lưu ý bảo mật

- **Không bao giờ** commit file `.env` lên GitHub.
- File `.gitignore` đã được cấu hình để bảo vệ `.env` tự động.

---

## 📄 License

MIT
