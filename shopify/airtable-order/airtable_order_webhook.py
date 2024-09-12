import os

import requests
from flask import Flask, request, jsonify
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY')
SHOPIFY_PASSWORD = os.environ.get('SHOPIFY_PASSWORD')
SHOPIFY_SHOP_NAME = os.environ.get('SHOPIFY_SHOP_NAME')
SHOPIFY_API_VERSION = '2023-04'

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME', 'Orders')


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        order_id = request.json['id']

        shopify_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/{SHOPIFY_API_VERSION}/orders/{order_id}.json"
        shopify_response = requests.get(shopify_url, auth=HTTPBasicAuth(SHOPIFY_API_KEY, SHOPIFY_PASSWORD))
        shopify_response.raise_for_status()
        order = shopify_response.json()['order']

        product_count = len(order['line_items'])
        product_info = '|'.join(f"{item.get('sku', 'N/A')}:{item['quantity']}" for item in order['line_items'])

        airtable_data = {
            "fields": {
                "Order ID": order['id'],
                "Order Date": order['created_at'],
                "Total Price": float(order['total_price']),
                "Customer Name": f"{order['customer']['first_name']} {order['customer']['last_name']}",
                "Customer Email": order['customer']['email'],
                "Number of Products": product_count,
                "Product SKUs and Quantities": product_info
            }
        }

        airtable_url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
        headers = {
            "Authorization": f"Bearer {AIRTABLE_API_KEY}",
            "Content-Type": "application/json"
        }
        airtable_response = requests.post(airtable_url, json=airtable_data, headers=headers)
        airtable_response.raise_for_status()

        return jsonify(success=True), 200
    except requests.exceptions.RequestException as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify(success=False, error=str(e)), 500


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 3000)))
