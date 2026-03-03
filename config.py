"""
Configuration management for the Autonomous Market Analytics Engine.
All sensitive data is loaded from environment variables.
"""
import os
from typing import Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration for state management"""
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "market-analytics-engine")
    credentials_path: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")
    collection_name: str = os.getenv("FIREBASE_COLLECTION", "trading_sessions")
    
    def validate(self) -> bool:
        """Validate Firebase configuration"""
        if not self.project_id:
            logging.error("FIREBASE_PROJECT_ID environment variable is required")
            return False
        if not os.path.exists(self.credentials_path):
            logging.error(f"Firebase credentials file not found: {self.credentials_path}")
            return False
        return True

@dataclass
class ExchangeConfig:
    """Exchange API configuration"""
    exchange_id: str = os.getenv("EXCHANGE_ID", "binance")
    api_key: str = os.getenv("EXCHANGE_API_KEY", "")
    api_secret: str = os.getenv("EXCHANGE_API_SECRET", "")
    sandbox_mode: bool = os.getenv("SANDBOX_MODE", "True").lower() == "true"
    
    def validate(self) -> bool:
        """Validate exchange configuration"""
        if not self.api_key or not self.api_secret:
            logging.warning("Exchange API credentials not set. Some features may be limited.")
        return True

@dataclass
class TradingConfig:
    """Trading strategy parameters"""
    initial_balance: float = float(os.getenv("INITIAL_BALANCE", "10000.0"))
    max_position_size: float = float(os.getenv("MAX_POSITION_SIZE", "0.1"))  # 10% of portfolio
    stop_loss_pct: float = float(os.getenv("STOP_LOSS_PCT", "0.02"))  # 2%
    take_profit_pct: float = float(os.getenv("TAKE_PROFIT_PCT", "0.05"))  # 5%
    risk_free_rate: float = float(os.getenv("RISK_FREE_RATE", "0.02"))
    
    def validate(self) -> bool:
        """Validate trading parameters"""
        if self.initial_balance <= 0:
            raise ValueError("Initial balance must be positive")
        if not 0 < self.max_position_size <= 1:
            raise ValueError("Max position size must be between 0 and 1")
        return True

@dataclass
class RLConfig:
    """Reinforcement Learning configuration"""
    learning_rate: float = float(os.getenv("RL_LEARNING_RATE", "0.0003"))
    gamma: float = float(os.getenv("RL_GAMMA", "0.99"))
    batch_size: int = int(os.getenv("RL_BATCH_SIZE", "64"))
    buffer_size: int = int(os.getenv("RL_BUFFER_SIZE", "100000"))
    target_update_interval: int = int(os.getenv("TARGET_UPDATE_INTERVAL", "1000"))
    
    def validate(self) -> bool:
        """Validate RL parameters"""
        if not 0 < self.learning_rate < 1:
            raise ValueError("Learning rate must be between 0 and 1")
        if not 0 < self.gamma <= 1:
            raise ValueError("Discount factor must be between 0 and 1")
        return True

class Config:
    """Main configuration class"""
    def __init__(self):
        self.firebase = FirebaseConfig()
        self.exchange = ExchangeConfig()
        self.trading = TradingConfig()
        self.rl = RLConfig()
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.data_refresh_interval = int(os.getenv("DATA_REFRESH_INTERVAL", "60"))  # seconds
        
    def validate_all(self) -> bool:
        """Validate all configurations"""
        try:
            self.firebase.validate()
            self.exchange.validate()
            self.trading.validate()
            self.rl.validate()
            logging.info("All configurations validated successfully")
            return True
        except Exception as e:
            logging.error(f"Configuration validation failed: {e}")
            return False

# Global configuration instance
config = Config()