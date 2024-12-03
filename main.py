import ccxt
import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
import time
from openpyxl import load_workbook
from dotenv import load_dotenv
import os

#  Load API credentials from .env file
load_dotenv()
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")

# Initialize the Bybit exchange
exchange = ccxt.bybit(
    {
        "apiKey": API_KEY,
        "secret": API_SECRET,
        "enableRateLimit": True,
    }
)

# File path to save Excel file
EXCEL_FILE = "crypto_signals.xlsx"


# Function to fetch market data
def fetch_data(symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(
        ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


# Function to add technical indicators
def add_indicators(df):
    df["rsi"] = RSIIndicator(close=df["close"], window=14).rsi()
    df["ema_short"] = EMAIndicator(close=df["close"], window=9).ema_indicator()
    df["ema_long"] = EMAIndicator(close=df["close"], window=21).ema_indicator()
    macd = MACD(close=df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    bb = BollingerBands(close=df["close"], window=20)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()
    stoch = StochasticOscillator(high=df["high"], low=df["low"], close=df["close"])
    df["stoch_k"] = stoch.stoch()
    df["stoch_d"] = stoch.stoch_signal()
    return df


# Function to generate trading signals
def generate_signal(row):
    score = 0
    if row["rsi"] < 30:
        score += 1
    elif row["rsi"] > 70:
        score -= 1
    if row["close"] < row["bb_lower"]:
        score += 1
    elif row["close"] > row["bb_upper"]:
        score -= 1
    if row["ema_short"] > row["ema_long"]:
        score += 1
    elif row["ema_short"] < row["ema_long"]:
        score -= 1
    if row["stoch_k"] < 20:
        score += 1
    elif row["stoch_k"] > 80:
        score -= 1

    if score >= 3:
        return "STRONG BUY"
    elif score <= -3:
        return "STRONG SELL"
    elif score > 0:
        return "BUY"
    elif score < 0:
        return "SELL"
    else:
        return "HOLD"


# Function to save dataframe to Excel
def save_to_excel(df, file_path):
    try:
        # Check if file exists
        with pd.ExcelWriter(
            file_path, mode="a", engine="openpyxl", if_sheet_exists="overlay"
        ) as writer:
            # If the file exists, append without adding headers again
            df.to_excel(
                writer,
                index=False,
                header=False,
                startrow=writer.sheets["Sheet1"].max_row,
            )
    except FileNotFoundError:
        # Create a new file if it doesn't exist
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, header=True)


# Main bot function
def run_bot(symbol, timeframe, interval=60):
    print("Starting the scalping bot with Excel logging...")
    while True:
        try:
            # Fetch market data
            df = fetch_data(symbol, timeframe)

            # Add indicators
            df = add_indicators(df)

            # Generate signals
            df["signal"] = df.apply(generate_signal, axis=1)

            # Save the dataframe to Excel
            save_to_excel(df, EXCEL_FILE)

            # Get the latest signal
            latest_signal = df.iloc[-1]
            print(
                f"\n{latest_signal['timestamp']}: {symbol} | Price: {latest_signal['close']:.2f} | Signal: {latest_signal['signal']}"
            )

        except ccxt.NetworkError as e:
            print(f"Network error: {e}")
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        # Wait for the next cycle
        time.sleep(interval)


# Configure bot parameters
SYMBOL = "ADA/USDT"  # Cryptocurrency pair to analyze
TIMEFRAME = "1m"  # Timeframe for candlesticks (e.g., 1m, 5m, 1h, 1d)
INTERVAL = 5  # Interval in seconds between each data fetch

# Start the bot
run_bot(SYMBOL, TIMEFRAME, INTERVAL)
