from flask import Flask, render_template, request
import json
import csv

app = Flask(__name__)

# JSON oxuma
def read_json():
    with open('products.json') as f:
        return json.load(f)

# CSV oxuma
def read_csv():
    data = []
    with open('products.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['price'] = float(row['price'])
            data.append(row)
    return data


@app.route('/products')
def products():
    source = request.args.get('source')
    product_id = request.args.get('id')

    if source == 'json':
        data = read_json()
    elif source == 'csv':
        data = read_csv()
    else:
        return render_template('product_display.html', error="Wrong source")

    if product_id:
        product_id = int(product_id)
        filtered = [p for p in data if p['id'] == product_id]

        if not filtered:
            return render_template('product_display.html', error="Product not found")

        data = filtered

    return render_template('product_display.html', products=data)


if __name__ == '__main__':
    app.run(debug=True)
