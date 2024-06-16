import base64
import json
import os
import requests
from fpdf import FPDF, XPos, YPos


def handler(request):
    PRINTNODE_API_KEY = os.getenv('PRINTNODE_API_KEY')
    PRINTNODE_PRINTER_ID = os.getenv('PRINTNODE_PRINTER_ID')

    payload = request['body']

    source_name = payload.get('source_name')
    if source_name.lower() == 'pos':
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'POS order, skipping print job.'})
        }

    # Extract order information from Shopify webhook payload
    order_id = payload.get('id')
    order_total = payload.get('total_price')
    customer = payload.get('customer', {})
    customer_name = customer.get('first_name') + ' ' + customer.get('last_name')
    shipping_address = customer.get('default_address', {})

    # Extracting shipping address details
    shipping_details = f"{shipping_address.get('address1', '')}, {shipping_address.get('city', '')}, {shipping_address.get('province', '')}, {shipping_address.get('country', '')}, {shipping_address.get('zip', '')}"

    order_items = payload.get('line_items', [])

    # Create a PDF document using fpdf2
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    # Add content to PDF
    pdf.cell(200, 10, text=f"Order ID: {order_id}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Order Total: ${order_total}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Customer: {customer_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Shipping Address: {shipping_details}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text="Items:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Items List
    for item in order_items:
        pdf.cell(200, 10, text=f"Item: {item.get('name')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(200, 10, text=f"   - SKU: {item.get('sku')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(200, 10, text=f"   - Quantity: {item.get('quantity')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(200, 10, text=f"   - Price: ${item.get('price')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        if 'variant_id' in item and item['variant_id']:
            pdf.cell(200, 10, text=f"   - Variant ID: {item.get('variant_id')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if 'variant_title' in item and item['variant_title']:
            pdf.cell(200, 10, text=f"   - Variant Name: {item.get('variant_title')}", new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)

    # Save the PDF to a variable
    pdf_output = pdf.output()
    pdf_base64 = base64.b64encode(pdf_output).decode('utf-8')

    print_job_payload = {
        "printerId": PRINTNODE_PRINTER_ID,
        "title": "Shopify Order",
        "contentType": "pdf_base64",
        "content": pdf_base64,
        "source": "Shopify Webhook"
    }

    response = requests.post(
        'https://api.printnode.com/printjobs',
        auth=(PRINTNODE_API_KEY, ''),
        headers={'Content-Type': 'application/json'},
        data=json.dumps(print_job_payload)
    )

    if response.status_code == 201:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Print job sent successfully!'})
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to send print job.', 'error': response.text})
        }
