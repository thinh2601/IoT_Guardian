from fastapi import FastAPI
import pymongo
from bson import json_util
import json
import threading
from scanner_service import save_scan_results # Import hàm quét mạng đã viết

app = FastAPI(title="IoT Guardian API", version="1.0")

# Kết nối Database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["iot_guardian_db"]

# Hàm bổ trợ: Chuyển dữ liệu MongoDB (ObjectId, DateTime) sang JSON chuẩn
def parse_json(data):
    return json.loads(json_util.dumps(data))

# 1. API Chào mừng
@app.get("/")
def read_root():
    return {"message": "Welcome to IoT Guardian API Server"}

# 2. API Lấy danh sách thiết bị (Cho App/Web hiển thị)
@app.get("/devices")
def get_all_devices():
    # Lấy tất cả thiết bị, sắp xếp theo trạng thái (Online lên trước)
    devices = list(db["devices"].find().sort("status", -1))
    return {
        "count": len(devices),
        "data": parse_json(devices)
    }

# 3. API Kích hoạt quét mạng (Trigger Scan)
# Dùng threading để việc quét diễn ra ngầm, không làm treo API
@app.post("/scan")
def trigger_scan():
    try:
        # Chạy hàm quét trong một luồng riêng (Background Thread)
        scan_thread = threading.Thread(target=save_scan_results)
        scan_thread.start()
        return {"status": "success", "message": "Đang tiến hành quét mạng ngầm..."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 4. API Lấy lịch sử quét
@app.get("/history")
def get_scan_history():
    history = list(db["scan_history"].find().sort("scan_time", -1).limit(10))
    return parse_json(history)