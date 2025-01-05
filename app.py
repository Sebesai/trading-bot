from flask import Flask, request, jsonify
from coinbase.wallet.client import Client
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Coinbase API bilgileri
API_KEY = os.getenv('COINBASE_API_KEY')
API_SECRET = os.getenv('COINBASE_API_SECRET')

# Client oluşturma
client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json

        # TradingView'dan gelen verileri işle
        action = data.get('action')
        amount = float(data.get('amount', 0))

        # Ana hesabı al
        primary_account = client.get_primary_account()

        if action == 'buy':
            # Alış emri
            buy = primary_account.buy(
                amount=str(amount),
                currency="BTC"
            )
            return jsonify({'success': True, 'order_id': buy.id})

        elif action == 'sell':
            # Satış emri
            sell = primary_account.sell(
                amount=str(amount),
                currency="BTC"
            )
            return jsonify({'success': True, 'order_id': sell.id})

        return jsonify({'error': 'Invalid action'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
