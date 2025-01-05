from flask import Flask, request, jsonify
from coinbase.wallet.client import Client
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Coinbase API bilgileri
API_KEY = os.getenv('COINBASE_API_KEY')
API_SECRET = os.getenv('COINBASE_API_SECRET')
client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        
        # TradingView'dan gelen verileri işle
        action = data.get('action')
        amount = float(data.get('amount', 0))
        
        if action == 'buy':
            # Alış emri
            order = client.buy(
                account_id='primary',  # Ana hesap ID'niz
                amount=str(amount),    # İşlem miktarı
                currency='BTC'         # İşlem yapılacak coin
            )
            return jsonify({'success': True, 'order_id': order.id})
            
        elif action == 'sell':
            # Satış emri
            order = client.sell(
                account_id='primary',
                amount=str(amount),
                currency='BTC'
            )
            return jsonify({'success': True, 'order_id': order.id})
            
        return jsonify({'error': 'Invalid action'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return 'Trading Bot is running!'

if __name__ == '__main__':
    app.run(debug=True)
