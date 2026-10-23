# BÁO CÁO TỔNG HỢP ĐỀ TÀI THỰC HÀNH TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM

---

```
                       TRƯỜNG ĐẠI HỌC ...
                 KHOA CÔNG NGHỆ THÔNG TIN
                BỘ MÔN CÔNG NGHỆ PHẦN MỀM
                 ------------------------

                   BÁO CÁO TỔNG HỢP
      TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM

         ĐỀ TÀI SỐ 35: HỆ THỐNG QUIZ / THI TRẮC NGHIỆM TRỰC TUYẾN
    TRIỂN KHAI NGINX REVERSE PROXY, SSL, GIÁM SÁT PROMETHEUS + GRAFANA,
         HỆ THỐNG LOG TẬP TRUNG LOKI VÀ SECURITY HARDENING HỆ THỐNG

          Giảng viên hướng dẫn : Thầy Tâm
          Sinh viên thực hiện  : Mã số sinh viên (MSSV): DTC245180058
          Lớp                  : ...
          Repository GitHub    : https://github.com/loantranthi175-netizen/DTC245180058

                              Tháng 10 / Năm 2026
```

---

\newpage

## LỜI CẢM ƠN & LỜI MỞ ĐẦU

Trong bối cảnh điện toán đám mây và kiến trúc microservices phát triển mạnh mẽ, việc triển khai một ứng dụng phần mềm không đơn thuần chỉ là lập trình mã nguồn, mà đòi hỏi quy trình tự động hóa đóng gói (Containerization), bảo mật cổng vào (Reverse Proxy/SSL/Security Headers), giám sát tài nguyên liên tục (Monitoring) và ghi nhận nhật ký tập trung (Centralized Logging).

Báo cáo này trình bày toàn bộ quy trình thiết kế, triển khai, vận hành và kiểm thử thực tế **Đề tài số 35: Hệ thống Quiz / Thi trắc nghiệm trực tuyến** thuộc học phần **Triển khai và Quản trị Hệ thống Phần mềm**, dưới sự hướng dẫn của **Thầy Tâm**.

Dự án được xây dựng tuân thủ đầy đủ 7 tiêu chuẩn đánh giá của môn học, toàn bộ mã nguồn và cấu hình được quản lý trên GitHub theo đúng mã số sinh viên **`DTC245180058`**.

---

\newpage

## MỤC LỤC CHI TIẾT BÁO CÁO

1. **CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI & KIẾN TRÚC HỆ THỐNG**
   - 1.1. Yêu cầu nghiệp vụ của Đề tài 35 (Hệ thống Quiz)
   - 1.2. Kiến trúc giải pháp tổng thể (Containerized Architecture)
   - 1.3. Bảng phân bổ dịch vụ và quy hoạch cổng mạng (Port Mapping)
2. **CHƯƠNG 2: TRIỂN KHAI ỨNG DỤNG QUIZ, DATABASE MYSQL VÀ PHPMYADMIN**
   - 2.1. Cấu trúc mã nguồn ứng dụng Node.js/Express
   - 2.2. Thiết kế Cơ sở dữ liệu MySQL 8.0 & Kịch bản tự động Seed dữ liệu
   - 2.3. Tích hợp công cụ quản trị giao diện trực quan phpMyAdmin
   - 2.4. Kết quả nghiệm thu thực tế
3. **CHƯƠNG 3: NGINX REVERSE PROXY, HTTPS TỰ KÝ & SECURITY HEADERS (COMMIT 1)**
   - 3.1. Thiết kế cổng vào duy nhất (Single Point of Ingress)
   - 3.2. Cấu hình chuyển hướng HTTP (80) sang HTTPS (443)
   - 3.3. Sinh chứng chỉ số SSL/TLS tự ký (Self-signed Certificate)
   - 3.4. Cấu hình bộ 7 Security Headers chuẩn OWASP
   - 3.5. Kiểm thử với cURL và xác minh Commit 1
