"""
Configuration settings for the trading bot
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Exchange Configuration
EXCHANGE_CONFIG = {
    'bitget': {
        'api_key': os.getenv('BITGET_API_KEY'),
        'secret_key': os.getenv('BITGET_SECRET_KEY'),
        'passphrase': os.getenv('BITGET_PASSPHRASE'),
        'sandbox': False,
        'enableRateLimit': True,
    },
    'bybit': {
        'api_key': os.getenv('BYBIT_API_KEY'),
        'secret_key': os.getenv('BYBIT_SECRET_KEY'),
        'sandbox': False,
        'enableRateLimit': True,
    },
    'okx': {
        'api_key': os.getenv('OKX_API_KEY'),
        'secret_key': os.getenv('OKX_SECRET_KEY'),
        'passphrase': os.getenv('OKX_PASSPHRASE'),
        'sandbox': False,
        'enableRateLimit': True,
    }
}

# Trading Configuration
TRADING_PAIR = os.getenv('TRADING_PAIR', 'BTC/USDT')
EXCHANGE = os.getenv('EXCHANGE', 'bitget').lower()
TESTNET = os.getenv('TESTNET', 'False').lower() == 'true'

# Time Interval (in minutes)
INTERVAL = int(os.getenv('INTERVAL', '5'))

# Grid Trading Parameters
GRID_CONFIG = {
    'levels': int(os.getenv('GRID_LEVELS', '10')),
    'profit_rate': float(os.getenv('GRID_PROFIT_RATE', '0.01')),  # 1% profit per level
    'lower_price': float(os.getenv('GRID_LOWER_PRICE', '45000')),
    'upper_price': float(os.getenv('GRID_UPPER_PRICE', '55000')),
}

# Risk Management
RISK_CONFIG = {
    'max_position_size': float(os.getenv('MAX_POSITION_SIZE', '1000')),
    'stop_loss_percent': float(os.getenv('STOP_LOSS_PERCENT', '2')),
    'take_profit_percent': float(os.getenv('TAKE_PROFIT_PERCENT', '5')),
    'max_positions': 5,
    'position_size_per_trade': 100,
}

# Technical Indicators
INDICATORS_CONFIG = {
    'rsi_period': 14,
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bb_period': 20,
    'bb_std_dev': 2,
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_dir': LOG_DIR,
}

# Database Configuration (Optional)
DATABASE_CONFIG = {
    'trades_db': DATA_DIR / 'trades.db',
    'signals_db': DATA_DIR / 'signals.db',
}
