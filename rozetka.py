import re
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import threading
import logging
import io
import csv

app = Flask(__name__, template_folder='.', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")
skip_out_of_stock = True  # Default state

logging.basicConfig(level=logging.INFO)

def fetch_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        logging.error(f"Error fetching page: {e}")
        return None

def extract_products(soup, skip_out_of_stock):
    products = []
    
    # Select all product elements in the soup
    product_elements = soup.select('.goods-tile')

    for element in product_elements:
        # Check if the product is out of stock
        if skip_out_of_stock and 'goods-tile_state_disabled' in element['class']:
            continue  # Skip this product

        link_element = element.select_one('a[href]')
        if not link_element:
            continue

        link = link_element['href']
        img_element = link_element.select_one('div.goods-tile__picture img')
        name = img_element.get('title', img_element.get('alt', 'N/A')) if img_element else 'N/A'
        price_element = element.select_one('.goods-tile__price-value')
        price = price_element.get_text(strip=True) if price_element else 'N/A'

        products.append({'name': name, 'link': link, 'price': price})

    return products

def get_next_page_url(soup, base_url):
    next_button = soup.select_one('a.pagination__direction--forward')
    if next_button and 'href' in next_button.attrs:
        return urljoin(base_url, next_button['href'])
    return None

def scrape_data(start_url):
    socketio.emit('status', {'message': 'Scraping started...'})
    current_url = start_url

    while current_url:
        soup = fetch_page(current_url)
        if soup is None:
            break
            
        # Call extract_products with the current skip_out_of_stock state
        products = extract_products(soup, skip_out_of_stock)

        socketio.emit('update', {'products': products})
        current_url = get_next_page_url(soup, start_url)

    socketio.emit('status', {'message': 'Scraping finished.'})

@socketio.on('toggle_skip_stock')
def toggle_skip_stock(data):
    global skip_out_of_stock
    skip_out_of_stock = not skip_out_of_stock

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter_products():
    data = request.json
    pattern = data.get('pattern', '').replace('*', '.*')

    regex = re.compile(pattern, re.IGNORECASE)

    filtered_results = {}
    for product in data['products']:
        match = regex.search(product)
        if match:
            filtered_results[product] = match.group(0).strip()

    return jsonify({'filtered_results': filtered_results})

@app.route('/export_csv', methods=['POST'])
def export_csv():
    data = request.json
    output = io.StringIO()  # Use StringIO instead of BytesIO
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Dynamically determine headers based on the keys in the first product
    if data['products']:
        headers = list(data['products'][0].keys())
    else:
        headers = ['Product Name', 'Price', 'Link']

    writer.writerow(headers)

    for product in data['products']:
        row = [product.get(header, '') for header in headers]
        writer.writerow(row)

    output.seek(0)
    # Convert the StringIO object to BytesIO before sending it as a file
    output_bytes = io.BytesIO(output.getvalue().encode('utf-8'))
    return send_file(output_bytes, mimetype='text/csv', download_name='products.csv', as_attachment=True)

@socketio.on('start_scraping')
def start_scraping(data):
    url = data['url']
    threading.Thread(target=scrape_data, args=(url,)).start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