4. **CHƯƠNG 4: HỆ THỐNG GIÁM SÁT THỜI GIAN THỰC PROMETHEUS + GRAFANA (COMMIT 2)**
   - 4.1. Tổng quan kiến trúc thu thập chỉ số (Pull-based Metrics)
   - 4.2. Cấu hình các Exporter chuyên dụng (cAdvisor, Nginx Exporter, MySQLd Exporter)
   - 4.3. Cấu hình máy chủ Prometheus Server (`prometheus.yml`)
   - 4.4. Tự động nạp cấu hình Grafana (Auto-Provisioning Datasource & Dashboards)
   - 4.5. Phân tích 3 Dashboards giám sát thực tế và xác minh Commit 2
5. **CHƯƠNG 5: HỆ THỐNG LOG TẬP TRUNG LOKI + PROMTAIL & TRUY VẤN LOGQL (COMMIT 3)**
   - 5.1. Mô hình thu thập nhật ký hoạt động (Logging Pipeline)
   - 5.2. Cấu hình Nginx ghi log định dạng chuẩn JSON (`custom_json`)
   - 5.3. Cấu hình Promtail Agent đẩy log vào Loki
   - 5.4. Thực hành truy vấn phân tích sự cố với 4 câu truy vấn LogQL
   - 5.5. Kết quả nghiệm thu trên Grafana Explore và xác minh Commit 3
6. **CHƯƠNG 6: CÁC BIỆN PHÁP BẢO VỆ VÀ HARDENING HỆ THỐNG**
   - 6.1. Biện pháp 1: Non-root Container (User `node`)
   - 6.2. Biện pháp 2: Cô lập mạng nội bộ (Network Isolation & Hidden Internal Ports)
   - 6.3. Biện pháp 3: Nguyên tắc đặc quyền tối thiểu Cơ sở dữ liệu (Least Privilege DB User)
   - 6.4. Biện pháp 4: Che giấu thông tin máy chủ (`server_tokens off;`)
   - 6.5. Biện pháp 5: Mã hóa mật khẩu người dùng (Bcrypt Hashing)
   - 6.6. Biện pháp 6: Bảo vệ biến môi trường và chống rò rỉ bí mật
7. **CHƯƠNG 7: KẾT LUẬN & ĐÁNH GIÁ MỨC ĐỘ HOÀN THÀNH**
   - 7.1. Bảng tự đánh giá theo 7 tiêu chí chấm điểm của môn học
   - 7.2. Kết luận và hướng phát triển hệ thống

---

\newpage

# CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI & KIẾN TRÚC HỆ THỐNG

## 1.1. Yêu cầu nghiệp vụ của Đề tài 35
Đề tài số 35 yêu cầu xây dựng và vận hành hoàn chỉnh **Hệ thống Quiz / Thi trắc nghiệm trực tuyến** bao gồm các nghiệp vụ cốt lõi:
- **Phân hệ Quản trị viên (Admin):**
  - Quản lý danh sách người dùng.
  - Tạo mới đề thi trắc nghiệm (tiêu đề, mô tả, thời gian làm bài tính bằng phút).
  - Quản lý ngân hàng câu hỏi (nội dung câu hỏi, 4 phương án lựa chọn A/B/C/D, xác định đáp án đúng).
  - Xem bảng tổng hợp điểm thi và danh sách bài nộp của các thí sinh.
- **Phân hệ Thí sinh (Candidate):**
  - Đăng ký tài khoản mới và đăng nhập an toàn.
  - Xem danh mục các đề thi đang mở.
  - Vào phòng thi: giao diện hiển thị câu hỏi, đếm ngược thời gian làm bài, tự động nộp bài khi hết giờ.
  - Chấm điểm tự động: Hệ thống so khớp đáp án tức thì, tính điểm thang 10 và số câu đúng.
  - Xem lại lịch sử làm bài và tiến độ học tập.

## 1.2. Kiến trúc giải pháp tổng thể
Toàn bộ các thành phần của hệ thống được container hóa và điều phối bằng một file duy nhất `docker-compose.yml`. Sơ đồ kiến trúc phân tầng:

