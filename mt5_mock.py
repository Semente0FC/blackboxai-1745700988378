"""Mock implementation of MetaTrader5 for demonstration purposes."""

import random
from dataclasses import dataclass
from typing import List, Optional, Dict

# Constants
TIMEFRAME_M1 = 1
TIMEFRAME_M5 = 5
TIMEFRAME_M15 = 15
TIMEFRAME_M30 = 30
TIMEFRAME_H1 = 60
TIMEFRAME_H4 = 240
TIMEFRAME_D1 = 1440

ORDER_TYPE_BUY = 0
ORDER_TYPE_SELL = 1
TRADE_ACTION_DEAL = 1
TRADE_ACTION_SLTP = 2
ORDER_TIME_GTC = 1
ORDER_FILLING_IOC = 2
TRADE_RETCODE_DONE = 10009

@dataclass
class Symbol:
    name: str
    description: str
    visible: bool = True
    ask: float = 1.0
    bid: float = 1.0

@dataclass
class AccountInfo:
    balance: float = 10000.0
    equity: float = 10000.0
    margin: float = 0.0
    margin_level: float = 100.0

@dataclass
class OrderResult:
    retcode: int = TRADE_RETCODE_DONE
    order: int = random.randint(1000, 9999)
    comment: str = "Success"

def initialize(server: str = "", login: int = 0, password: str = "") -> bool:
    """Mock MT5 initialization."""
    return True

def shutdown():
    """Mock MT5 shutdown."""
    pass

def symbols_get() -> List[Symbol]:
    """Return mock symbols."""
    return [
        Symbol("EURUSD", "Euro vs US Dollar"),
        Symbol("GBPUSD", "Great Britain Pound vs US Dollar"),
        Symbol("USDJPY", "US Dollar vs Japanese Yen")
    ]

def copy_rates_from_pos(symbol: str, timeframe: int, start_pos: int, count: int) -> List[Dict]:
    """Return mock price data."""
    base_price = 1.2000
    result = []
    for i in range(count):
        price = base_price + random.uniform(-0.0050, 0.0050)
        result.append({
            'time': i,
            'open': price,
            'high': price + random.uniform(0, 0.0020),
            'low': price - random.uniform(0, 0.0020),
            'close': price + random.uniform(-0.0010, 0.0010),
            'tick_volume': random.randint(100, 1000),
            'spread': random.randint(1, 5),
            'real_volume': random.randint(1000, 10000)
        })
    return result

def symbol_info_tick(symbol: str):
    """Return mock tick info."""
    base_price = 1.2000
    class Tick:
        ask = base_price + 0.0001
        bid = base_price
        last = base_price
        volume = random.randint(1, 100)
        time = 0
    return Tick()

def positions_get(ticket: Optional[int] = None) -> List[Dict]:
    """Return mock positions."""
    if ticket:
        return [{
            'ticket': ticket,
            'symbol': 'EURUSD',
            'type': ORDER_TYPE_BUY,
            'volume': 0.1,
            'price_open': 1.2000,
            'sl': 1.1950,
            'tp': 1.2100
        }]
    return []

def order_send(request: Dict) -> OrderResult:
    """Mock order sending."""
    return OrderResult()

def account_info() -> AccountInfo:
    """Return mock account info."""
    return AccountInfo()

def last_error() -> str:
    """Return mock error."""
    return "No error"
