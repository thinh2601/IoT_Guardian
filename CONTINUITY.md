# CONTINUITY.md - IoT Guardian Project Ledger

## 1. Goal (Mục tiêu)
* **Sản phẩm:** IoT Guardian - Hệ thống giám sát an ninh mạng gia đình.
* **Mục tiêu cốt lõi:** Quét mạng LAN, phát hiện thiết bị lạ, cảnh báo lỗ hổng.

## 2. Constraints & Assumptions
* **OS Server:** Windows 11 (Confirmed).
* **Tech Stack:** Python 3.13 + Nmap 7.98 (Backend), Flutter (Mobile), ReactJS (Web), MongoDB.
* **Path:** `C:\BaoCaoTotNghiep\IoT_Guardian`

## 3. Key Decisions
* **Architecture:** Centralized Server (Laptop quét, Mobile xem).
* **DB Strategy:** NoSQL (MongoDB) để lưu dữ liệu thiết bị IoT đa dạng.

## 4. Master Plan & Status (Lộ trình 12 Tuần)

### 🟢 Giai đoạn 1: Khởi tạo & Thiết kế (Weeks 1-2) [DONE]
* **Week 1 (Planning):** [🟢 Done] Setup môi trường, chốt kế hoạch.
* **Week 2 (Design):** [🟢 Done] Thiết kế & Cài đặt Database MongoDB.

### 🟠 Giai đoạn 2: Xây dựng Core System (Weeks 3-4) [IN-PROGRESS]
* **Week 3 (Backend Core):** [🟢 Done] API & Basic Scan hoàn tất.
* **Week 4 (Security & CVE):** [🟡 In-Progress]
    * [ ] Nâng cấp Scanner: Quét cổng dịch vụ (Port Scan & Service Version).
    * [ ] Module CVE: Đối chiếu phiên bản dịch vụ với cơ sở dữ liệu lỗi.
    * [ ] API: Trả về mức độ rủi ro (Risk Level) cho từng thiết bị.

### 🔵 Giai đoạn 3: Phát triển Giao diện (Weeks 5-7) [PENDING]
* **Week 5 (Mobile UI):** [⚪ Pending] Cắt giao diện Flutter, Dashboard.
* **Week 6 (Mobile Logic):** [⚪ Pending] Kết nối API, Push Notification.
* **Week 7 (Web Dashboard):** [⚪ Pending] Dựng Web ReactJS, Chart.

### 🟣 Giai đoạn 4: Tích hợp & Kiểm thử (Weeks 8-10)
*Mục tiêu: Ghép các mảnh lại với nhau và bắt lỗi.*
* **Week 8 (Integration):** [⚪ Chờ] Đồng bộ dữ liệu Real-time giữa Web-App-Server, tính năng chặn (Block).
* **Week 9 (Testing Dev):** [⚪ Chờ] Unit Test cho Backend, kiểm tra API chịu tải.
* **Week 10 (Testing User):** [⚪ Chờ] Release bản Beta, nhờ bạn bè dùng thử (UAT) để tìm lỗi thực tế.

### 🏁 Giai đoạn 5: Hoàn thiện & Báo cáo (Weeks 11-12)
*Mục tiêu: Đóng gói sản phẩm đẹp đẽ để trình bày.*
* **Week 11 (Refine):** [⚪ Chờ] Tối ưu tốc độ quét, viết tài liệu hướng dẫn (Documentation).
* **Week 12 (Finish):** [⚪ Chờ] Deploy lên Cloud (Demo), làm Slide thuyết trình.


## 5. Current Sprint (Week 4 Detail)
* **Goal:** Biến hệ thống từ "Danh bạ thiết bị" thành "Chuyên gia bảo mật".
* **To-Do:**
    * [ ] Nâng cấp `scanner_core.py` để tìm Open Ports (Cổng mở).
    * [ ] Nâng cấp `scanner_service.py` để lưu danh sách cổng vào DB.
    * [ ] Test thực tế với Camera/Router trong nhà.

## 6. Next Decision (Quyết định tiếp theo)
* **Option A:** Làm tiếp Week 4 (Security & CVE Scan).
* **Option B:** Nhảy sang Week 5 (Mobile App UI) trước.