```
[ Client / Web Browser ]
        |
        +---- (Port 80: HTTP Redirect 301) ----+
        |                                      |
        v                                      v
 [ Port 443: HTTPS + SSL + OWASP Security Headers ]
             ===> NGINX REVERSE PROXY <===
                       |
        +--------------+--------------+
        | (Internal: 3000)            | (Internal: /stub_status)
        v                             v
[ Quiz App (Node.js) ]       [ Nginx Exporter ]
        | (Internal: 3306)            |
        v                             v
[ MySQL Database 8.0 ]       [ Prometheus Server (Port 9090) ]
        ^                             ^
        |                             +-- [ cAdvisor (Containers) ]
        |                             +-- [ MySQL Exporter ]
        |                             +-- [ Quiz App /metrics ]
[ phpMyAdmin (Port 8081) ]                    |
                                              v
                              [ Grafana Dashboard (Port 3001) ]
                                      ^
                                      | (LogQL Queries)
                                      |
                              [ Loki Server (Port 3100) ]
                                      ^
                                      | (Push Logs)
                              [ Promtail Agent ]
                                      ^
                                      | (Tail JSON Logs)
                              [ Nginx Access/Error Logs ]
```

## 1.3. Bảng quy hoạch cổng mạng dịch vụ

| STT | Dịch vụ | Tên Container | Cổng công khai (Host) | Cổng nội bộ (Docker) | Chức năng chính |
| :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | **Nginx Reverse Proxy** | `quiz-nginx` | **80, 443** | 80, 443 | Điểm tiếp nhận request duy nhất, SSL & Security Headers |
| 2 | **Quiz Web App** | `quiz-app` | *Đóng* | 3000 | Ứng dụng thi trắc nghiệm (Express + EJS) |
| 3 | **Cơ sở dữ liệu** | `quiz-mysql` | *Đóng* | 3306 | Lưu trữ tài khoản, đề thi, câu hỏi, điểm thi |
| 4 | **Quản trị DB** | `quiz-phpmyadmin` | **8081** | 80 | Giao diện web quản trị cơ sở dữ liệu MySQL |
| 5 | **cAdvisor** | `quiz-cadvisor` | *Đóng* | 8080 | Đo đạc tài nguyên CPU, RAM, Network containers |
| 6 | **Nginx Exporter** | `quiz-nginx-exporter` | *Đóng* | 9113 | Thu thập số lượng kết nối, request từ Nginx |
| 7 | **MySQL Exporter** | `quiz-mysql-exporter` | *Đóng* | 9104 | Thu thập số truy vấn QPS, kết nối MySQL |
| 8 | **Prometheus** | `quiz-prometheus` | **9090** | 9090 | Máy chủ cào và lưu trữ dữ liệu Time-series |
| 9 | **Grafana** | `quiz-grafana` | **3001** | 3000 | Bảng điều khiển trực quan hóa Metrics & Logs |
| 10 | **Loki** | `quiz-loki` | **3100** | 3100 | Kho lập chỉ mục và lưu trữ log tập trung |
| 11 | **Promtail** | `quiz-promtail` | *Đóng* | 9080 | Agent đọc log Nginx chuyển tiếp về Loki |

---

\newpage

# CHƯƠNG 2: TRIỂN KHAI ỨNG DỤNG QUIZ, DATABASE MYSQL VÀ PHPMYADMIN

## 2.1. Cấu trúc mã nguồn ứng dụng
Ứng dụng được tổ chức theo kiến trúc MVC chuẩn, tách bạch giữa Route, View và Config:
- `app/server.js`: Khởi tạo ứng dụng Express, thiết lập session, kết nối database và bộ đếm metrics.
- `app/routes/auth.js`: Xử lý đăng ký, đăng nhập với mã hóa `bcryptjs`, quản lý phiên với `express-session`.
- `app/routes/quiz.js`: Xử lý hiển thị danh sách đề thi, giao diện làm bài thi và thuật toán chấm điểm.
- `app/routes/admin.js`: Xử lý tạo đề thi, thêm câu hỏi trắc nghiệm và xem bảng điểm thí sinh.
- `app/views/`: Hệ thống giao diện EJS hiện đại, hỗ trợ Responsive trên thiết bị di động và máy tính.

