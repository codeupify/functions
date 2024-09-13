import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

SHOPIFY_ACCESS_TOKEN = os.environ.get('SHOPIFY_ACCESS_TOKEN')
SHOPIFY_SHOP_NAME = os.environ.get('SHOPIFY_SHOP_NAME')
SHOPIFY_API_VERSION = '2024-07'

AIRTABLE_PERSONAL_ACCESS_TOKEN = os.environ.get('AIRTABLE_PERSONAL_ACCESS_TOKEN')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME', 'Orders')


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        order_id = request.json['id']

        shopify_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/{SHOPIFY_API_VERSION}/orders/{order_id}.json"
        headers = {
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
            "Content-Type": "application/json"
        }
        shopify_response = requests.get(shopify_url, headers=headers)
        if not shopify_response.ok:
            raise requests.exceptions.RequestException(
                f"Shopify error: {shopify_response.status_code}, {shopify_response.text}")

        order = shopify_response.json()['order']

        product_count = len(order['line_items'])
        product_info = '|'.join(f"{item.get('sku', 'N/A')}:{item['quantity']}" for item in order['line_items'])

        airtable_data = {
            "fields": {
                "Order Number": str(order['order_number']),
                "Order Date": datetime.fromisoformat(order['created_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d'),
                "Total Price": float(order['total_price']),
                "Customer Name": f"{order['customer']['first_name']} {order['customer']['last_name']}",
                "Customer Email": order['customer']['email'],
                "Number of Products": product_count,
                "Product SKUs and Quantities": product_info
            }
        }

        airtable_url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
        headers = {
            "Authorization": f"Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        airtable_response = requests.post(airtable_url, json=airtable_data, headers=headers)
        if not airtable_response.ok:
            raise requests.exceptions.RequestException(
                f"Airtable error: {airtable_response.status_code}, {airtable_response.text}")

        return jsonify(success=True), 200
    except requests.exceptions.RequestException as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify(success=False, error=str(e)), 500


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 3000)))
