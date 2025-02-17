# Order Fulfillment API
This project demonstrates a simple order fulfillment system. Its goal is to fulfill orders by sending emails containing activation codes and (optionally) creating a fulfillment in Shopify.

## Overview
- **Email Fulfillment**  
When an order is received, the system sends an email to the customer with activation codes.

- **Shopify Fulfillment (Optional)**  
If enabled, the system also creates a fulfillment in Shopify via its API.

## Files
- **main.py** – Flask application exposing a `/fulfill-order` endpoint.
- **helper.py** – Utility functions for drafting emails, sending emails, and fulfilling orders in Shopify.
- **README.md** – This file.

## Setup Instructions
1. **Clone the repository:**  
```
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. **Create and activate a virtual environment:**
```
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
3. **Install dependencies:**
```
pip install flask requests
```
4. **Set environment variables:**

The application requires email credentials and (if using Shopify fulfillment) Shopify credentials. For example:
```
export SENDER_EMAIL="your_email@example.com"
export SENDER_PASSWORD="your_email_password"
export SHOPIFY_SHOP_NAME="yourshop"
export SHOPIFY_API_KEY="your_shopify_api_key"
export SHOPIFY_PASSWORD="your_shopify_password"
```

5. **Run the application:**
```
python main.py
```
The API will be available at `http://localhost:5001`.

## API Usage
Send a `POST` request to `/fulfill-order` with a JSON payload. For example:
```json
{
    "order_number": "ORDER123",
    "customer_email": "customer@example.com",
    "customer_name": "Alice",
    "items": [
        {"Product": "Product A", "ActivationCode": "ABC123"},
        {"Product": "Product B", "ActivationCode": "XYZ789"}
    ],
    "fulfill_shopify": true,
    "shopify_order_id": "123456789",
    "line_items_for_shopify": [
        {"id": 111, "quantity": 1},
        {"id": 222, "quantity": 2}
    ],
    "tracking_info": {
        "tracking_number": "TRACK123",
        "tracking_company": "UPS"
    }
}
```
This will send an email with the activation codes and, if `fulfill_shopify` is true, also attempt to create a fulfillment in Shopify.

## License
This project is licensed under the MIT License.
