import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from models import ShopifyOrderResponse, OrderNode
import logging

logger = logging.Logger(__file__)

class ShopifyClient:
    def __init__(self, shop_url: str, token: str, api_version: str = "2025-07"):
        self.endpoint = f"https://{shop_url}/admin/api/{api_version}/graphql.json"
        self.session = requests.Session()
        self.session.headers.update({
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json",
        })

    def get_orders_last_14_days(self, first: int = 250) -> ShopifyOrderResponse:
        """
        Fetches all orders from the last 14 days with automatic pagination.
        
        Args:
            first: Number of orders per page (max 250)
        
        Returns:
            ShopifyOrderResponse with all orders across all pages
        """

        fourteen_days_ago = (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%SZ")
        query_string = (
            f"created_at:>={fourteen_days_ago} "
            "financial_status:paid "
            "fulfillment_status:unfulfilled"
        )

        all_orders = []
        cursor = None

        while True:
            response = self._fetch_orders_page(query_string, first, cursor)
            
            if not response or "data" not in response:
                break

            orders_data = response["data"]["orders"]
            edges = orders_data.get("edges", [])
            
            # Add orders from this page
            all_orders.extend(edges)
            
            # Check if there are more pages
            page_info = orders_data.get("pageInfo", {})
            if not page_info.get("hasNextPage", False):
                break
                
            # Get cursor for next page
            cursor = page_info.get("endCursor")
            if not cursor:
                break

        # Create response with all orders and final page info
        combined_response = {
            "data": {
                "orders": {
                    "edges": all_orders,
                    "pageInfo": {
                        "hasNextPage": False,
                        "hasPreviousPage": len(all_orders) > 0,
                        "startCursor": all_orders[0].get("cursor") if all_orders else None,
                        "endCursor": all_orders[-1].get("cursor") if all_orders else None
                    }
                }
            }
        }
        
        return ShopifyOrderResponse(**combined_response)

    def _fetch_orders_page(self, query_string: str, first: int, cursor: Optional[str] = None):
        """
        Fetches a single page of orders.
        
        Args:
            query_string: The search query string
            first: Number of orders to fetch
            cursor: Pagination cursor (None for first page)
        
        Returns:
            GraphQL response for this page
        """
        query = """
        query ($query: String, $first: Int, $after: String) {
          orders(query: $query, first: $first, after: $after, sortKey: CREATED_AT) {
            edges {
              node {
                id
                name
                createdAt
                email
                displayFinancialStatus
                displayFulfillmentStatus
                paymentGatewayNames
                shippingAddress {
                  firstName
                  lastName
                  countryCode
                  city
                  zip
                  address1
                  address2
                  company
                  phone
                  name
                  country
                  provinceCode
                  province
                  longitude
                  latitude
                }
                billingAddress {
                  firstName
                  lastName
                  countryCode
                  city
                  zip
                  address1
                  address2
                  company
                  phone
                  name
                  country
                  provinceCode
                  province
                  longitude
                  latitude
                }
                currentShippingPriceSet {
                  shopMoney {
                    amount
                    currencyCode
                  }
                }
                customAttributes {
                  key
                  value
                }
                lineItems(first: 10) {
                  edges {
                    node {
                      quantity
                      sku
                    }
                  }
                }
              }
            }
            pageInfo {
                hasNextPage
                hasPreviousPage
                startCursor
                endCursor
            }
          }
        }
        """
        
        variables = {
            "query": query_string,
            "first": first,
            "after": cursor
        }
        
        try:
            response = self.session.post(self.endpoint, json={"query": query, "variables": variables})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching orders page: {e}")
            return None
