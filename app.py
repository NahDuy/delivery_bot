from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Các điểm cố định
delivery_points = {
    "ban_1": {"x": 2, "y": 1},
    "ban_2": {"x": 4, "y": 3},
    "ban_3": {"x": 1, "y": 4}
}

@app.route('/')
def home():
    return open('templates/index.html').read()

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    table = data.get("table")
    dish = data.get("dish")

    # Kiểm tra bàn và món hợp lệ
    if table not in delivery_points:
        return jsonify({"status": "error", "message": "Bàn không hợp lệ!"}), 400
    if not dish:
        return jsonify({"status": "error", "message": "Chưa chọn món!"}), 400

    # Lấy tọa độ bàn
    destination = delivery_points[table]
    
    # Lưu route vào file JSON (hoặc xử lý logic khác ở đây)
    route = [{"x": 0, "y": 0}, destination]  # Giả sử xe xuất phát từ (0, 0)

    with open("route_data.json", "w") as f:
        json.dump(route, f)

    return jsonify({"status": "ok", "route": route})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
