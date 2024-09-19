# Shopify to Airtable Product Sync

This script demonstrates a Python-based integration between Shopify and Airtable, automatically syncing product
information from your Shopify store to an Airtable base using webhooks. When a product is created or updated in Shopify,
the changes are immediately reflected in your Airtable base.

## Features

- Creates or updates product information in Airtable in real-time
- Handles both new products and updates to existing products

## Prerequisites

NOTE: This script uses Flask for a local setup. The code is also available
on [codeupify.com](https://codeupify.com/f/gl9av2maG1) as a serverless function
that is ready to run.

- Python 3.7 or higher installed on your local machine
- A Shopify store with API access
- An Airtable account and base set up

### Shopify Access Token

[Get your Shopify API Key](https://codeupify.com/blog/how-to-get-a-shopify-api-key) with the following API access scopes

- `read_products`

### Airtable API

[Get your Airtable Personal Access Token](https://codeupify.com/blog/get-an-airtable-personal-access-token) with the
following token permissions:

- `data.records:read`
- `data.records:write`
- `schema.bases:read`

### Others

- [Get your Airtable Base ID](https://codeupify.com/blog/how-to-get-airtable-base-id), this is the id of the base you
  want to
  sync your Shopify products to, it generally looks like this `appXXXXXXXXXXXXXX`
- Airtable Table Name - this is a URL encoded table name (e.g., `Test Table` becomes `Test%20Table`)
- Shopify Shop Name - this is the name of your Shopify store, you can get it from the url of your Shopify store (e.g.,
  `https://your-store-name.myshopify.com`)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/codeupify/functions.git
   cd functions/shopify/airtable-product-sync
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install Flask requests python-dotenv
   ```

4. Create a `.env` file in the root directory and add your credentials:
   ```
   SHOPIFY_ACCESS_TOKEN=your_shopify_access_token
   SHOPIFY_SHOP_NAME=your_shop_name
   AIRTABLE_PERSONAL_ACCESS_TOKEN=your_airtable_personal_access_token
   AIRTABLE_BASE_ID=your_airtable_base_id
   AIRTABLE_TABLE_NAME=Products
   ```

## Configuration

1. In your Airtable base, create a table named "Products" with the following fields:
    - Product ID (Text)
    - Title (Text)
    - Description (Long text)
    - Vendor (Text)
    - Product Type (Text)
    - Created At (Date)
    - Updated At (Date)
    - Handle (Text)
    - Status (Text)
    - Tags (Text)
    - Variants (Number)
    - Images (Number)

2. In your Shopify admin panel:
    - Go to Settings > Notifications
    - Scroll down to "Webhooks" and click "Create webhook"
    - Select "Product creation" and "Product update" as events
    - Enter your server's URL as the webhook URL (e.g., `https://your-server.com/webhook/product`)

## Usage

1. Start the Flask server:
   ```
   python airtable_product_sync.py
   ```

2. The server will start running on the specified port (default is 3000).

3. When a product is created or updated in your Shopify store, Shopify will send a webhook to your server, triggering
   the sync process.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.