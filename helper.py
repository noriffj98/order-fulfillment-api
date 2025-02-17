import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def draft_activation_email(customer_name, activation_details):
    """
    Compose an email with activation codes.
    activation_details is a list of dicts with keys: "Product" and "ActivationCode".
    """
    subject = "Your Activation Codes"
    html = f"<p>Dear {customer_name},</p>"
    html += "<p>Thank you for your order. Here are your activation codes:</p>"
    html += "<ul>"
    for detail in activation_details:
        html += f"<li>{detail['Product']}: <strong>{detail['ActivationCode']}</strong></li>"
    html += "</ul><p>Best regards,<br>Support Team</p>"
    return subject, html

def send_email(sender, password, recipient, subject, html, smtp_server="smtp.gmail.com", smtp_port=587):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(html, "html"))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())

def shopify_fulfill_order(api_key, password, shop_name, order_id, line_items, tracking_info, api_version="2021-01"):
    """
    Create a fulfillment in Shopify.
    - order_id: Shopify order ID.
    - line_items: List of dictionaries with 'id' and 'quantity'.
    - tracking_info: Dictionary with 'tracking_number' and 'tracking_company'.
    """
    url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}/fulfillments.json"
    auth = (api_key, password)
    payload = {
        "fulfillment": {
            "order_id": order_id,
            "tracking_info": {
                "tracking_number": tracking_info.get("tracking_number", ""),
                "tracking_company": tracking_info.get("tracking_company", "Default Company")
            },
            "line_items": line_items
        }
    }
    response = requests.post(url, json=payload, auth=auth)
    if response.status_code == 201:
        print("Shopify fulfillment created successfully.")
    else:
        print(f"Shopify fulfillment failed: {response.status_code} - {response.text}")
    return response.json()
