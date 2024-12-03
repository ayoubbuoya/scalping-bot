### Crypto Scalping Bot Documentation

#### **Overview**
A Python bot for crypto scalping using technical indicators. It fetches data from Bybit, analyzes market trends, generates signals, and logs results to an Excel file.

---

#### **Features**
- **Technical Indicators**: RSI, EMA, MACD, Bollinger Bands, Stochastic Oscillator.
- **Signals**: STRONG BUY, BUY, HOLD, SELL, STRONG SELL.
- **Excel Logging**: Saves market data and signals for analysis.
- **Error Handling**: Handles network and API errors.

---

#### **Setup**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/crypto-scalping-bot.git
   cd crypto-scalping-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```env
   BYBIT_API_KEY=your_api_key
   BYBIT_API_SECRET=your_api_secret
   ```

---

#### **Usage**

1. Update parameters in the script:
   - `SYMBOL`: Cryptocurrency pair (e.g., `BTC/USDT`).
   - `TIMEFRAME`: Candlestick timeframe (e.g., `1m`).
   - `INTERVAL`: Fetch interval in seconds.

2. Run the bot:
   ```bash
   python bot.py
   ```

---

#### **Dependencies**
- `ccxt`
- `pandas`
- `ta`
- `openpyxl`
- `dotenv`

Install dependencies with:
```bash
pip install -r requirements.txt
```

---

#### **Future Enhancements**
- Multi-coin support.
- Notifications via email or Telegram.
- Strategy backtesting.

---

#### **License**
Open-source under the [MIT License](LICENSE).