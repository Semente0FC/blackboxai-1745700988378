import MetaTrader5 as mt5
import time
import logging
from typing import Optional, Tuple, List, Callable
from dataclasses import dataclass
from datetime import datetime
from configuracoes_avancadas import config

@dataclass
class TradePosition:
    """Data class for trade position information."""
    ticket: int
    type: str
    entry_price: float
    stop_loss: float
    take_profit: float
    volume: float

class TradingStrategy:
    """Base class for trading strategies."""
    
    def __init__(self, symbol: str, timeframe: int, volume: float):
        self.symbol = symbol
        self.timeframe = timeframe
        self.volume = volume
        
    def calculate_signals(self, rates: List[dict]) -> Tuple[bool, bool]:
        """
        Calculate buy and sell signals.
        
        Args:
            rates: List of OHLCV data
            
        Returns:
            Tuple of (buy_signal, sell_signal)
        """
        raise NotImplementedError("Subclasses must implement calculate_signals")

class FutureBreakout(TradingStrategy):
    """
    FutureBreakout trading strategy implementation.
    Uses moving averages and head & shoulders pattern for trade signals.
    """
    
    def __init__(self, symbol: str, volume: float, timeframe: int, logger: Callable):
        """
        Initialize the FutureBreakout strategy.
        
        Args:
            symbol: Trading symbol
            volume: Trading volume
            timeframe: Trading timeframe
            logger: Logging function
        """
        super().__init__(symbol, timeframe, volume)
        self.logger = logger
        self.initial_balance = mt5.account_info().balance
        self.active_position: Optional[TradePosition] = None
        
        logging.info(f"Strategy initialized for {symbol} with {volume} volume")

    def log(self, message: str):
        """Log message with timestamp."""
        timestamp = time.strftime("[%H:%M:%S]")
        self.logger.insert('end', f"{timestamp} {message}\n")
        self.logger.see('end')
        logging.info(f"{self.symbol}: {message}")

    def calculate_moving_average(self, data: List[float], period: int = 20) -> Optional[float]:
        """
        Calculate moving average for given data.
        
        Args:
            data: List of price data
            period: MA period
            
        Returns:
            Moving average value or None if not enough data
        """
        try:
            if len(data) < period:
                return None
            return sum(data[-period:]) / period
        except Exception as e:
            logging.error(f"MA calculation error: {str(e)}")
            return None

    def detect_pattern(self, highs: List[float], lows: List[float]) -> Optional[str]:
        """
        Detect chart patterns.
        
        Args:
            highs: List of high prices
            lows: List of low prices
            
        Returns:
            Pattern type or None if no pattern detected
        """
        try:
            if len(highs) < 7:
                return None

            # Head and Shoulders pattern detection
            left_shoulder = highs[-7]
            head = highs[-5]
            right_shoulder = highs[-3]

            if self._is_head_and_shoulders(left_shoulder, head, right_shoulder):
                return 'head_and_shoulders'

            # Inverse Head and Shoulders pattern detection
            left_valley = lows[-7]
            head_valley = lows[-5]
            right_valley = lows[-3]

            if self._is_inverse_head_and_shoulders(left_valley, head_valley, right_valley):
                return 'inverse_head_and_shoulders'

            return None

        except Exception as e:
            logging.error(f"Pattern detection error: {str(e)}")
            return None

    def _is_head_and_shoulders(self, left: float, head: float, right: float) -> bool:
        """Check for head and shoulders pattern."""
        tolerance = 0.4
        return (head > left and head > right and 
                abs(left - right) < (head - left) * tolerance)

    def _is_inverse_head_and_shoulders(self, left: float, head: float, right: float) -> bool:
        """Check for inverse head and shoulders pattern."""
        tolerance = 0.4
        return (head < left and head < right and 
                abs(left - right) < (left - head) * tolerance)

    def execute(self):
        """Main strategy execution loop."""
        while True:
            try:
                # Check daily target
                if self._check_daily_target():
                    break

                # Get market data
                rates = self._get_market_data()
                if not rates:
                    continue

                # Process market data
                self._process_market_data(rates)

                # Sleep to prevent excessive CPU usage
                time.sleep(5)

            except Exception as e:
                logging.error(f"Strategy execution error: {str(e)}")
                time.sleep(5)

    def _check_daily_target(self) -> bool:
        """Check if daily profit target is reached."""
        try:
            current_balance = mt5.account_info().balance
            profit_percentage = ((current_balance - self.initial_balance) / 
                              self.initial_balance * 100)

            if (config["parar_ao_bater_meta"] and 
                profit_percentage >= config["meta_diaria"]):
                self.log("✅ Daily target reached! Stopping operations.")
                return True

            return False

        except Exception as e:
            logging.error(f"Daily target check error: {str(e)}")
            return False

    def _get_market_data(self) -> Optional[List[dict]]:
        """Get market data from MT5."""
        try:
            rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, 100)
            
            if rates is None or len(rates) < 50:
                self.log("⚠️ Insufficient candles loaded.")
                time.sleep(5)
                return None

            return rates

        except Exception as e:
            logging.error(f"Market data error: {str(e)}")
            return None

    def _process_market_data(self, rates: List[dict]):
        """Process market data and execute trades."""
        try:
            opens = [r['open'] for r in rates]
            highs = [r['high'] for r in rates]
            lows = [r['low'] for r in rates]
            closes = [r['close'] for r in rates]

            current_price = closes[-1]
            spread = (mt5.symbol_info_tick(self.symbol).ask - 
                     mt5.symbol_info_tick(self.symbol).bid)

            if current_price == 0 or spread > 20 * 0.0001:
                self.log("⚡ High spread or invalid price. Waiting...")
                return

            # Calculate indicators
            ma20 = self.calculate_moving_average(closes, 20)
            ma50 = self.calculate_moving_average(closes, 50)
            pattern = self.detect_pattern(highs, lows)

            self.log(
                f"🎯 Price: {current_price:.5f} | "
                f"MA20: {ma20:.5f} | "
                f"MA50: {ma50:.5f} | "
                f"Pattern: {pattern}"
            )

            # Trading logic
            if not self.active_position:
                self._check_entry_signals(closes, ma20, ma50, pattern)
            else:
                self._manage_position(current_price)

        except Exception as e:
            logging.error(f"Data processing error: {str(e)}")

    def _check_entry_signals(self, closes: List[float], ma20: float, 
                           ma50: float, pattern: Optional[str]):
        """Check for entry signals."""
        try:
            if ma20 > ma50:
                if (closes[-2] < ma20 and closes[-1] > closes[-2]):
                    self._open_buy(closes[-1])
            elif ma20 < ma50:
                if (closes[-2] > ma20 and closes[-1] < closes[-2]):
                    self._open_sell(closes[-1])

            if pattern == 'head_and_shoulders':
                self._open_sell(closes[-1])
            elif pattern == 'inverse_head_and_shoulders':
                self._open_buy(closes[-1])

        except Exception as e:
            logging.error(f"Entry signal check error: {str(e)}")

    def _open_buy(self, price: float):
        """Open a buy position."""
        try:
            sl = price - 50 * 0.0001
            tp = price + 100 * 0.0001
            
            ticket = self._send_order(mt5.ORDER_TYPE_BUY, price, sl, tp)
            if ticket:
                self.active_position = TradePosition(
                    ticket=ticket,
                    type='buy',
                    entry_price=price,
                    stop_loss=sl,
                    take_profit=tp,
                    volume=self.volume
                )
                self.log(f"✅ Buy opened at {price:.5f}")

        except Exception as e:
            logging.error(f"Buy order error: {str(e)}")

    def _open_sell(self, price: float):
        """Open a sell position."""
        try:
            sl = price + 50 * 0.0001
            tp = price - 100 * 0.0001
            
            ticket = self._send_order(mt5.ORDER_TYPE_SELL, price, sl, tp)
            if ticket:
                self.active_position = TradePosition(
                    ticket=ticket,
                    type='sell',
                    entry_price=price,
                    stop_loss=sl,
                    take_profit=tp,
                    volume=self.volume
                )
                self.log(f"✅ Sell opened at {price:.5f}")

        except Exception as e:
            logging.error(f"Sell order error: {str(e)}")

    def _send_order(self, order_type: int, price: float, 
                   sl: float, tp: float) -> Optional[int]:
        """Send order to MT5."""
        try:
            if not mt5.symbol_select(self.symbol, True):
                self.log("❌ Symbol selection failed")
                return None

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": self.volume,
                "type": order_type,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": 10,
                "magic": 234000,
                "comment": "Future MT5",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                self.log(f"❌ Order failed: {result.comment}")
                return None

            return result.order

        except Exception as e:
            logging.error(f"Order send error: {str(e)}")
            return None

    def _manage_position(self, current_price: float):
        """Manage open position."""
        try:
            if not self.active_position:
                return

            position = mt5.positions_get(ticket=self.active_position.ticket)
            if not position:
                self.active_position = None
                return

            if config["break_even"]:
                self._check_break_even(current_price)

            if config["trailing"]:
                self._check_trailing_stop(current_price)

        except Exception as e:
            logging.error(f"Position management error: {str(e)}")

    def _check_break_even(self, current_price: float):
        """Check and apply break-even if conditions are met."""
        try:
            min_profit = config["pips_be"] * 0.0001
            offset = config["offset_be"] * 0.0001

            if self.active_position.type == 'buy':
                if current_price >= self.active_position.entry_price + min_profit:
                    new_sl = self.active_position.entry_price + offset
                    self._modify_stop_loss(new_sl)
                    self.log("🔒 Break Even activated for Buy!")

            elif self.active_position.type == 'sell':
                if current_price <= self.active_position.entry_price - min_profit:
                    new_sl = self.active_position.entry_price - offset
                    self._modify_stop_loss(new_sl)
                    self.log("🔒 Break Even activated for Sell!")

        except Exception as e:
            logging.error(f"Break-even check error: {str(e)}")

    def _check_trailing_stop(self, current_price: float):
        """Check and apply trailing stop if conditions are met."""
        try:
            distance = config["pips_trailing_distancia"] * 0.0001
            start = config["pips_trailing_start"] * 0.0001

            if self.active_position.type == 'buy':
                if current_price >= self.active_position.entry_price + start:
                    new_sl = current_price - distance
                    self._modify_stop_loss(new_sl)
                    self.log("🏹 Trailing Stop adjusted for Buy!")

            elif self.active_position.type == 'sell':
                if current_price <= self.active_position.entry_price - start:
                    new_sl = current_price + distance
                    self._modify_stop_loss(new_sl)
                    self.log("🏹 Trailing Stop adjusted for Sell!")

        except Exception as e:
            logging.error(f"Trailing stop check error: {str(e)}")

    def _modify_stop_loss(self, new_sl: float):
        """Modify stop loss level."""
        try:
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": self.symbol,
                "sl": new_sl,
                "tp": self.active_position.take_profit,
                "position": self.active_position.ticket,
            }
            
            result = mt5.order_send(request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                self.active_position.stop_loss = new_sl
            else:
                self.log(f"❌ Stop loss modification failed: {result.comment}")

        except Exception as e:
            logging.error(f"Stop loss modification error: {str(e)}")