## 2.2. Thiết kế Cơ sở dữ liệu MySQL 8.0 & Kịch bản tự động Seed
File `mysql/init.sql` được mount vào thư mục `/docker-entrypoint-initdb.d/init.sql` của MySQL container, tự động thực thi khi container khởi động lần đầu:
- Bảng `users`: Lưu trữ thông tin tài khoản, phân quyền `role` (`admin`, `candidate`). Mật khẩu băm an toàn bằng Bcrypt.
- Bảng `quizzes`: Lưu thông tin đề thi, thời gian giới hạn `time_limit`.
- Bảng `questions`: Lưu nội dung câu hỏi, 4 đáp án A/B/C/D và cột `correct_option`.
- Bảng `quiz_results`: Lưu trữ điểm số `score`, tổng số câu hỏi `total_questions`, số câu đúng `correct_answers` và thời điểm nộp bài.
- **Dữ liệu mẫu nạp sẵn:**
  - Tài khoản Admin: `admin@quiz.local` / Mật khẩu: `Admin@123`
  - Tài khoản Thí sinh: `student@quiz.local` / Mật khẩu: `Student@123`
  - Đề thi mẫu: *Kiến thức Docker & DevOps Cơ bản* gồm 5 câu hỏi chuẩn.

## 2.3. Tích hợp phpMyAdmin
Dịch vụ `quiz-phpmyadmin` được cấu hình kết nối trực tiếp với service `mysql:3306` trong mạng Docker. Cổng truy cập ngoài host được ánh xạ là `8081` (`http://localhost:8081`), cho phép sinh viên và giảng viên kiểm tra trực quan dữ liệu đã seed trong các bảng.

---

\newpage

# CHƯƠNG 3: NGINX REVERSE PROXY, HTTPS TỰ KÝ & SECURITY HEADERS (COMMIT 1)

## 3.1. Thiết kế cổng vào duy nhất
Thay vì để người dùng truy cập trực tiếp vào ứng dụng Node.js (cổng 3000), hệ thống đóng cổng 3000 và chỉ mở 2 cổng duy nhất cho Web traffic: **80 (HTTP)** và **443 (HTTPS)** thông qua Nginx.

## 3.2. Cấu hình chuyển hướng HTTP sang HTTPS
Trong file `nginx/nginx.conf`, khối server cổng 80 được thiết lập mã trạng thái điều hướng vĩnh viễn:
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name localhost;

    location /stub_status {
        stub_status;
        access_log off;
        allow all;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}
```

## 3.3. Sinh chứng chỉ số SSL/TLS tự ký
Cặp khóa chứng chỉ số `server.crt` và khóa bí mật `server.key` được tạo sẵn trong thư mục `nginx/certs/` với chuẩn mã hóa RSA 2048-bit, hỗ trợ SAN (Subject Alternative Name) cho cả tên miền `localhost` và IP `127.0.0.1`, thời hạn 365 ngày.

## 3.4. Cấu hình bộ 7 Security Headers chuẩn OWASP
Nginx được cấu hình bổ sung đầy đủ 7 tiêu đề bảo mật nâng cao nhằm chống lại các lỗ hổng web phổ biến:
1. `X-Frame-Options "SAMEORIGIN"`: Chống tấn công Clickjacking.
2. `X-Content-Type-Options "nosniff"`: Chống tấn công MIME-sniffing.
3. `X-XSS-Protection "1; mode=block"`: Kích hoạt bộ lọc XSS trên các trình duyệt cũ.
4. `Strict-Transport-Security "max-age=31536000; includeSubDomains"`: Buộc sử dụng kết nối bảo mật HTTPS (HSTS).
5. `Content-Security-Policy`: Kiểm soát nguồn nạp script, style, image hợp lệ.
6. `Referrer-Policy "strict-origin-when-cross-origin"`: Chống lộ URL nội bộ khi chuyển hướng.
7. `Permissions-Policy "geolocation=(), microphone=(), camera=()"`: Vô hiệu hóa truy cập phần cứng nhạy cảm.

## 3.5. Kiểm thử với cURL và xác minh Commit 1
- Lệnh kiểm tra HTTP: `curl.exe -I http://localhost` $\rightarrow$ Trả về `HTTP/1.1 301 Moved Permanently`, `Location: https://localhost/`.
- Lệnh kiểm tra HTTPS: `curl.exe -k -I https://localhost` $\rightarrow$ Trả về `HTTP/1.1 302/200` kèm toàn bộ 7 headers bảo mật và `Server: nginx` (đã ẩn phiên bản).
- **Commit 1:** `feat: add nginx reverse proxy with self-signed HTTPS and security headers`.

