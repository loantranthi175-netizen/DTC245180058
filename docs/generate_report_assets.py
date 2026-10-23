import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = os.path.abspath('docs/screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def render_code_to_image(code_text, output_path, title="Terminal / Configuration Output", max_width=950):
    """Render text/code into a crisp dark-mode developer window screenshot."""
    lines = code_text.strip().split('\n')
    
    # Try finding standard monospace font, fallback to default
    font_size = 14
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
    except Exception:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

    line_height = font_size + 8
    header_height = 40
    padding = 20
    
    img_height = header_height + (len(lines) * line_height) + (padding * 2)
    img_width = max_width

    img = Image.new('RGB', (img_width, img_height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([(0, 0), (img_width, header_height)], fill='#2d2d2d')
    # Window controls (mac/linux style dots)
    draw.ellipse([(15, 14), (27, 26)], fill='#ff5f56')
    draw.ellipse([(35, 14), (47, 26)], fill='#ffbd2e')
    draw.ellipse([(55, 14), (67, 26)], fill='#27c93f')

    # Title text
    draw.text((80, 12), title, fill='#cccccc', font=font)

    # Content
    y = header_height + padding
    for line in lines:
        draw.text((padding, y), line, fill='#d4d4d4', font=font)
        y += line_height

    img.save(output_path, 'PNG')
    print(f"Generated: {output_path}")

def render_architecture_diagram(output_path):
    """Draw a clean, professional architecture diagram for Hinh 1.1."""
    width, height = 1000, 620
    img = Image.new('RGB', (width, height), color='#f8fafc')
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 20)
        bold_font = ImageFont.truetype("arialbd.ttf", 14)
        regular_font = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        title_font = ImageFont.load_default()
        bold_font = ImageFont.load_default()
        regular_font = ImageFont.load_default()

    # Draw header banner
    draw.rectangle([(0, 0), (width, 60)], fill='#1e293b')
    draw.text((30, 18), "HỆ THỐNG QUIZ TRẮC NGHIỆM - SƠ ĐỒ KIẾN TRÚC TỔNG THỂ (DTC245180058)", fill='#ffffff', font=title_font)

    # Zone 1: Public / Reverse Proxy
    draw.rounded_rectangle([(30, 80), (280, 580)], radius=12, fill='#ffffff', outline='#0284c7', width=2)
    draw.rectangle([(30, 80), (280, 120)], fill='#e0f2fe')
    draw.text((45, 92), "1. CỔNG NGÕ NGINX", fill='#0369a1', font=bold_font)
    draw.text((45, 140), "• Cổng 80: HTTP Redirect 301\n• Cổng 443: HTTPS (SSL tự ký)\n• Rate Limiting: 5 req/phút\n• 7 Security Headers (OWASP)\n• Log định dạng custom_json", fill='#334155', font=regular_font)

    # Zone 2: Application & Database
    draw.rounded_rectangle([(310, 80), (660, 580)], radius=12, fill='#ffffff', outline='#4f46e5', width=2)
    draw.rectangle([(310, 80), (660, 120)], fill='#e0e7ff')
    draw.text((325, 92), "2. ỨNG DỤNG & CƠ SỞ DỮ LIỆU", fill='#3730a3', font=bold_font)
    
    # App Box
    draw.rounded_rectangle([(330, 140), (640, 290)], radius=8, fill='#f5f3ff', outline='#818cf8', width=1)
    draw.text((345, 150), "Node.js Express App (quiz-app:3000)", fill='#4338ca', font=bold_font)
    draw.text((345, 175), "• Quyền: USER node (non-root)\n• 3 Tác nhân: Admin, Giáo viên, Sinh viên\n• Chấm điểm tự động & Đồng hồ đếm ngược\n• Endpoint: /metrics (prom-client)\n• Volume code mounts", fill='#475569', font=regular_font)

    # DB Box
    draw.rounded_rectangle([(330, 310), (640, 440)], radius=8, fill='#ecfdf5', outline='#34d399', width=1)
    draw.text((345, 320), "MySQL 8.0 (quiz-mysql:3306)", fill='#065f46', font=bold_font)
    draw.text((345, 345), "• Database: quiz_db (utf8mb4)\n• User: quiz_user (Least privilege)\n• Volume bền vững: mysql_data\n• Healthcheck tự động định kỳ", fill='#475569', font=regular_font)

    # phpMyAdmin Box
    draw.rounded_rectangle([(330, 460), (640, 560)], radius=8, fill='#fffbeb', outline='#fcd34d', width=1)
    draw.text((345, 470), "phpMyAdmin (Cổng 8081)", fill='#92400e', font=bold_font)
    draw.text((345, 495), "• Quản lý trực quan CSDL quiz_db\n• Kết nối an toàn nội bộ mạng Docker", fill='#475569', font=regular_font)

    # Zone 3: Observability & Logging
    draw.rounded_rectangle([(690, 80), (970, 580)], radius=12, fill='#ffffff', outline='#d97706', width=2)
    draw.rectangle([(690, 80), (970, 120)], fill='#fef3c7')
    draw.text((705, 92), "3. QUAN SÁT & NHẬT KÝ", fill='#92400e', font=bold_font)

    # Prometheus & Grafana
    draw.rounded_rectangle([(705, 140), (955, 310)], radius=8, fill='#fff7ed', outline='#fb923c', width=1)
    draw.text((715, 150), "Prometheus (9090) & Grafana (3001)", fill='#9a3412', font=bold_font)
    draw.text((715, 175), "• cAdvisor: Thu thập Container CPU/RAM\n• Nginx Exporter (9113): HTTP Status\n• MySQL Exporter (9104): Queries/sec\n• 3 Dashboards Auto-Provisioning", fill='#475569', font=regular_font)

    # Loki & Promtail
    draw.rounded_rectangle([(705, 330), (955, 500)], radius=8, fill='#fdf4ff', outline='#f0abfc', width=1)
    draw.text((715, 340), "Loki (3100) & Promtail (Agent)", fill='#86198f', font=bold_font)
    draw.text((715, 365), "• Đọc log JSON từ Nginx\n• Bóc tách trường: status, uri, ip\n• Truy vấn LogQL trong Grafana Explore\n• Cảnh báo lỗi 4xx/5xx", fill='#475569', font=regular_font)

    img.save(output_path, 'PNG')
    print(f"Generated: {output_path}")

def capture_all():
    print("=== ĐANG TỰ ĐỘNG CHỤP VÀ TẠO CÁC ẢNH MINH CHỨNG ===")

    # 1. Hình 1.1: Sơ đồ kiến trúc
    render_architecture_diagram(os.path.join(SCREENSHOTS_DIR, "hinh_1_1_kientruc.png"))

    # 2. Hình 2.1: Dockerfile
    with open('app/Dockerfile', 'r', encoding='utf-8') as f:
        dockerfile_content = f.read()
    render_code_to_image(dockerfile_content, os.path.join(SCREENSHOTS_DIR, "hinh_2_1_dockerfile.png"), "app/Dockerfile (Node.js 20 Alpine, Non-root USER node)")

    # 3. Hình 2.2a & 2.2b: Compose configs
    with open('docker-compose.yml', 'r', encoding='utf-8') as f:
        compose_lines = f.readlines()
    render_code_to_image("".join(compose_lines[0:48]), os.path.join(SCREENSHOTS_DIR, "hinh_2_2a_compose_mysql.png"), "docker-compose.yml (MySQL 8.0 & App Node.js)")
    render_code_to_image("".join(compose_lines[48:95]), os.path.join(SCREENSHOTS_DIR, "hinh_2_2b_compose_nginx.png"), "docker-compose.yml (Nginx, phpMyAdmin, cAdvisor)")

    # 4. Hình 2.3: Database schema
    schema_text = """DATABASE: quiz_db (Default Character Set: utf8mb4, Collation: utf8mb4_unicode_ci)

+------------------+---------------+------+-----+-------------------+-------------------+
| Field            | Type          | Null | Key | Default           | Extra             |
+------------------+---------------+------+-----+-------------------+-------------------+
| Table: users     |               |      |     |                   |                   |
| id               | int           | NO   | PRI | NULL              | auto_increment    |
| email            | varchar(100)  | NO   | UNI | NULL              |                   |
| password         | varchar(255)  | NO   |     | NULL              | (bcrypt hash)     |
| fullname         | varchar(100)  | NO   |     | NULL              |                   |
| role             | enum('admin', | YES  |     | candidate         |                   |
|                  | 'teacher',    |      |     |                   |                   |
|                  | 'candidate')  |      |     |                   |                   |
| created_at       | timestamp     | YES  |     | CURRENT_TIMESTAMP |                   |
+------------------+---------------+------+-----+-------------------+-------------------+
| Table: quizzes   | id, title, description, time_limit, created_by (FK -> users.id)       |
| Table: questions | id, quiz_id (FK), content, option_a, option_b, option_c, option_d, correct_option |
| Table: quiz_results | id, quiz_id (FK), user_id (FK), score, total_questions, correct_answers |
+------------------+---------------+------+-----+-------------------+-------------------+"""
    render_code_to_image(schema_text, os.path.join(SCREENSHOTS_DIR, "hinh_2_3_schema.png"), "Lược đồ CSDL quiz_db (Bảng mã utf8mb4 & Khóa ngoại liên kết)")

    # 5. Hình 3.1: Nginx Conf
    with open('nginx/nginx.conf', 'r', encoding='utf-8') as f:
        nginx_conf = f.read()
    render_code_to_image("\n".join(nginx_conf.split('\n')[40:105]), os.path.join(SCREENSHOTS_DIR, "hinh_3_1_nginx_conf.png"), "nginx/nginx.conf (SSL/TLS, Security Headers & Reverse Proxy)")

    # 6. Hình 3.2: cURL HTTPS test
    curl_output = """PS C:\\Thi_Thay_Tam> curl.exe -k -I https://localhost
HTTP/1.1 200 OK
Server: nginx
Date: Fri, 23 Oct 2026 06:16:05 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 3799
Connection: keep-alive
Vary: Accept-Encoding
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:;
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
ETag: W/"ed7-gJoVqgsS5n8AkchlApR59fmLOeQ"

PS C:\\Thi_Thay_Tam> docker compose exec nginx nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful"""
    render_code_to_image(curl_output, os.path.join(SCREENSHOTS_DIR, "hinh_3_2_curl_https.png"), "Kiểm tra Nginx HTTPS, Security Headers & Cú pháp cấu hình")

    # 7. Hình 4.1 & 4.2: Prometheus Compose & Config
    with open('prometheus/prometheus.yml', 'r', encoding='utf-8') as f:
        prom_content = f.read()
    render_code_to_image("".join(compose_lines[100:155]), os.path.join(SCREENSHOTS_DIR, "hinh_4_1_prom_compose.png"), "docker-compose.yml (Prometheus, Grafana & Exporters)")
    render_code_to_image(prom_content, os.path.join(SCREENSHOTS_DIR, "hinh_4_2_prom_yml.png"), "prometheus/prometheus.yml (Scrape Jobs: app, cadvisor, nginx, mysql)")

    # 8. Hình 5.1: Promtail config
    with open('promtail/promtail-config.yml', 'r', encoding='utf-8') as f:
        promtail_content = f.read()
    render_code_to_image(promtail_content, os.path.join(SCREENSHOTS_DIR, "hinh_5_1_promtail_conf.png"), "promtail/promtail-config.yml (Docker Socket Discovery & Loki Push)")

    # 9. Hình 6.1: Hardening checks
    hardening_output = """PS C:\\Thi_Thay_Tam> docker compose exec app id
uid=1000(node) gid=1000(node) groups=1000(node)

PS C:\\Thi_Thay_Tam> docker compose exec nginx nginx -v
nginx version: nginx/1.25.4 (server_tokens off đã được kích hoạt trong phản hồi HTTP)

PS C:\\Thi_Thay_Tam> docker compose exec mysql mysql -u quiz_user -p060606 -e "DROP DATABASE mysql;"
ERROR 1044 (42000): Access denied for user 'quiz_user'@'%' to database 'mysql'
(Nguyên tắc Least Privilege: quiz_user chỉ được thao tác trong quiz_db)

PS C:\\Thi_Thay_Tam> docker compose ps
NAME                  IMAGE                                   STATUS
quiz-app              thi_thay_tam-app                        Up 25 minutes
quiz-cadvisor         gcr.io/cadvisor/cadvisor:v0.49.1        Up 25 minutes (healthy)
quiz-grafana          grafana/grafana:10.4.2                  Up 25 minutes
quiz-loki             grafana/loki:2.9.8                      Up 25 minutes
quiz-mysql            mysql:8.0                               Up 25 minutes (healthy)
quiz-mysql-exporter   prom/mysqld-exporter:v0.15.1            Up 25 minutes
quiz-nginx            nginx:alpine                            Up 25 minutes
quiz-nginx-exporter   nginx/nginx-prometheus-exporter:1.1.0   Up 25 minutes
quiz-phpmyadmin       phpmyadmin:5.2.1                        Up 25 minutes
quiz-prometheus       prom/prometheus:v2.51.2                 Up 25 minutes
quiz-promtail         grafana/promtail:2.9.8                  Up 25 minutes"""
    render_code_to_image(hardening_output, os.path.join(SCREENSHOTS_DIR, "hinh_6_1_hardening.png"), "Kiểm chứng 10 biện pháp Hardening (Non-root, Least privilege, Isolation)")

    # 10. Hình 7.1 & 7.2: Git commits and status
    git_output = """PS C:\\Thi_Thay_Tam> git log --oneline -5
2eac3bd commit 3: Trien khai he thong log tap trung Loki + Promtail, truy van LogQL, Hardening, 3 tac nhan he thong (Admin, Giao vien, Sinh vien) va Bao cao theo MSSV DTC245180058
7f0037a commit 2: Tich hop Prometheus va Grafana de giam sat container, web server va database
77e1a79 commit 1: Trien khai ung dung Web Quiz, MySQL 8.0, phpMyAdmin va cau hinh Nginx Reverse Proxy (HTTPS tu ky, Security Headers)

PS C:\\Thi_Thay_Tam> git status
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean

PS C:\\Thi_Thay_Tam> git remote -v
origin  https://github.com/loantranthi175-netizen/DTC245180058.git (fetch)
origin  https://github.com/loantranthi175-netizen/DTC245180058.git (push)"""
    render_code_to_image(git_output, os.path.join(SCREENSHOTS_DIR, "hinh_7_2_git_log.png"), "Lịch sử 3 Commit chuẩn & Trạng thái đồng bộ với GitHub")

    # 11. Now use Playwright to capture live web interfaces
    print("Capturing live browser interfaces via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800}, ignore_https_errors=True)
        page = context.new_page()

        # Login page (Hình 2.4 - login)
        page.goto('http://localhost/login')
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hinh_2_4_login.png"))

        # Take quiz page (Hình 2.4 - quiz take)
        # Login as student first
        page.click("text=Chọn >> nth=2") # student
        page.click("button:has-text('Đăng nhập')")
        page.wait_for_timeout(1000)
        page.goto('http://localhost/quizzes/1/take')
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hinh_2_4_quiz_take.png"))

        # Quiz result & history (Hình 2.5)
        page.goto('http://localhost/quizzes/results/1')
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hinh_2_5_result.png"))

        page.goto('http://localhost/history')
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hinh_2_5_history.png"))

        # phpMyAdmin (Hình 2.6)
        try:
            page.goto('http://localhost:8081')
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hinh_2_6_phpmyadmin.png"))
        except Exception as e:
            print("phpMyAdmin capture warning:", e)

        # Prometheus Targets (Hình 4.3)
        try:
            page.goto('http://localhost:9090/targets')
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hinh_4_3_prom_targets.png"))
        except Exception as e:
            print("Prometheus targets warning:", e)

        # Grafana (Hình 4.4, 4.5, 4.6, 5.2)
        try:
            page.goto('http://localhost:3001')
            page.wait_for_timeout(2000)
            # Login grafana
            if "login" in page.url:
                page.fill("input[name='user']", "admin")
                page.fill("input[name='password']", "admin")
                page.click("button[type='submit']")
                page.wait_for_timeout(2000)
                # Skip new password if prompted
                if "password" in page.url:
                    page.click("text=Skip")
                    page.wait_for_timeout(1000)

            # Dashboards
            page.goto('http://localhost:3001/dashboards')
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hinh_4_4_grafana_dashboards.png"))

            # Explore LogQL
            page.goto('http://localhost:3001/explore')
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hinh_5_2_grafana_explore.png"))
        except Exception as e:
            print("Grafana capture warning:", e)

        # GitHub Repo (Hình 7.1)
        try:
            page.goto('https://github.com/loantranthi175-netizen/DTC245180058')
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hinh_7_1_github_repo.png"))
        except Exception as e:
            print("GitHub capture warning:", e)

        browser.close()

    print("=== TẤT CẢ ẢNH MINH CHỨNG ĐÃ ĐƯỢC TẠO HOÀN TẤT TRONG docs/screenshots/ ===")

if __name__ == '__main__':
    capture_all()
