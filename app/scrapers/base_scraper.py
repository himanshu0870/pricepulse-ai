from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import re

class BaseScraper(ABC):
    @abstractmethod
    def scrape(self, url: str, custom_selectors: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        pass

    @staticmethod
    def clean_price(price_str: Optional[str]) -> Optional[float]:
        if not price_str:
            return None
        cleaned = re.sub(r"[^\d.]", "", price_str.replace(",", ""))
        try:
            return float(cleaned) if cleaned else None
        except ValueError:
            return None