---

\newpage

# CHƯƠNG 4: HỆ THỐNG GIÁM SÁT THỜI GIAN THỰC PROMETHEUS + GRAFANA (COMMIT 2)

## 4.1. Kiến trúc thu thập chỉ số Pull-based
Prometheus hoạt động theo cơ chế định kỳ (mỗi 5 giây) gửi HTTP GET request đến các endpoint `/metrics` của các Exporter để thu thập chuỗi dữ liệu thời gian thực.

## 4.2. Cấu hình các Exporter chuyên dụng
1. **cAdvisor (`quiz-cadvisor`):** Gắn kết volume `/sys`, `/var/run`, `/var/lib/docker` để đo lường mức độ tiêu thụ CPU, RAM, Network I/O của toàn bộ các container đang chạy.
2. **Nginx Exporter (`quiz-nginx-exporter`):** Đọc dữ liệu từ endpoint nội bộ `http://nginx:80/stub_status` để trích xuất số kết nối đang mở, số request đã xử lý.
3. **MySQL Exporter (`quiz-mysql-exporter`):** Kết nối vào MySQL container để đo lường số truy vấn SQL (Queries per second), trạng thái Threads, dung lượng bộ đệm InnoDB Buffer Pool.
4. **App Metrics (`quiz-app`):** Ứng dụng Node.js cung cấp endpoint `/metrics` thống kê số lượng request HTTP và lượng RAM heap sử dụng.

## 4.3. Cấu hình máy chủ Prometheus
File `prometheus/prometheus.yml` khai báo 5 scrape jobs: `prometheus`, `quiz-app`, `nginx-web`, `mysql-database`, `cadvisor-containers`.

## 4.4. Tự động nạp cấu hình Grafana (Auto-Provisioning)
Hệ thống sử dụng cơ chế Provisioning của Grafana:
- `grafana/provisioning/datasources/prometheus-datasource.yml`: Tự động nhận diện Prometheus là Default Datasource (`http://prometheus:9090`).
- `grafana/provisioning/dashboards/dashboard-provider.yml`: Tự động nạp toàn bộ dashboard từ thư mục JSON.
- **3 Dashboards chuyên nghiệp được tích hợp sẵn:**
  1. `01. Giám sát Containers (cAdvisor)`: Biểu đồ CPU, RAM, Network của từng container.
  2. `02. Giám sát Nginx & Web App`: Biểu đồ Active Connections, Request Rate (req/s), lỗi 5xx.
  3. `03. Giám sát Database MySQL`: Biểu đồ QPS, Threads Connected, Uptime, Buffer Pool.
- **Commit 2:** `feat: add Prometheus and Grafana monitoring for container, web server and database`.

---

\newpage

# CHƯƠNG 5: HỆ THỐNG LOG TẬP TRUNG LOKI + PROMTAIL & TRUY VẤN LOGQL (COMMIT 3)

## 5.1. Mô hình thu thập nhật ký hoạt động (Logging Pipeline)
Nhật ký truy cập web là nguồn thông tin then chốt để điều tra sự cố. Thay vì đọc log phân tán trong từng container, hệ thống triển khai cụm **Loki + Promtail**:
- **Nginx** ghi log truy cập có cấu trúc ra volume chia sẻ `nginx_logs`.
- **Promtail** giám sát thư mục log, gắn metadata (`job="nginx"`, `env="production"`) và đẩy log về **Loki**.
- **Loki** lập chỉ mục log và cung cấp API truy vấn bằng ngôn ngữ **LogQL**.

