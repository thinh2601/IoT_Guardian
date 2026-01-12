import nmap
import socket

def get_local_ip_range():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        ip_parts = ip.split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        return network_range, ip
    except Exception as e:
        print(f"Lỗi lấy IP: {e}")
        return "192.168.1.0/24", "127.0.0.1"

def scan_network():
    target, my_ip = get_local_ip_range()
    print(f"📡 Đang quét SÂU mạng (Deep Scan): {target}")
    print("⏳ Quét cổng & Dịch vụ (sẽ tốn 1-2 phút, vui lòng kiên nhẫn)...")

    nmap_path = [r"C:\Program Files (x86)\Nmap\nmap.exe", r"C:\Program Files\Nmap\nmap.exe"]
    try:
        nm = nmap.PortScanner(nmap_search_path=nmap_path)
    except nmap.PortScannerError:
        print("❌ CRITICAL ERROR: Không tìm thấy file nmap.exe!")
        return []
    
    # THAY ĐỔI LỚN Ở ĐÂY:
    # -sV: Service Version (Tìm phiên bản phần mềm)
    # --top-ports 50: Chỉ quét 50 cổng phổ biến nhất để nhanh (Web, FTP, SSH...)
    # -T4: Tốc độ quét nhanh
    nm.scan(hosts=target, arguments='-sV --top-ports 50 -T4')
    
    devices = []
    
    for host in nm.all_hosts():
        # Lấy thông tin cơ bản
        if 'mac' in nm[host]['addresses']:
            mac_address = nm[host]['addresses']['mac']
            vendor = nm[host]['vendor'].get(mac_address, "Unknown")
        else:
            mac_address = "SELF_DEVICE" 
            vendor = "This Computer"

        # Lấy danh sách cổng mở (Open Ports)
        open_ports = []
        if 'tcp' in nm[host]:
            for port in nm[host]['tcp']:
                if nm[host]['tcp'][port]['state'] == 'open':
                    service_name = nm[host]['tcp'][port]['name']
                    product_version = nm[host]['tcp'][port]['product'] + " " + nm[host]['tcp'][port]['version']
                    open_ports.append({
                        "port": port,
                        "service": service_name,
                        "version": product_version.strip()
                    })

        # Logic đánh giá rủi ro sơ bộ
        risk_level = "low"
        if len(open_ports) > 0:
            risk_level = "medium"
        # Nếu mở cổng 23 (Telnet) hoặc 21 (FTP) -> Rủi ro cao
        for p in open_ports:
            if p['port'] in [21, 23, 445]:
                risk_level = "high"

        device_info = {
            "ip": host,
            "mac": mac_address,
            "hostname": nm[host].hostname(),
            "vendor": vendor,
            "status": nm[host].state(),
            "open_ports": open_ports, # Thêm trường mới
            "risk_level": risk_level  # Thêm trường mới
        }
        devices.append(device_info)
        
        # In ra màn hình cho đẹp
        print(f"✅ {device_info['ip']} | {vendor}")
        if open_ports:
            print(f"   ⚠️  Cổng mở: {open_ports}")
        else:
            print("   🔒 Không có cổng mở (An toàn)")

    print(f"\n📊 Tổng cộng: {len(devices)} thiết bị.")
    return devices

if __name__ == "__main__":
    scan_network()