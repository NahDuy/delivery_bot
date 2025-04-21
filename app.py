from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

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

    if not dish or not table:
        return jsonify({"status": "error", "message": "Thiếu thông tin"}), 400

    # Đọc đường đi từ paths.json
    try:
        with open("paths.json", "r") as f:
            all_paths = json.load(f)["paths"]

        pathReceive = []
        pathBack = []
        for p in all_paths:
            if p["to"].lower() == table.lower():
                pathReceive = p["pathReceive"]
                pathBack = p["pathBack"]
                break

        if not pathReceive:
            return jsonify({"status": "error", "message": "Không tìm thấy đường đi cho bàn này"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": f"Lỗi đọc paths.json: {e}"}), 500

    order_entry = {
        "table": table,
        "dish": dish,
        "commands": pathReceive,
        "returnPath": pathBack
    }

    # Ghi đơn hàng vào file
    try:
        with open("orders.json", "r") as f:
            orders = json.load(f)
    except:
        orders = []

    orders.append(order_entry)

    with open("orders.json", "w") as f:
        json.dump(orders, f)

    return jsonify({"status": "ok"})

@app.route('/orders')
def get_orders():
    try:
        with open("orders.json", "r") as f:
            orders = json.load(f)
    except FileNotFoundError:
        orders = []
    return jsonify(orders)

@app.route('/return', methods=['POST'])
def return_robot():
    index = request.json.get("index")
    try:
        with open("orders.json", "r") as f:
            orders = json.load(f)
    except:
        return jsonify({"status": "error", "message": "Không đọc được file orders"}), 500

    if 0 <= index < len(orders):
        try:
            with open("static/return_command.json", "w") as f:
                json.dump(orders[index]["returnPath"], f)
            print(f"✅ Gửi returnPath cho đơn index {index}")
            return jsonify({"status": "ok"})
        except Exception as e:
            return jsonify({"status": "error", "message": f"Lỗi ghi return_command.json: {e}"}), 500
    else:
        return jsonify({"status": "error", "message": "Index không hợp lệ"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
