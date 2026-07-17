"""
Technical indicators calculation module
Supports: RSI, MACD, Bollinger Bands, EMA, SMA, etc.
"""
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from core.logger import setup_logger
from config.settings import INDICATORS_CONFIG

logger = setup_logger(__name__)


class TechnicalIndicators:
    """Technical indicators calculator"""
    
    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> List[float]:
        """
        Calculate Simple Moving Average
        
        Args:
            prices: List of prices
            period: SMA period
        
        Returns:
            List of SMA values
        """
        prices = np.array(prices)
        return np.convolve(prices, np.ones(period) / period, mode='valid').tolist()
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> List[float]:
        """
        Calculate Exponential Moving Average
        
        Args:
            prices: List of prices
            period: EMA period
        
        Returns:
            List of EMA values
        """
        prices = np.array(prices, dtype=float)
        ema = pd.Series(prices).ewm(span=period, adjust=False).mean().tolist()
        return ema
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
        """
        Calculate Relative Strength Index
        
        Args:
            prices: List of prices
            period: RSI period (default 14)
        
        Returns:
            List of RSI values
        """
        prices = np.array(prices, dtype=float)
        deltas = np.diff(prices)
        seed = deltas[:period + 1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100. / (1. + rs)
        
        for i in range(period, len(prices)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
            
            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            rs = up / down
            rsi[i] = 100. - 100. / (1. + rs)
        
        return rsi.tolist()
    
    @staticmethod
    def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[List[float], List[float], List[float]]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            prices: List of prices
            fast: Fast EMA period (default 12)
            slow: Slow EMA period (default 26)
            signal: Signal line period (default 9)
        
        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        prices = np.array(prices, dtype=float)
        ema_fast = pd.Series(prices).ewm(span=fast, adjust=False).mean()
        ema_slow = pd.Series(prices).ewm(span=slow, adjust=False).mean()
        
        macd_line = (ema_fast - ema_slow).tolist()
        signal_line = pd.Series(macd_line).ewm(span=signal, adjust=False).mean().tolist()
        histogram = [m - s for m, s in zip(macd_line, signal_line)]
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2) -> Tuple[List[float], List[float], List[float]]:
        """
        Calculate Bollinger Bands
        
        Args:
            prices: List of prices
            period: BB period (default 20)
            std_dev: Standard deviation multiplier (default 2)
        
        Returns:
            Tuple of (Middle band, Upper band, Lower band)
        """
        prices = np.array(prices, dtype=float)
        sma = pd.Series(prices).rolling(window=period).mean()
        std = pd.Series(prices).rolling(window=period).std()
        
        upper_band = (sma + (std * std_dev)).tolist()
        middle_band = sma.tolist()
        lower_band = (sma - (std * std_dev)).tolist()
        
        return middle_band, upper_band, lower_band
    
    @staticmethod
    def calculate_atr(high: List[float], low: List[float], close: List[float], period: int = 14) -> List[float]:
        """
        Calculate Average True Range
        
        Args:
            high: List of high prices
            low: List of low prices
            close: List of close prices
            period: ATR period (default 14)
        
        Returns:
            List of ATR values
        """
        high = np.array(high, dtype=float)
        low = np.array(low, dtype=float)
        close = np.array(close, dtype=float)
        
        tr1 = high - low
        tr2 = np.abs(high - np.roll(close, 1))
        tr3 = np.abs(low - np.roll(close, 1))
        
        tr = np.maximum(tr1, np.maximum(tr2, tr3))
        atr = pd.Series(tr).rolling(window=period).mean().tolist()
        
        return atr
    
    @staticmethod
    def calculate_stochastic(high: List[float], low: List[float], close: List[float], 
                            k_period: int = 14, d_period: int = 3) -> Tuple[List[float], List[float]]:
        """
        Calculate Stochastic Oscillator
        
        Args:
            high: List of high prices
            low: List of low prices
            close: List of close prices
            k_period: K period (default 14)
            d_period: D period (default 3)
        
        Returns:
            Tuple of (K line, D line)
        """
        high = np.array(high, dtype=float)
        low = np.array(low, dtype=float)
        close = np.array(close, dtype=float)
        
        lowest_low = pd.Series(low).rolling(window=k_period).min()
        highest_high = pd.Series(high).rolling(window=k_period).max()
        
        k_line = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_line = pd.Series(k_line).rolling(window=d_period).mean()
        
        return k_line.tolist(), d_line.tolist()
    
    @staticmethod
    def calculate_roc(prices: List[float], period: int = 12) -> List[float]:
        """
        Calculate Rate of Change
        
        Args:
            prices: List of prices
            period: ROC period (default 12)
        
        Returns:
            List of ROC values
        """
        prices = np.array(prices, dtype=float)
        roc = pd.Series(prices).pct_change(periods=period) * 100
        return roc.tolist()


class IndicatorAnalyzer:
    """Analyze indicators and generate signals"""
    
    def __init__(self):
        self.indicators = TechnicalIndicators()
        self.config = INDICATORS_CONFIG
    
    def analyze_rsi(self, prices: List[float]) -> Dict:
        """
        Analyze RSI and return signal
        
        Returns:
            {
                'rsi': current RSI value,
                'signal': 'buy', 'sell', or 'hold',
                'strength': signal strength (0-100)
            }
        """
        rsi = self.indicators.calculate_rsi(prices, self.config['rsi_period'])
        current_rsi = rsi[-1]
        
        if current_rsi < self.config['rsi_oversold']:
            return {
                'rsi': current_rsi,
                'signal': 'buy',
                'strength': abs(current_rsi - self.config['rsi_oversold'])
            }
        elif current_rsi > self.config['rsi_overbought']:
            return {
                'rsi': current_rsi,
                'signal': 'sell',
                'strength': abs(current_rsi - self.config['rsi_overbought'])
            }
        else:
            return {
                'rsi': current_rsi,
                'signal': 'hold',
                'strength': 0
            }
    
    def analyze_macd(self, prices: List[float]) -> Dict:
        """Analyze MACD and return signal"""
        macd, signal, histogram = self.indicators.calculate_macd(
            prices,
            self.config['macd_fast'],
            self.config['macd_slow'],
            self.config['macd_signal']
        )
        
        current_macd = macd[-1]
        current_signal = signal[-1]
        current_histogram = histogram[-1]
        
        if current_histogram > 0 and current_macd > current_signal:
            return {
                'macd': current_macd,
                'signal': current_signal,
                'histogram': current_histogram,
                'signal_type': 'buy',
                'strength': min(abs(current_histogram), 100)
            }
        elif current_histogram < 0 and current_macd < current_signal:
            return {
                'macd': current_macd,
                'signal': current_signal,
                'histogram': current_histogram,
                'signal_type': 'sell',
                'strength': min(abs(current_histogram), 100)
            }
        else:
            return {
                'macd': current_macd,
                'signal': current_signal,
                'histogram': current_histogram,
                'signal_type': 'hold',
                'strength': 0
            }
    
    def analyze_bollinger_bands(self, prices: List[float]) -> Dict:
        """Analyze Bollinger Bands and return signal"""
        middle, upper, lower = self.indicators.calculate_bollinger_bands(
            prices,
            self.config['bb_period'],
            self.config['bb_std_dev']
        )
        
        current_price = prices[-1]
        current_middle = middle[-1]
        current_upper = upper[-1]
        current_lower = lower[-1]
        
        if current_price < current_lower:
            return {
                'price': current_price,
                'middle': current_middle,
                'upper': current_upper,
                'lower': current_lower,
                'signal': 'buy',
                'position': 'below_lower'
            }
        elif current_price > current_upper:
            return {
                'price': current_price,
                'middle': current_middle,
                'upper': current_upper,
                'lower': current_lower,
                'signal': 'sell',
                'position': 'above_upper'
            }
        else:
            return {
                'price': current_price,
                'middle': current_middle,
                'upper': current_upper,
                'lower': current_lower,
                'signal': 'hold',
                'position': 'between'
            }
