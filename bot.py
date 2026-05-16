from flask import Flask, request
import requests
import json
from datetime import datetime

# ========== CONFIGURATION ==========
HELIUS_API_KEY = "7fc3db8a-f3f0-40a2-91bf-76c7fe75b60c"
TELEGRAM_BOT_TOKEN = "8947303055:AAHVJJ2gtLNy1ViUazgNHzsJKpm3RdP7KAk"
TELEGRAM_CHAT_ID = "8694962656"

# Your tracked wallets with names
WALLETS = {
    "J3dnz2QDVfiouCjWTXowtX9zpNzVp9eQdnTa1P1xMArB": "CUPSEYY",
    "2dsHJfXJgXqDGp4EB2GQuGy9RNqwBhTzaiZ8YDBeQ8tb": "Cutie",
    "DxM1hfY8FQ8dNGrucuJzhJcF8KRbjk8WBwrgKvQ9spPv": "Resell Calendar",
}

# ========== TELEGRAM ==========
def send_telegram(message):
    url = f"https://api.telegram.org/botAAHVJJ2gtLNy1ViUazgNHzsJKpm3RdP7KAk/sendMessage"
    payload = {
        "chat_id": 8694962656,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")

# ========== WEBHOOK ==========
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        
        # Process each transaction
        for tx in data:
            process_transaction(tx)
        
        return "OK", 200
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return "Error", 500

def process_transaction(tx):
    # Get token transfers from this transaction
    token_transfers = tx.get('tokenTransfers', [])
    
    if not token_transfers:
        return
    
    for transfer in token_transfers:
        # Check if money moved TO one of our tracked wallets (BUY)
        to_wallet = transfer.get('toUserAccount', '')
        
        if to_wallet in WALLETS:
            wallet_name = WALLETS[to_wallet]
            token_address = transfer.get('mint', 'Unknown')
            amount = transfer.get('tokenAmount', 0)
            
            # Skip tiny dust amounts
            if float(amount) < 1:
                continue
            
            # Format message
            now = datetime.now().strftime("%H:%M:%S")
            
            message = f"""
<b>🟢 BUY DETECTED</b>

<b>Trader:</b> {wallet_name}
<b>Token:</b> <code>{token_address}</code>
<b>Amount:</b> {amount}
<b>Time:</b> {now}

<a href="https://dexscreener.com/solana/{token_address}">📊 View Chart</a>
            """
            
            send_telegram(message)
            print(f"Alert sent: {wallet_name} bought {token_address}")

# ========== MAIN ==========
if __name__ == '__main__':
    print("🚀 Wallet Tracker Bot Running...")
    print(f"📊 Tracking {len(WALLETS)} wallets")
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 