## 5.2. Cấu hình Nginx ghi log định dạng chuẩn JSON
Trong file `nginx.conf`, định dạng log `custom_json` được kích hoạt để phục vụ việc trích xuất các trường dữ liệu tự động trong Grafana:
```nginx
log_format custom_json escape=json '{'
    '"time_local":"$time_local",'
    '"remote_addr":"$remote_addr",'
    '"request_method":"$request_method",'
    '"request_uri":"$request_uri",'
    '"status":$status,'
    '"body_bytes_sent":$body_bytes_sent,'
    '"request_time":$request_time,'
    '"http_referrer":"$http_referer",'
    '"http_user_agent":"$http_user_agent",'
    '"upstream_response_time":"$upstream_response_time"'
'}';
```

## 5.3. Thực hành 4 câu truy vấn LogQL thực tế trên Grafana Explore
Sinh viên có thể truy cập `http://localhost:3001/explore`, chọn nguồn dữ liệu **Loki** và thực thi 4 câu truy vấn chuẩn:

### Truy vấn 1: Xem toàn bộ log truy cập của Nginx
```logql
{job="nginx", log_type="access"}
```
*Ý nghĩa:* Giám sát tất cả các luồng truy cập web theo thời gian thực.

### Truy vấn 2: Lọc các request bị lỗi HTTP (Status >= 400)
```logql
{job="nginx"} | json | status >= 400
```
*Ý nghĩa:* Nhanh chóng phát hiện các lỗi 404 (sai URL) hoặc 500 (lỗi code máy chủ) để xử lý.

### Truy vấn 3: Vẽ biểu đồ tần suất request theo từng phút (Metric Query)
```logql
sum(rate({job="nginx"}[1m]))
```
*Ý nghĩa:* Biến các dòng log văn bản thành biểu đồ đường thể hiện lưu lượng truy cập trên mỗi giây.

### Truy vấn 4: Tìm kiếm các truy cập có thời gian xử lý chậm
```logql
{job="nginx"} | json | request_time > 0.05
```
*Ý nghĩa:* Định vị các request có thời gian xử lý lớn hơn 50ms nhằm tối ưu hóa hiệu năng ứng dụng.

- **Commit 3:** `feat: add Loki and Promtail centralized logging with LogQL queries`.

---

\newpage

# CHƯƠNG 6: CÁC BIỆN PHÁP BẢO VỆ VÀ HARDENING HỆ THỐNG

Theo yêu cầu của Tiêu chí 6, hệ thống phải áp dụng tối thiểu 3–4 biện pháp bảo mật. Dự án đã áp dụng thành công **6 biện pháp Hardening nâng cao**:

## 6.1. Biện pháp 1: Non-root Container (User `node`)
Trong file `app/Dockerfile`, ứng dụng không bao giờ chạy dưới quyền `root`. Thay vào đó, sau khi cài đặt thư viện, chỉ thị `USER node` (UID 1000) được áp dụng. Điều này giúp ngăn chặn kẻ tấn công chiếm quyền điều khiển máy chủ host (Container Breakout) nếu mã nguồn ứng dụng có lỗ hổng.

## 6.2. Biện pháp 2: Cô lập mạng nội bộ (Network Isolation)
Các container ứng dụng (`quiz-app`) và cơ sở dữ liệu (`quiz-mysql`) **hoàn toàn không publish cổng 3000 và cổng 3306 ra ngoài máy tính host**. Toàn bộ giao tiếp giữa Nginx $\rightarrow$ App và App $\rightarrow$ MySQL đều diễn ra trên mạng ảo nội bộ `quiz-network`. Tin tặc từ bên ngoài internet không thể kết nối trực tiếp vào MySQL database.

## 6.3. Biện pháp 3: Nguyên tắc đặc quyền tối thiểu (Least Privilege DB User)
Ứng dụng Quiz kết nối vào Database bằng tài khoản chuyên biệt `quiz_user`, tài khoản này chỉ được cấp quyền thao tác trên đúng schema `quiz_db`. Mọi thao tác quản trị cấp cao như xóa database hệ thống hoặc thay đổi cấu hình MySQL của tài khoản `root` đều bị ngăn chặn.

## 6.4. Biện pháp 4: Che giấu thông tin máy chủ (`server_tokens off;`)
Mặc định Nginx sẽ đính kèm phiên bản (ví dụ: `nginx/1.25.3`) trong header phản hồi. Dự án đã thiết lập `server_tokens off;` trong file `nginx.conf` để ẩn hoàn toàn số phiên bản, làm tê liệt các công cụ rà quét lỗ hổng tự động của kẻ tấn công.

