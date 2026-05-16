from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def health():
    return "Bot is running", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    return "OK", 200

if name == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
