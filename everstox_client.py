import json
import requests
import logging

logger = logging.Logger(__file__)

class EverstoxStoreClient:
    def __init__(self, shop_id: int = 1):
        self.base_url = f"https://api.demo.everstox.com/shops/{shop_id}/orders"

    def send_orders(self, order_data: dict) -> dict:
        """
        Send a single order to Everstox API.
        
        Args:
            order_data: Order in custom JSON format from ShopifyClient.transform_orders_to_custom_json()
        
        Returns:
            API response as dict
        """
        url = self.base_url
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = requests.post(url, headers=headers, json=order_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(str(e))
            return {"error": str(e)}