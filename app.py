from flask import Flask, render_template, request, jsonify
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(f"{ticker}.SA")
        info = stock.info
        hist = stock.history(period="7d")
        
        
        img = io.BytesIO()
        plt.figure(figsize=(8,4))
        plt.plot(hist.index, hist['Close'], 'b-o')
        plt.title(f'Variação de {ticker} - 7 dias')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return {
            'nome': info.get('longName', ticker),
            'cotacao': info.get('currentPrice', 'N/A'),
            'grafico': plot_url
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta', methods=['POST'])
def consulta():
    ticker = request.form['ticker'].upper()
    data = get_stock_data(ticker)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)