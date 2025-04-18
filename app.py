from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Các điểm cố định
delivery_points = {
    "ban_1": {"x": 2, "y": 1},
    "ban_2": {"x": 4, "y": 3},
    "ban_3": {"x": 1, "y": 4}
}

@app.route('/')
def home():
    return open('templates/index.html', encoding='utf-8').read()

@app.route('/kitchen')
def kitchen():
    return open('templates/kitchen.html', encoding='utf-8').read()


@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    table = data.get("table")
    dish = data.get("dish")

    # Kiểm tra dữ liệu
    if table not in delivery_points:
        return jsonify({"status": "error", "message": "Bàn không hợp lệ!"}), 400
    if not dish:
        return jsonify({"status": "error", "message": "Chưa chọn món!"}), 400

    destination = delivery_points[table]
    route = [{"x": 0, "y": 0}, destination]  # Xe bắt đầu từ (0, 0)

    # Tạo đơn hàng
    order_entry = {
        "table": table,
        "dish": dish,
        "route": route
    }

    # Ghi vào file orders.json
    if os.path.exists("orders.json"):
        with open("orders.json", "r") as f:
            orders = json.load(f)
    else:
        orders = []

    orders.append(order_entry)

    with open("orders.json", "w") as f:
        json.dump(orders, f)

    return jsonify({"status": "ok", "route": route})

@app.route('/orders')
def get_orders():
    try:
        with open("orders.json", "r") as f:
            orders = json.load(f)
    except FileNotFoundError:
        orders = []
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