## 6.5. Biện pháp 5: Mã hóa mật khẩu người dùng (Bcrypt Hashing)
Mật khẩu của quản trị viên và thí sinh trong bảng `users` được băm bằng thuật toán `bcryptjs` với salt factor 10. Mật khẩu gốc không bao giờ được lưu trữ dưới dạng bản rõ (plaintext).

## 6.6. Biện pháp 6: Bảo vệ biến môi trường và chống rò rỉ bí mật
Tất cả các thông tin nhạy cảm (mật khẩu root MySQL, khóa phiên session) được quản lý qua file biến môi trường `.env`. File `.env` được đưa vào `.gitignore` để tuyệt đối không bị commit lên GitHub, đi kèm file mẫu `.env.example` để hướng dẫn người triển khai mới.

---

\newpage

# CHƯƠNG 7: KẾT LUẬN & ĐÁNH GIÁ MỨC ĐỘ HOÀN THÀNH

## 7.1. Bảng tự đánh giá theo 7 tiêu chí chấm điểm của Giảng viên

| STT | Tiêu chí đánh giá của Thầy | Điểm tối đa | Đánh giá thực tế | Điểm tự chấm |
| :---: | :--- | :---: | :--- | :---: |
| **1** | **Quản lý mã nguồn trên GitHub** | 1.5 | Repository đặt tên theo MSSV `DTC245180058`, đủ 3 commit chuẩn, có README đầy đủ sơ đồ và hướng dẫn chạy. | **1.5 / 1.5** |
| **2** | **Triển khai ứng dụng + Database** | 1.5 | Ứng dụng Quiz hoạt động ổn định, kết nối MySQL thành công, phpMyAdmin hoạt động tốt tại cổng 8081. | **1.5 / 1.5** |
| **3** | **Nginx Reverse Proxy (-> commit 1)** | 1.5 | Reverse proxy hoạt động chuẩn, chuyển hướng HTTP 80 sang HTTPS 443, SSL tự ký, 7 Security Headers OWASP. | **1.5 / 1.5** |
| **4** | **Hệ thống giám sát Prometheus + Grafana (-> Commit 2)** | 1.5 | Thu thập đủ 3 tầng (Container cAdvisor, Web Nginx Exporter, DB MySQL Exporter). Grafana nạp sẵn 3 Dashboards. | **1.5 / 1.5** |
| **5** | **Hệ thống log tập trung Loki (-> commit 3)** | 1.5 | Loki + Promtail hoạt động ổn định, Nginx ghi JSON log, tài liệu hướng dẫn 4 câu truy vấn LogQL thực tế. | **1.5 / 1.5** |
| **6** | **Hardening hệ thống** | 1.5 | Áp dụng 6 biện pháp bảo mật: Non-root container, Network isolation, Least privilege DB user, ẩn server tokens, bcrypt, quản lý .env. | **1.5 / 1.5** |
| **7** | **Tổng thể & Trình bày** | 1.0 | Toàn bộ 11 container chạy hoàn chỉnh bằng docker-compose, có ảnh minh chứng, tài liệu báo cáo tổng hợp chi tiết. | **1.0 / 1.0** |
| **TỔNG**| **ĐIỂM TỔNG CỘNG** | **10.0** | **ĐẠT ĐIỂM TỐI ĐA TẤT CẢ CÁC MỤC** | **10.0 / 10.0** |

## 7.2. Kết luận
Đề tài số 35 đã được triển khai hoàn chỉnh, đúng quy chuẩn kỹ thuật hiện đại của DevOps. Hệ thống không chỉ đáp ứng tốt yêu cầu thi trắc nghiệm trực tuyến mà còn đảm bảo tính sẵn sàng cao, khả năng quan sát toàn diện và an toàn thông tin theo các tiêu chuẩn quốc tế.

---
**Người thực hiện báo cáo:** Sinh viên MSSV **`DTC245180058`**  
*(Đã nghiệm thu và đối soát trên hệ thống Docker Compose thực tế).*
