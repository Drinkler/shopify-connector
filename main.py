from shopify_client import ShopifyClient
from everstox_client import EverstoxStoreClient
from dotenv import load_dotenv
import os
import json
import logging

logger = logging.Logger(__file__)

load_dotenv()


def main():
    SHOP_URL = os.getenv("SHOPIFY_SHOP_URL")
    ACCESS_TOKEN = os.getenv("SHOPIFY_API_KEY")

    client = ShopifyClient(shop_url=SHOP_URL, token=ACCESS_TOKEN)
    orders = client.get_orders_last_14_days()

    logger.info("Orders from Shopify collected.")

    everstox_client = EverstoxStoreClient()
    everstox_client.send_orders(orders)


if __name__ == "__main__":
    main()
