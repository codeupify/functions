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
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME', 'Products')


def get_shopify_product(product_id):
    url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/{SHOPIFY_API_VERSION}/products/{product_id}.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        raise requests.exceptions.RequestException(
            f"Shopify error: {response.status_code}, {response.text}")

    return response.json()['product']


def sync_product_to_airtable(product):
    airtable_data = {
        "fields": {
            "Product ID": str(product['id']),
            "Title": product['title'],
            "Description": product['body_html'],
            "Vendor": product['vendor'],
            "Product Type": product['product_type'],
            "Created At": datetime.fromisoformat(product['created_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d'),
            "Updated At": datetime.fromisoformat(product['updated_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d'),
            "Handle": product['handle'],
            "Status": product['status'],
            "Tags": ', '.join(product['tags']),
            "Variants": len(product['variants']),
            "Images": len(product['images'])
        }
    }

    airtable_url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"{airtable_url}?filterByFormula={{Product ID}}={product['id']}", headers=headers)
    if not response.ok:
        raise requests.exceptions.RequestException(
            f"Airtable error: {response.status_code}, {response.text}")

    existing_record = response.json()

    if existing_record['records']:
        record_id = existing_record['records'][0]['id']
        response = requests.patch(f"{airtable_url}/{record_id}", json=airtable_data, headers=headers)
    else:
        response = requests.post(airtable_url, json=airtable_data, headers=headers)

    if not response.ok:
        raise requests.exceptions.RequestException(
            f"Airtable error: {response.status_code}, {response.text}")

    return response.json()


@app.route('/webhook/product', methods=['POST'])
def product_webhook():
    webhook_data = request.json
    product_id = webhook_data['id']

    product = get_shopify_product(product_id)

    sync_product_to_airtable(product)

    print(f"Product {product_id} synced successfully")
    return jsonify({"success": True, "message": f"Product {product_id} synced successfully"}), 200


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 3000)))
