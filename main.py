from flask import Flask, request, jsonify
from helper import draft_activation_email, send_email, shopify_fulfill_order
import os

app = Flask(__name__)

@app.route("/fulfill-order", methods=["POST"])
def fulfill_order():
    """
    Endpoint to fulfill an order by:
      1. Sending an email with activation codes.
      2. Optionally fulfilling the order in Shopify.
    
    Expected JSON payload:
    {
        "order_number": "ORDER123",
        "customer_email": "customer@example.com",
        "customer_name": "Alice",
        "items": [
            {"Product": "Product A", "ActivationCode": "ABC123"},
            {"Product": "Product B", "ActivationCode": "XYZ789"}
        ],
        "fulfill_shopify": true,         // optional flag
        "shopify_order_id": "123456789",   // required if fulfill_shopify is true
        "line_items_for_shopify": [        // list of Shopify line items with id and quantity
            {"id": 111, "quantity": 1},
            {"id": 222, "quantity": 2}
        ],
        "tracking_info": {                 // tracking info for Shopify fulfillment
            "tracking_number": "TRACK123",
            "tracking_company": "UPS"
        }
    }
    """
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    customer_email = data.get("customer_email")
    customer_name = data.get("customer_name", "Customer")
    items = data.get("items", [])

    if not customer_email or not items:
        return jsonify({"error": "Missing required fields"}), 400

    # Send activation email
    subject, html = draft_activation_email(customer_name, items)
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")
    if not sender or not password:
        return jsonify({"error": "Email configuration not set"}), 500

    try:
        send_email(sender, password, customer_email, subject, html)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Optionally fulfill order in Shopify
    if data.get("fulfill_shopify"):
        shopify_order_id = data.get("shopify_order_id")
        line_items = data.get("line_items_for_shopify", [])
        tracking_info = data.get("tracking_info", {"tracking_number": "", "tracking_company": "Default Company"})
        shopify_shop_name = os.getenv("SHOPIFY_SHOP_NAME")
        shopify_api_key = os.getenv("SHOPIFY_API_KEY")
        shopify_password = os.getenv("SHOPIFY_PASSWORD")
        if not shopify_shop_name or not shopify_api_key or not shopify_password or not shopify_order_id:
            return jsonify({"error": "Shopify configuration missing"}), 500
        fulfillment_response = shopify_fulfill_order(
            shopify_api_key, shopify_password, shopify_shop_name,
            shopify_order_id, line_items, tracking_info
        )
        print("Shopify fulfillment response:", fulfillment_response)

    return jsonify({"message": "Order fulfilled and email sent."}), 200

if __name__ == "__main__":
    app.run(port=5001)
