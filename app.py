from flask import Flask, render_template, request, redirect, url_for, session, flash
import re
import firebase_admin
from firebase_admin import credentials, db
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

cred = credentials.Certificate("iak-pelaporan-969de-firebase-adminsdk-xd4vq-a70f78569d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iak-pelaporan-969de-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Referensi ke path `/users` di Firebase untuk menyimpan data pengguna
user_ref = db.reference('/users')

def fetch_distributor_data():
    api_url = "http://159.223.41.243:8000/api/distributors6"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        distributor_data = response.json()

        if distributor_data:
            print("Data dari API:", distributor_data)
            existing_data = db.reference('/distributor_data').get() or {}

            # Simpan data ke Firebase jika tidak ada data yang sama
            for distributor in distributor_data:
                # Cek apakah data sudah ada
                if not any(
                    existing['kota_asal'] == distributor['kota_asal'] and
                    existing['kota_tujuan'] == distributor['kota_tujuan'] and
                    existing['harga_ongkir_per_kg'] == distributor['harga_ongkir_per_kg']
                    for existing in existing_data.values()
                ):
                    result = db.reference('/distributor_data').push(distributor)
                    print(f'Data berhasil disimpan dengan key: {result.key}')
                else:
                    print(f'Data sudah ada: {distributor}')

            print('Data berhasil diambil dan di simpan ke Firebase')
        else:
            print('Tidak ada data yang diterima dari API')

    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')

def fetch_product_data():
    api_url = "https://suplierman.pythonanywhere.com/products/api/products"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        product_data = response.json()

        if product_data:
            print("Data dari API Produk:", product_data)
            existing_data = db.reference('/products').get() or {}

            # Simpan data ke Firebase jika tidak ada data yang sama
            for product in product_data:
                if not any(
                    existing['id_produk'] == product['id_produk'] for existing in existing_data.values()
                ):
                    result = db.reference('/products').push(product)
                    print(f'Produk berhasil disimpan dengan key: {result.key}')
                else:
                    print(f'Produk sudah ada: {product}')

            print('Data produk berhasil diambil dan disimpan ke Firebase')
        else:
            print('Tidak ada data produk yang diterima dari API')

    except requests.exceptions.RequestException as e:
        print(f'Error fetching product data: {e}')

def fetch_supplier_ban_data():
    api_url = "http://167.99.238.114:8000/api/products"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        product_data = response.json()

        if product_data:
            print("Data dari API Supplier Ban:", product_data)
            existing_data = db.reference('/supplier_ban_products').get() or {}

            # Simpan data ke Firebase jika tidak ada data yang sama
            for product in product_data:
                if not any(
                    existing['id_produk'] == product['id_produk'] for existing in existing_data.values()
                ):
                    result = db.reference('/supplier_ban_products').push(product)
                    print(f'Produk Supplier Ban berhasil disimpan dengan key: {result.key}')
                else:
                    print(f'Produk sudah ada: {product}')

            print('Data produk Supplier Ban berhasil diambil dan disimpan ke Firebase')
        else:
            print('Tidak ada data produk yang diterima dari API Supplier Ban')

    except requests.exceptions.RequestException as e:
        print(f'Error fetching product data from Supplier Ban: {e}')

def fetch_supplier3_data():
    api_url = "https://supplier3.pythonanywhere.com/api/products"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        product_data = response.json()

        if product_data:
            print("Data dari API Supplier 3:", product_data)
            existing_data = db.reference('/supplier3_products').get() or {}

            # Simpan data ke Firebase jika tidak ada data yang sama
            for product in product_data:
                if not any(
                    existing['id_produk'] == product['id_produk'] for existing in existing_data.values()
                ):
                    result = db.reference('/supplier3_products').push(product)
                    print(f'Produk Supplier 3 berhasil disimpan dengan key: {result.key}')
                else:
                    print(f'Produk sudah ada: {product}')

            print('Data produk Supplier 3 berhasil diambil dan disimpan ke Firebase')
        else:
            print('Tidak ada data produk yang diterima dari API Supplier 3')

    except requests.exceptions.RequestException as e:
        print(f'Error fetching product data from Supplier 3: {e}')



def add_dummy_retail_data_1():
    # Dummy data for the first retail store
    dummy_data_1 = {
        "transaction1": {
            "detailed_products": [
                {
                    "name": "Madone",
                    "price": 1000000.0,
                    "quantity": 2,
                    "total_price": 2000000.0
                },
                {
                    "name": "Allant",
                    "price": 500.0,
                    "quantity": 2,
                    "total_price": 1000.0
                }
            ],
            "storeLoc": "bali",
            "storeName": "Sepeda Onthel Skena",
            "timestamp": "Sun, 29 Sep 2024 11:53:09 GMT",
            "total_items": 4,
            "total_transaction_price": 2001000.0,
            "user": "nyk"
        }
    }

    # Save to Firebase
    db.reference('/retail_transactions/store_1').set(dummy_data_1)
    print('Data dummy retail 1 berhasil ditambahkan!')

def add_dummy_retail_data_2():
    # Dummy data for the second retail store
    dummy_data_2 = {
        "transaction1": {
            "detailed_products": [
                {
                    "name": "Trek",
                    "price": 12000.0,
                    "quantity": 1,
                    "total_price": 12000.0
                },
                {
                    "name": "Giant",
                    "price": 8000.0,
                    "quantity": 3,
                    "total_price": 24000.0
                }
            ],
            "storeLoc": "jakarta",
            "storeName": "Toko Sepeda Jakarta",
            "timestamp": "Sun, 29 Sep 2024 11:55:09 GMT",
            "total_items": 4,
            "total_transaction_price": 36000.0,
            "user": "john_doe"
        }
    }

    # Save to Firebase
    db.reference('/retail_transactions/store_2').set(dummy_data_2)
    print('Data dummy retail 2 berhasil ditambahkan!')

def add_dummy_retail_data_3():
    # Dummy data for the third retail store
    dummy_data_3 = {
        "transaction1": {
            "detailed_products": [
                {
                    "name": "Brompton",
                    "price": 30000.0,
                    "quantity": 1,
                    "total_price": 30000.0
                },
                {
                    "name": "Dahon",
                    "price": 15000.0,
                    "quantity": 2,
                    "total_price": 30000.0
                }
            ],
            "storeLoc": "bandung",
            "storeName": "Toko Sepeda Bandung",
            "timestamp": "Sun, 29 Sep 2024 11:57:09 GMT",
            "total_items": 3,
            "total_transaction_price": 60000.0,
            "user": "doe_john"
        }
    }

    # Save to Firebase
    db.reference('/retail_transactions/store_3').set(dummy_data_3)
    print('Data dummy retail 3 berhasil ditambahkan!')

# Route untuk halaman login
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        # Mengambil semua data pengguna dari Firebase
        users = user_ref.get()

        # Memeriksa apakah pengguna ada di database Firebase
        if users:
            for user_id, user_data in users.items():
                if user_data.get('email') == email and user_data.get('password') == password:
                    session['loggedin'] = True
                    session['id'] = user_id  # Menggunakan user_id dari Firebase sebagai session ID
                    session['email'] = user_data.get('email')
                    return redirect(url_for('supplier'))
            msg = 'Incorrect email/password!'
        else:
            msg = 'No users found in the database!'
    return render_template('login.html', msg=msg)

# Route untuk halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Memeriksa apakah email sudah ada di Firebase
        users = user_ref.get()
        if users and any(user.get('email') == email for user in users.values()):
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Menyimpan user baru ke Firebase
            user_ref.push({
                'name': name,
                'email': email,
                'password': password
            })
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('login.html', msg=msg)

# Route untuk logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

# Route untuk halaman Supplier
@app.route('/supplier', methods=['GET', 'POST'])
def supplier():
    if 'loggedin' in session:
        # Default supplier is 'Supplierman'
        selected_supplier = request.form.get('supplier', 'Supplierman')

        if selected_supplier == 'Supplierman':
            fetch_product_data()
            product_data = db.reference('/products').get()
        elif selected_supplier == 'Supplier Ban':
            fetch_supplier_ban_data()
            product_data = db.reference('/supplier_ban_products').get()
        elif selected_supplier == 'Supplier 3':
            fetch_supplier3_data()
            product_data = db.reference('/supplier3_products').get()
        else:
            product_data = []

        # Pastikan product_data bukan None dan konversi ke list
        if product_data is None:
            product_data = []  # Kembalikan list kosong jika tidak ada data
        else:
            product_data = list(product_data.values())

        return render_template('supplier.html', products=product_data, selected_supplier=selected_supplier)
    return redirect(url_for('login'))


# Route untuk halaman Distributor
@app.route('/distributor')
def distributor():
    if 'loggedin' in session:
        fetch_distributor_data()  # Memanggil fungsi di dalam request context
        distributor_data = db.reference('/distributor_data').get()

        # Pastikan distributor_data bukan None dan konversi ke list
        if distributor_data is None:
            distributor_data = []  # Kembalikan list kosong jika tidak ada data
        else:
            # Konversi dict menjadi list
            distributor_data = list(distributor_data.values())

        return render_template('distributor.html', distributor_data=distributor_data)
    return redirect(url_for('login'))

# Route untuk halaman Retail
@app.route('/retail')
def retail():
    if 'loggedin' in session:
        add_dummy_retail_data_1()
        add_dummy_retail_data_2()
        add_dummy_retail_data_3()
        # Mengambil data transaksi dari Firebase
        retail_data = db.reference('/retail_transactions').get() or {}

        # Memproses data untuk visualisasi
        product_summary = { "store_1": {}, "store_2": {}, "store_3": {} }
        total_revenue = { "store_1": 0, "store_2": 0, "store_3": 0 }

        for store_id, transactions in retail_data.items():
            for transaction in transactions.values():
                for product in transaction['detailed_products']:
                    product_name = product['name']
                    product_quantity = product['quantity']
                    product_total_price = product['total_price']

                    # Update store-specific summaries
                    if store_id not in product_summary:
                        product_summary[store_id] = {}

                    if product_name in product_summary[store_id]:
                        product_summary[store_id][product_name]['quantity'] += product_quantity
                        product_summary[store_id][product_name]['total_price'] += product_total_price
                    else:
                        product_summary[store_id][product_name] = {
                            'quantity': product_quantity,
                            'total_price': product_total_price
                        }

                    # Accumulate total revenue for each store
                    total_revenue[store_id] += product_total_price

        # Siapkan data untuk pie chart dan bar chart
        labels = {}
        quantities = {}
        total_prices = {}

        for store_id in product_summary:
            labels[store_id] = list(product_summary[store_id].keys())
            quantities[store_id] = [summary['quantity'] for summary in product_summary[store_id].values()]
            total_prices[store_id] = [summary['total_price'] for summary in product_summary[store_id].values()]

        return render_template(
            'retail.html',
            labels_toko1=labels["store_1"],
            quantities_toko1=quantities["store_1"],
            total_prices_toko1=total_prices["store_1"],
            labels_toko2=labels["store_2"],
            quantities_toko2=quantities["store_2"],
            total_prices_toko2=total_prices["store_2"],
            labels_toko3=labels["store_3"],
            quantities_toko3=quantities["store_3"],
            total_prices_toko3=total_prices["store_3"],
            total_pemasukan_toko1=total_revenue["store_1"],
            total_pemasukan_toko2=total_revenue["store_2"],
            total_pemasukan_toko3=total_revenue["store_3"]
        )
    return redirect(url_for('login'))


# Menjalankan aplikasi Flask dan mengambil data distributor saat dimulai
if __name__ == '__main__':
    app.run(debug=True)
