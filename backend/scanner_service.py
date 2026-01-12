import pymongo
from datetime import datetime
from scanner_core import scan_network  # Import hàm quét từ file cũ

# Cấu hình kết nối DB
DB_CONNECTION_STRING = "mongodb://localhost:27017/"
DB_NAME = "iot_guardian_db"

def save_scan_results():
    # 1. Thực hiện quét mạng
    print("🚀 Bắt đầu quy trình quét và lưu dữ liệu...")
    devices = scan_network() # Gọi hàm từ scanner_core.py
    
    if not devices:
        print("⚠️ Không tìm thấy thiết bị nào hoặc có lỗi quét.")
        return

    # 2. Kết nối DB
    client = pymongo.MongoClient(DB_CONNECTION_STRING)
    db = client[DB_NAME]
    devices_col = db["devices"]
    history_col = db["scan_history"]

    # 3. Xử lý từng thiết bị
    new_devices_count = 0
    updated_devices_count = 0

    print(f"\n💾 Đang lưu {len(devices)} thiết bị vào MongoDB...")
    
    for device in devices:
        mac = device['mac']
        
        # Kiểm tra xem thiết bị đã có trong DB chưa
        existing_device = devices_col.find_one({"mac_address": mac})
        
        if existing_device:
            # Nếu đã có -> Cập nhật trạng thái và thời gian last_seen
            devices_col.update_one(
                {"mac_address": mac},
                {"$set": {
                    "ip_address": device['ip'], # IP có thể đổi (DHCP)
                    "status": "online",
                    "last_seen": datetime.now()
                }}
            )
            updated_devices_count += 1
        else:
            # Nếu chưa có -> Thêm mới
            new_device_doc = {
                "mac_address": mac,
                "ip_address": device['ip'],
                "hostname": device['hostname'],
                "vendor": device['vendor'],
                "type": "camera" if "Uniview" in device['vendor'] or "Kbvision" in device['vendor'] else "unknown", # Tự động nhận diện Camera
                "status": "online",
                "first_seen": datetime.now(),
                "last_seen": datetime.now(),
                "is_blocked": False
            }
            devices_col.insert_one(new_device_doc)
            new_devices_count += 1
            print(f"   [+] Thiết bị mới: {device['ip']} ({device['vendor']})")

    # 4. Đánh dấu các thiết bị KHÔNG tìm thấy trong lần quét này là 'offline'
    # Lấy danh sách tất cả MAC vừa quét được
    scanned_macs = [d['mac'] for d in devices]
    
    # Cập nhật status = offline cho các thiết bị có trong DB nhưng không có trong danh sách vừa quét
    result = devices_col.update_many(
        {"mac_address": {"$nin": scanned_macs}}, # $nin = Not In
        {"$set": {"status": "offline"}}
    )
    offline_count = result.modified_count

    # 5. Lưu lịch sử quét
    scan_log = {
        "scan_time": datetime.now(),
        "total_devices": len(devices),
        "new_devices_found": new_devices_count,
        "vulnerabilities_found": 0 # Tạm thời để 0, tuần sau làm module quét lỗi
    }
    history_col.insert_one(scan_log)

    print("\n✅ HOÀN TẤT ĐỒNG BỘ DỮ LIỆU!")
    print(f"   - Thêm mới: {new_devices_count}")
    print(f"   - Cập nhật: {updated_devices_count}")
    print(f"   - Đã chuyển Offline: {offline_count}")
    print("------------------------------------------------")

if __name__ == "__main__":
    save_scan_results()