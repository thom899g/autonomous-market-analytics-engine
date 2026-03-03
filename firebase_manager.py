"""
Firebase Manager for state persistence and real-time data streaming.
CRITICAL: All database operations use firebase-admin as required.
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import json
from config import config

class FirebaseManager:
    """Manages all Firebase interactions for the trading system"""
    
    def __init__(self):
        self._client: Optional[FirestoreClient] = None
        self._initialized = False
        self._initialize_firebase()
        
    def _initialize_firebase(self) -> None:
        """Initialize Firebase connection with error handling"""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(config.firebase.credentials_path)
                firebase_admin.initialize_app(cred, {
                    'projectId': config.firebase.project_id
                })
            
            self._client = firestore.client()
            self._initialized = True
            logging.info("Firebase initialized successfully")
            
        except FileNotFoundError as e:
            logging.error(f"Firebase credentials file not found: {e}")
            raise