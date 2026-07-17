"""
Exchange interface using CCXT library
Supports: Bitget, Bybit, OKX and other exchanges
"""
import ccxt
from typing import Dict, List, Optional
from core.logger import setup_logger
from config.settings import EXCHANGE_CONFIG

logger = setup_logger(__name__)


class ExchangeManager:
    """Manages exchange connections and operations"""
    
    def __init__(self, exchange_name: str, testnet: bool = False):
        """
        Initialize exchange manager
        
        Args:
            exchange_name: Name of the exchange (bitget, bybit, okx)
            testnet: Use testnet or mainnet
        """
        self.exchange_name = exchange_name.lower()
        self.testnet = testnet
        self.exchange = self._initialize_exchange()
        logger.info(f"Exchange {self.exchange_name} initialized")
    
    def _initialize_exchange(self) -> ccxt.Exchange:
        """Initialize CCXT exchange instance"""
        if self.exchange_name not in EXCHANGE_CONFIG:
            raise ValueError(f"Unsupported exchange: {self.exchange_name}")
        
        config = EXCHANGE_CONFIG[self.exchange_name].copy()
        if self.testnet:
            config['sandbox'] = True
        
        exchange_class = getattr(ccxt, self.exchange_name)
        return exchange_class(config)
    
    def get_ticker(self, symbol: str) -> Dict:
        """
        Get current ticker information
        
        Args:
            symbol: Trading pair (e.g., BTC/USDT)
        
        Returns:
            Ticker data
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            logger.debug(f"Fetched ticker for {symbol}")
            return ticker
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            raise
    
    def get_ohlcv(self, symbol: str, timeframe: str = '5m', limit: int = 100) -> List:
        """
        Get OHLCV (candle) data
        
        Args:
            symbol: Trading pair
            timeframe: Timeframe (1m, 5m, 15m, 1h, etc.)
            limit: Number of candles to fetch
        
        Returns:
            List of OHLCV data
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            logger.debug(f"Fetched {len(ohlcv)} candles for {symbol} {timeframe}")
            return ohlcv
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {symbol}: {e}")
            raise
    
    def get_balance(self) -> Dict:
        """Get account balance"""
        try:
            balance = self.exchange.fetch_balance()
            logger.debug("Fetched account balance")
            return balance
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            raise
    
    def create_limit_buy_order(self, symbol: str, amount: float, price: float) -> Dict:
        """
        Create a limit buy order
        
        Args:
            symbol: Trading pair
            amount: Order amount
            price: Order price
        
        Returns:
            Order details
        """
        try:
            order = self.exchange.create_limit_buy_order(symbol, amount, price)
            logger.info(f"Created buy order: {symbol} {amount} @ {price}")
            return order
        except Exception as e:
            logger.error(f"Error creating buy order: {e}")
            raise
    
    def create_limit_sell_order(self, symbol: str, amount: float, price: float) -> Dict:
        """
        Create a limit sell order
        
        Args:
            symbol: Trading pair
            amount: Order amount
            price: Order price
        
        Returns:
            Order details
        """
        try:
            order = self.exchange.create_limit_sell_order(symbol, amount, price)
            logger.info(f"Created sell order: {symbol} {amount} @ {price}")
            return order
        except Exception as e:
            logger.error(f"Error creating sell order: {e}")
            raise
    
    def create_market_buy_order(self, symbol: str, amount: float) -> Dict:
        """Create a market buy order"""
        try:
            order = self.exchange.create_market_buy_order(symbol, amount)
            logger.info(f"Created market buy order: {symbol} {amount}")
            return order
        except Exception as e:
            logger.error(f"Error creating market buy order: {e}")
            raise
    
    def create_market_sell_order(self, symbol: str, amount: float) -> Dict:
        """Create a market sell order"""
        try:
            order = self.exchange.create_market_sell_order(symbol, amount)
            logger.info(f"Created market sell order: {symbol} {amount}")
            return order
        except Exception as e:
            logger.error(f"Error creating market sell order: {e}")
            raise
    
    def cancel_order(self, order_id: str, symbol: str) -> Dict:
        """
        Cancel an order
        
        Args:
            order_id: Order ID
            symbol: Trading pair
        
        Returns:
            Cancelled order details
        """
        try:
            order = self.exchange.cancel_order(order_id, symbol)
            logger.info(f"Cancelled order: {order_id}")
            return order
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            raise
    
    def get_orders(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None) -> List:
        """
        Get orders for a symbol
        
        Args:
            symbol: Trading pair
            since: Timestamp in milliseconds
            limit: Maximum number of orders
        
        Returns:
            List of orders
        """
        try:
            orders = self.exchange.fetch_orders(symbol, since=since, limit=limit)
            logger.debug(f"Fetched {len(orders)} orders for {symbol}")
            return orders
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            raise
    
    def get_closed_orders(self, symbol: str, since: Optional[int] = None) -> List:
        """Get closed orders for a symbol"""
        try:
            orders = self.exchange.fetch_closed_orders(symbol, since=since)
            return orders
        except Exception as e:
            logger.error(f"Error fetching closed orders: {e}")
            raise
    
    def get_order(self, order_id: str, symbol: str) -> Dict:
        """Get details of a specific order"""
        try:
            order = self.exchange.fetch_order(order_id, symbol)
            return order
        except Exception as e:
            logger.error(f"Error fetching order {order_id}: {e}")
            raise
