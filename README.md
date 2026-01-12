# IoT_Guardian

Dự án IoT_Guardian — hệ thống giám sát/kiểm thử thiết bị IoT.

Cấu trúc chính:
- `backend/` - mã nguồn backend (API, scanner)
- `mobile-app/` - ứng dụng di động
- `web-dashboard/` - giao diện quản trị web

Nền tảng và cài đặt nhanh (Windows):
1. Cài Python 3.10+ và Git.
2. Tạo môi trường ảo và cài phụ thuộc (nếu có `requirements.txt`):

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Chạy backend (ví dụ):

```powershell
python backend\api_server.py
```

Ghi chú:
- Thư mục `backend` chứa các tập tin: `api_server.py`, `scanner_core.py`, `scanner_service.py`.
- Nếu bạn muốn tôi thêm hướng dẫn chi tiết, file `requirements.txt`, hoặc cấu hình Docker, hãy cho biết.

Liên hệ: chủ repo trên GitHub: https://github.com/thinh2601/IoT_Guardian
