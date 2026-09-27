from pydantic import BaseModel
from typing import Literal


class IntentResult(BaseModel):
    intent: Literal[
        "order_status", 
        "order_cancel", 
        "delivery_tracking",
        "delivery_delayed",
        "delivery_address_change",
        "payment_failed",
        "payment_refund",
        "product_information",
        "product_availability",
        "return_request",
        "return_status",
        "unknown"
    ]
    confidence: float
    requires_clarification: bool
    probabilities: dict[str, float]


INTENTS = {
    "order_status": "The customer wants to know the status of an order.",
    "order_cancel": "The customer wants to cancel an order.",
    "delivery_tracking": "The customer wants to track a delivery or discovery where is the order.",
    "delivery_delayed": "The customer says the delivery is delayed.",
    "delivery_address_change": "The customer wants to change the delivery address.",
    "payment_failed": "The payment failed or was declined.",
    "payment_refund": "The customer wants a refund.",
    "product_information": "The customer wants information about a product.",
    "product_availability": "The customer wants to know whether a product is available.",
    "return_request": "The customer wants to return a product.",
    "return_status": "The customer wants to know the status of a return.",
    "unknown": "The message does not clearly match any other intent."
}