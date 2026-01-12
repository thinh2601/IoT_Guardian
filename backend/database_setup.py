import pymongo
from datetime import datetime

# 1. Cấu hình kết nối
DB_CONNECTION_STRING = "mongodb://localhost:27017/"
DB_NAME = "iot_guardian_db"

def init_database():
    try:
        # Tạo kết nối đến MongoDB
        client = pymongo.MongoClient(DB_CONNECTION_STRING)
        
        # Kiểm tra kết nối
        client.admin.command('ping')
        print("✅ Kết nối MongoDB thành công!")
        
        # 2. Tạo (hoặc chọn) Database
        db = client[DB_NAME]
        
        # 3. Tạo Collection 'devices' và ràng buộc dữ liệu
        # Tạo index cho 'mac_address' để đảm bảo nó là duy nhất (không có 2 thiết bị trùng MAC)
        devices_col = db["devices"]
        devices_col.create_index("mac_address", unique=True)
        print("✅ Đã tạo collection 'devices' và cài đặt ràng buộc (Unique MAC).")

        # 4. Tạo Collection 'scan_history'
        # [SỬA LỖI] Cú pháp đúng để tạo index giảm dần trong PyMongo
        history_col = db["scan_history"]
        history_col.create_index([("scan_time", pymongo.DESCENDING)]) 
        print("✅ Đã tạo collection 'scan_history'.")
        
        # 5. Thêm một dữ liệu mẫu (Dummy Data) để Database hiện lên trong Compass
        sample_device = {
            "mac_address": "AA:BB:CC:11:22:33",
            "ip_address": "192.168.1.10",
            "hostname": "Test-Device-01",
            "vendor": "Virtual Machine",
            "type": "laptop",
            "status": "online",
            "created_at": datetime.now()
        }
        
        # Dùng try-except để tránh lỗi nếu dữ liệu mẫu đã tồn tại (do lần chạy trước có thể đã tạo index xong nhưng chưa insert)
        try:
            devices_col.insert_one(sample_device)
            print("🎉 Đã thêm dữ liệu mẫu thành công!")
        except pymongo.errors.DuplicateKeyError:
            print("⚠️ Dữ liệu mẫu đã tồn tại, không cần thêm mới.")

        print(f"\n🚀 Database '{DB_NAME}' đã sẵn sàng sử dụng!")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    init_database()