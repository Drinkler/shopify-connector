from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ShopMoney(BaseModel):
    amount: str
    currencyCode: str = Field(alias="currencyCode")

class CurrentShippingPriceSet(BaseModel):
    shopMoney: ShopMoney

class Address(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    countryCode: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    country: Optional[str] = None
    provinceCode: Optional[str] = None
    province: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

class CustomAttribute(BaseModel):
    key: str
    value: str

class LineItemNode(BaseModel):
    quantity: int
    sku: Optional[str] = None

class LineItemEdge(BaseModel):
    node: LineItemNode

class LineItems(BaseModel):
    edges: List[LineItemEdge]

class OrderNode(BaseModel):
    id: str
    name: str
    createdAt: datetime
    email: Optional[str] = None
    displayFinancialStatus: str
    displayFulfillmentStatus: str
    paymentGatewayNames: List[str]
    shippingAddress: Optional[Address] = None
    billingAddress: Optional[Address] = None
    currentShippingPriceSet: Optional[CurrentShippingPriceSet] = None
    customAttributes: Optional[List[CustomAttribute]] = None
    lineItems: Optional[LineItems] = None

class OrderEdge(BaseModel):
    node: OrderNode

class PageInfo(BaseModel):
    hasNextPage: bool
    hasPreviousPage: bool
    startCursor: Optional[str] = None
    endCursor: Optional[str] = None

class Orders(BaseModel):
    edges: List[OrderEdge]
    pageInfo: PageInfo

class OrdersData(BaseModel):
    orders: Orders

class ShopifyOrderResponse(BaseModel):
    data: OrdersData