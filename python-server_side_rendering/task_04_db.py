from flask import Flask, render_template, request
import json
import csv
import sqlite3

app = Flask(__name__)

# JSON
def read_json():
    with open('products.json') as f:
        return json.load(f)

# CSV
def read_csv():
    data = []
    with open('products.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['price'] = float(row['price'])
            data.append(row)
    return data

# SQL (SQLite)
def read_sql():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, category, price FROM Products")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"id": r[0], "name": r[1], "category": r[2], "price": r[3]}
        for r in rows
    ]


@app.route('/products')
def products():
    source = request.args.get('source')
    product_id = request.args.get('id')

    # source seçimi
    if source == 'json':
        data = read_json()
    elif source == 'csv':
        data = read_csv()
    elif source == 'sql':
        data = read_sql()
    else:
        return render_template('product_display.html', error="Wrong source")

    # id filter
    if product_id:
        product_id = int(product_id)
        filtered = [p for p in data if p['id'] == product_id]

        if not filtered:
            return render_template('product_display.html', error="Product not found")

        data = filtered

    return render_template('product_display.html', products=data)


if __name__ == '__main__':
    app.run(debug=True)
