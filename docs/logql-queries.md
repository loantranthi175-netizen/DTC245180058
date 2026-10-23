# HƯỚNG DẪN TRUY VẤN LOG BẰNG LOGQL TRÊN GRAFANA (LOKI)

Tài liệu này cung cấp các câu truy vấn **LogQL** thực tế để giám sát, phân tích và điều tra sự cố hệ thống Quiz System thông qua Grafana Explore.

---

## 1. Cách truy cập giao diện truy vấn LogQL

1. Truy cập Grafana: [**`http://localhost:3001`**](http://localhost:3001)
2. Đăng nhập: Tài khoản `admin` / Mật khẩu `admin`
3. Trên thanh menu bên trái, chọn biểu tượng **Explore** (hình la bàn) hoặc truy cập [**`http://localhost:3001/explore`**](http://localhost:3001/explore).
4. Tại góc trên bên trái ô chọn nguồn dữ liệu (Data source), chọn **Loki**.
5. Nhập các câu truy vấn LogQL dưới đây vào ô **Log browser** và bấm nút **Run query** (hoặc nhấn `Shift + Enter`).

---

## 2. Danh sách các truy vấn LogQL thực tế

### Truy vấn 1: Xem toàn bộ log truy cập (Access Log) của Web Server Nginx
> **Mục đích**: Theo dõi tất cả các luồng request thời gian thực gửi tới hệ thống.

```logql
{job="nginx", log_type="access"}
```

- **Giải thích cú pháp**:
  - `{job="nginx"}`: Lọc theo nhãn `job` được Promtail đánh dấu khi cào log Nginx.
  - `log_type="access"`: Lọc riêng tập tin access.log, loại bỏ các dòng cảnh báo hệ thống.

---

### Truy vấn 2: Lọc các request gặp lỗi HTTP (Mã trạng thái 4xx hoặc 5xx)
> **Mục đích**: Phát hiện sớm các truy cập bị lỗi (404 Not Found, 403 Forbidden hoặc 500 Internal Server Error) để kịp thời sửa chữa.

```logql
{job="nginx"} | json | status >= 400
```
*Hoặc truy vấn tìm kiếm chuỗi nhanh:*
```logql
{job="nginx"} |= " 404 "
```

- **Giải thích cú pháp**:
  - `| json`: Nginx ghi log dưới định dạng JSON (`custom_json`), bộ phân tích LogQL tự động trích xuất các trường dữ liệu như `status`, `request_method`, `request_uri`, `request_time`.
  - `| status >= 400`: Chỉ hiển thị các dòng log có mã phản hồi HTTP $\ge$ 400 (Client/Server Errors).

---

### Truy vấn 3: Đếm tần suất Request theo thời gian (Request Rate Metric Query)
> **Mục đích**: Chuyển đổi dữ liệu Log thành biểu đồ lưu lượng để xem tải truy cập theo từng phút.

```logql
sum(rate({job="nginx"}[1m]))
```

- **Giải thích cú pháp**:
  - `rate({job="nginx"}[1m])`: Tính toán số lượng dòng log xuất hiện trên mỗi giây trong cửa sổ trượt 1 phút.
  - `sum(...)`: Tổng hợp toàn bộ lượng truy cập thành một đường biểu đồ duy nhất trên Grafana.

---

### Truy vấn 4: Đo thời gian phản hồi trung bình (Upstream Response Time)
> **Mục đích**: Giám sát hiệu năng của ứng dụng Node.js (thời gian xử lý request tính bằng giây).

```logql
{job="nginx"} | json | request_time > 0.05
```

- **Giải thích cú pháp**:
  - Lọc các request có thời gian xử lý lớn hơn 50ms (0.05s) để tìm điểm nghẽn hiệu năng (bottleneck).
