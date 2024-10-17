
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Connect to the SQLite database (inventory.db will be created automatically)
def connect_db():
    conn = sqlite3.connect('inventory.db')
    return conn

# Create the inventory table if it doesn't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Run this function when the app starts
create_table()
# GET all inventory items
@app.route('/inventory', methods=['GET'])
def get_inventory():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    items = cursor.fetchall()
    conn.close()

    return jsonify([{'id': item[0], 'name': item[1], 'quantity': item[2], 'price': item[3]} for item in items])

# GET a specific inventory item by ID
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()

    if item:
        return jsonify({'id': item[0], 'name': item[1], 'quantity': item[2], 'price': item[3]})
    else:
        return jsonify({'error': 'Item not found'}), 404

# POST (Create) a new inventory item
@app.route('/inventory', methods=['POST'])
def create_item():
    new_item = request.get_json()

    name = new_item['name']
    quantity = new_item['quantity']
    price = new_item['price']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Item added successfully!'}), 201

# PUT (Update) an inventory item by ID
@app.route('/inventory/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_item = request.get_json()

    name = updated_item['name']
    quantity = updated_item['quantity']
    price = updated_item['price']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?', (name, quantity, price, item_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Item updated successfully!'})

# DELETE an inventory item by ID
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Item deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)


# Base URL
BASE_URL = "http://127.0.0.1:5000/inventory"

# Test GET all items
response = request.get(BASE_URL)
print("GET all items:", response.json())

# Test POST (Add new item)
new_item = {
    "name": "Laptop",
    "quantity": 10,
    "price": 999.99
}
response = request.post(BASE_URL, json=new_item)
print("POST new item:", response.json())

# Test GET specific item by ID
response = request.get(f"{BASE_URL}/1")
print("GET item with ID 1:", response.json())

# Test PUT (Update an item)
update_item = {
    "name": "Laptop",
    "quantity": 5,
    "price": 899.99
}
response = request.put(f"{BASE_URL}/1", json=update_item)
print("PUT update item:", response.json())

# Test DELETE an item
response = request.delete(f"{BASE_URL}/1")
print("DELETE item with ID 1:", response.json())


