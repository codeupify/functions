# Shopify to Airtable Order Integration

This script demonstrates a simple integration between Shopify and Airtable, automatically syncing new orders from your
Shopify store to an Airtable base.
Each order is stored as a single row in Airtable, including order details, customer information, and a summary of
products purchased.

## Features

- Listens for new order webhooks from Shopify
- Fetches detailed order information from Shopify API
- Creates a single row in Airtable for each new order

## Prerequisites

NOTE: This script uses Flask for a local setup. The code is also available
on [codeupify.com](https://codeupify.com/f/yMYerkEaOB) as a serverless function
that is ready to run.

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your local machine
- A Shopify store with API access
- An Airtable account and base set up

### Shopify Access Token

[Get your Shopify API Key](https://codeupify.com/blog/how-to-get-a-shopify-api-key) with the following API access scopes

- `read_orders`
- `read_customers`
- `read_products`

### Airtable API

[Get your Airtable Personal Access Token](https://codeupify.com/blog/get-an-airtable-personal-access-token) with the
following token permissions:

- `data.records:write`
- `schema.bases:read`

### Others

- [Get your Airtable Base ID](https://codeupify.com/blog/how-to-get-airtable-base-id), this is the id of the base you
  want to send your orders to, it generally looks like this `appXXXXXXXXXXXXXX`
- Airtable Table Name - this is a URL encoded table name (e.g., `Test Table` becomes `Test%20Table`)
- Shopify Shop Name - this is the name of your Shopify store, you can get it from the url of your Shopify store (e.g.,
  `https://your-store-name.myshopify.com`)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/codeupify/functions.git
   cd functions/shopify/airtable-order-integration
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install Flask requests
   ```

4. Create a `.env` file in the root directory and add your credentials:
   ```
   SHOPIFY_ACCESS_TOKEN=your_shopify_access_token
   SHOPIFY_SHOP_NAME=your_shop_name
   AIRTABLE_PERSONAL_ACCESS_TOKEN=your_airtable_personal_access_token
   AIRTABLE_BASE_ID=your_airtable_base_id
   AIRTABLE_TABLE_NAME=Orders
   ```

# Configuration

1. In your Airtable base, create a table named "Orders" with the following fields:
    - Order Number (Text)
    - Order Date (Date)
    - Total Price (Number)
    - Customer Name (Text)
    - Customer Email (Text)
    - Number of Products (Number)
    - Product SKUs and Quantities (Text)

2. In your Shopify admin panel:
    - Go to Settings > Notifications
    - Scroll down to "Webhooks" and click "Create webhook"
    - Select "Order creation" as the event
    - Enter your server's URL as the webhook URL (e.g., `https://your-server.com/webhook`)

## Usage

1. Start the Flask server:
   ```
   python airtable_order_integration.py
   ```

2. The server will start running on the specified port (default is 3000).

3. When a new order is created in your Shopify store, the webhook will trigger, and the order information will be
   automatically synced to your Airtable base.

## Data Format

The product information is stored in the "Product SKUs and Quantities" field using the following format:

```
SKU1:quantity|SKU2:quantity|SKU3:quantity
```

For example: `ABC123:2|XYZ789:1|DEF456:3`

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.