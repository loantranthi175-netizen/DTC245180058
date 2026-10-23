import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DOCX_OUTPUT = os.path.abspath('docs/BAO_CAO_TONG_HOP_DTC245180058.docx')
SCREENSHOTS_DIR = os.path.abspath('docs/screenshots')

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.bold = True
    if level == 1:
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(16, 75, 133) # Deep Blue
    elif level == 2:
        run.font.size = Pt(13.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
    else:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_body_p(doc, text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13)
        r_pre.bold = True
        
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.italic = italic
    return p

def add_image_with_caption(doc, img_name, caption_text, width_inches=6.0):
    img_path = os.path.join(SCREENSHOTS_DIR, img_name)
    if not os.path.exists(img_path):
        print(f"Warning: Image {img_path} not found!")
        return

    # Image paragraph
    p_img = doc.add_paragraph()
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_img = p_img.add_run()
    r_img.add_picture(img_path, width=Inches(width_inches))

    # Caption paragraph
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(11)
    r_cap.bold = True
    r_cap.italic = True
    r_cap.font.color.rgb = RGBColor(71, 85, 105)

def build_report():
    print("=== ĐANG KHỞI TẠO BÁO CÁO WORD TOÀN DIỆN CÓ ĐẦY ĐỦ ẢNH MINH CHỨNG ===")
    doc = docx.Document()

    # Set 1-inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # ==========================================
    # TRANG BÌA (COVER PAGE)
    # ==========================================
    p_school = doc.add_paragraph()
    p_school.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_school.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(13)
    r1.bold = True
    r2 = p_school.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(13)
    r2.bold = True

    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_before = Pt(36)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_bck = p_title.add_run("BÁO CÁO CUỐI KỲ\n")
    r_bck.font.name = 'Times New Roman'
    r_bck.font.size = Pt(18)
    r_bck.bold = True
    r_bck.font.color.rgb = RGBColor(16, 75, 133)

    r_hp = p_title.add_run("HỌC PHẦN: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM\n\n")
    r_hp.font.name = 'Times New Roman'
    r_hp.font.size = Pt(15)
    r_hp.bold = True

    r_dt = p_title.add_run("ĐỀ TÀI 35\n")
    r_dt.font.name = 'Times New Roman'
    r_dt.font.size = Pt(16)
    r_dt.bold = True
    r_dt.font.color.rgb = RGBColor(180, 83, 9)

    r_topic = p_title.add_run("HỆ THỐNG QUIZ / THI TRẮC NGHIỆM TRỰC TUYẾN\nQUIZ SYSTEM\n")
    r_topic.font.name = 'Times New Roman'
    r_topic.font.size = Pt(16)
    r_topic.bold = True
    r_topic.font.color.rgb = RGBColor(16, 75, 133)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(48)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.left_indent = Inches(1.5)
    
    info_runs = [
        ("Sinh viên thực hiện: ", "Trần Thị Loan\n"),
        ("Mã sinh viên: ", "DTC245180058\n"),
        ("Lớp: ", "KTPM K23C\n"),
        ("Giảng viên hướng dẫn: ", "Hoàng Văn Tâm\n")
    ]
    for lbl, val in info_runs:
        r_lbl = p_info.add_run(lbl)
        r_lbl.font.name = 'Times New Roman'
        r_lbl.font.size = Pt(13)
        r_val = p_info.add_run(val)
        r_val.font.name = 'Times New Roman'
        r_val.font.size = Pt(13)
        r_val.bold = True

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_before = Pt(72)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_loc = p_loc.add_run("Thái Nguyên — 2026")
    r_loc.font.name = 'Times New Roman'
    r_loc.font.size = Pt(13)
    r_loc.bold = True

    doc.add_page_break()

    # ==========================================
    # MỤC LỤC
    # ==========================================
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_toc = p_toc_title.add_run("MỤC LỤC")
    r_toc.font.name = 'Times New Roman'
    r_toc.font.size = Pt(16)
    r_toc.bold = True
    r_toc.font.color.rgb = RGBColor(16, 75, 133)

    toc_items = [
        ("LỜI NÓI ĐẦU", "2"),
        ("CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ KIẾN TRÚC HỆ THỐNG", "2"),
        ("CHƯƠNG 2. TRIỂN KHAI WEBSITE VÀ DATABASE BẰNG DOCKER COMPOSE", "4"),
        ("CHƯƠNG 3. CẤU HÌNH NGINX REVERSE PROXY", "9"),
        ("CHƯƠNG 4. TRIỂN KHAI PROMETHEUS VÀ GRAFANA", "12"),
        ("CHƯƠNG 5. TRIỂN KHAI LOKI VÀ PROMTAIL", "17"),
        ("CHƯƠNG 6. HARDENING VÀ BẢO MẬT HỆ THỐNG", "24"),
        ("CHƯƠNG 7. QUẢN LÝ MÃ NGUỒN VỚI GIT VÀ GITHUB", "25"),
        ("CHƯƠNG 8. KẾT QUẢ TRIỂN KHAI VÀ ĐÁNH GIÁ", "27"),
        ("KẾT LUẬN", "29"),
        ("TÀI LIỆU THAM KHẢO", "29")
    ]
    for title, page in toc_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_after = Pt(4)
        r_t = p_item.add_run(title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(12)
        r_t.bold = ("CHƯƠNG" in title or "LỜI NÓI ĐẦU" in title or "KẾT LUẬN" in title)
        
        # Leader dots
        dots = " ." * int((65 - len(title)) / 2)
        r_d = p_item.add_run(dots + " " + page)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(12)

    doc.add_page_break()

    # ==========================================
    # LỜI NÓI ĐẦU & CHƯƠNG 1
    # ==========================================
    add_styled_heading(doc, "LỜI NÓI ĐẦU", 1)
    add_body_p(doc, "Việc triển khai phần mềm không chỉ dừng ở xây dựng chức năng mà còn bao gồm chuẩn bị môi trường, lưu trữ dữ liệu và theo dõi hoạt động sau khi đưa ứng dụng vào sử dụng. Docker giúp đóng gói ứng dụng cùng các thành phần phụ thuộc, còn Docker Compose cho phép mô tả nhiều dịch vụ trong các tệp cấu hình thống nhất. Cách triển khai này phù hợp với mục tiêu thực hành của học phần Triển khai và Quản trị Hệ thống Phần mềm.")
    add_body_p(doc, "Trong đề tài 35, em xây dựng và triển khai 'Hệ thống Quiz / Thi trắc nghiệm trực tuyến'. Đây là ứng dụng giáo dục thiết thực phục vụ tổ chức thi cử, kiểm tra đánh giá kiến thức với đồng hồ đếm ngược, nộp bài, tính điểm tự động và tra cứu lịch sử bài làm. Website được viết bằng Node.js kết hợp framework Express, sử dụng MySQL 8.0 để lưu trữ người dùng, đề thi, câu hỏi và bài nộp; Nginx tiếp nhận yêu cầu, xử lý mã hóa HTTPS tự ký, chuyển hướng bắt buộc HTTP sang HTTPS và chuyển tiếp đến ứng dụng. phpMyAdmin hỗ trợ quan sát dữ liệu trong quá trình kiểm tra.")
    add_body_p(doc, "Bên cạnh chức năng website, đề tài triển khai Prometheus và Grafana để thu thập, hiển thị số liệu giám sát qua 3 Dashboard chuyên dụng (Container cAdvisor, Web Server Nginx + App, Database MySQL); Loki và Promtail để tập trung nhật ký Docker và thực hiện các truy vấn LogQL. Các biện pháp hardening gồm phân tách 3 vùng mạng biệt lập, hệ thống file container chỉ đọc (read-only), non-root container, hạn chế cổng CSDL và rate limiting Nginx. Git và GitHub lưu lại toàn bộ tiến trình triển khai theo các commit rõ ràng.")
    
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sign = p_sign.add_run("Trần Thị Loan")
    r_sign.font.name = 'Times New Roman'
    r_sign.font.size = Pt(13)
    r_sign.bold = True

    add_styled_heading(doc, "CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ KIẾN TRÚC HỆ THỐNG", 1)
    add_styled_heading(doc, "1.1. Giới thiệu và mục tiêu", 2)
    add_body_p(doc, "Hệ thống Quiz cung cấp giao diện đăng nhập, đăng ký phân quyền chuẩn 3 tác nhân (Quản trị viên, Giáo viên, Sinh viên), giao diện làm bài thi trắc nghiệm trực quan với đồng hồ đếm ngược, nộp bài chấm điểm tức thời và trang lịch sử bài làm. Mục tiêu là triển khai một ứng dụng web có cơ sở dữ liệu, reverse proxy, giám sát và nhật ký tập trung hoàn toàn bằng Docker Compose. Hệ thống gồm 11 dịch vụ được điều phối thống nhất, phân tách rõ ràng giữa hạ tầng ứng dụng và hạ tầng quan sát.")

    add_styled_heading(doc, "1.2. Luồng xử lý và sơ đồ kiến trúc", 2)
    add_body_p(doc, "Người dùng truy cập HTTPS (hoặc HTTP được tự động chuyển hướng sang HTTPS) đến Nginx trên cổng 443 của máy chủ. Nginx kiểm tra SSL/TLS, thêm các security headers, áp dụng rate limit tại /login rồi chuyển tiếp yêu cầu sang app:3000 qua mạng frontend. Ứng dụng Node.js dùng connection pool kết nối MySQL qua mạng backend nội bộ bằng tài khoản quyền hạn chế quiz_user. phpMyAdmin cũng kết nối MySQL nhưng chỉ công bố giao diện tại localhost (127.0.0.1:8081) qua Docker network.")
    
    add_image_with_caption(doc, "hinh_1_1_kientruc.png", "Hình 1.1. Kiến trúc ứng dụng, giám sát và nhật ký theo cấu hình dự án.")

    add_body_p(doc, "Prometheus chủ động kéo (pull) metrics định kỳ mỗi 10 giây từ chính nó, cAdvisor, MySQL Exporter, Nginx Exporter và endpoint /metrics của ứng dụng web. Grafana truy vấn Prometheus để hiển thị số liệu qua 3 dashboard chuyên sâu. Với nhật ký, Promtail phát hiện container qua Docker socket, gán nhãn container và gửi log đến Loki; Grafana truy vấn Loki khi người quản trị dùng Explore bằng ngôn ngữ LogQL.")

    # ==========================================
    # CHƯƠNG 2
    # ==========================================
    add_styled_heading(doc, "CHƯƠNG 2. TRIỂN KHAI WEBSITE VÀ DATABASE BẰNG DOCKER COMPOSE", 1)
    add_styled_heading(doc, "2.1. Dockerfile và cấu hình ứng dụng Node.js", 2)
    add_body_p(doc, "Dockerfile của ứng dụng sử dụng image chính thức node:20-alpine nhằm tối ưu hóa kích thước và bảo mật. Lệnh npm ci --omit=dev chỉ cài đặt các thư viện sản xuất cần thiết, loại bỏ các công cụ phát triển không an toàn. Mã nguồn được đặt trong thư mục /usr/src/app và cấp quyền sở hữu cho người dùng thông thường node (uid 1000). Chỉ thị USER node kích hoạt trạng thái non-root ngay trong ảnh đóng gói. EXPOSE 3000 mô tả cổng ứng dụng; cổng này không publish trực tiếp ra máy host.")

    add_image_with_caption(doc, "hinh_2_1_dockerfile.png", "Hình 2.1. Dockerfile dùng Node.js 20 Alpine, cài đặt production và chỉ định USER node.")

    add_styled_heading(doc, "2.2. Dịch vụ và biến môi trường trong docker-compose.yml", 2)
    add_body_p(doc, "MySQL nhận các tham số khởi tạo (mật khẩu root, database, user và mật khẩu người dùng ứng dụng) từ tệp .env. Ứng dụng web được build tại thư mục ./app và chờ MySQL đạt trạng thái service_healthy mới khởi động. phpMyAdmin nhận PMA_HOST=mysql và ánh xạ cổng 8081:80 cho phép truy cập. Nginx lắng nghe cổng 80 và 443 chuyển tiếp lưu lượng vào ứng dụng.")

    add_styled_heading(doc, "2.3. Mạng, volume và điều kiện khởi động tuần tự", 2)
    add_body_p(doc, "Cơ sở dữ liệu MySQL chỉ tham gia mạng backend nội bộ; ứng dụng web và Nginx phối hợp điều hướng. Volume mysql_data lưu trữ bền vững dữ liệu tại /var/lib/mysql; tệp init.sql được mount chỉ đọc để khởi tạo CSDL với charset utf8mb4. Healthcheck chạy mysqladmin ping đảm bảo tính sẵn sàng.")

    add_image_with_caption(doc, "hinh_2_2a_compose_mysql.png", "Hình 2.2a. Cấu hình MySQL, volume, healthcheck và điều kiện phụ thuộc của ứng dụng.")
    add_image_with_caption(doc, "hinh_2_2b_compose_nginx.png", "Hình 2.2b. Phần tiếp của compose gồm Nginx, phpMyAdmin, networks và volumes.")

    add_styled_heading(doc, "2.4. Khởi tạo CSDL quiz_db và quan hệ dữ liệu", 2)
    add_body_p(doc, "Tệp mysql/init.sql tạo cơ sở dữ liệu quiz_db với bảng mã utf8mb4. Bảng users lưu trữ tài khoản, mật khẩu băm bcrypt, vai trò (admin, teacher, candidate). Bảng quizzes lưu thông tin đề thi và thời lượng. Bảng questions lưu danh mục câu hỏi và 4 đáp án lựa chọn kèm đáp án đúng. Bảng quiz_results lưu kết quả bài thi, điểm số và chi tiết câu trả lời của thí sinh.")

    add_image_with_caption(doc, "hinh_2_3_schema.png", "Hình 2.3. Lược đồ cơ sở dữ liệu quiz_db, cấu trúc bảng và khóa ngoại quan hệ.")

    add_styled_heading(doc, "2.5. Giao diện và các chức năng chính của website", 2)
    add_body_p(doc, "Website thi trắc nghiệm được thiết kế thanh lịch, hiện đại và phân quyền chặt chẽ cho 3 tác nhân:")
    add_body_p(doc, "• Quản trị viên (Admin): Toàn quyền quản lý hệ thống, quản lý tài khoản người dùng tại /admin/users, đổi vai trò và xóa tài khoản.")
    add_body_p(doc, "• Giáo viên (Teacher): Soạn đề thi mới tại /admin/quizzes/create, quản lý câu hỏi trắc nghiệm và theo dõi điểm thi của sinh viên.")
    add_body_p(doc, "• Sinh viên (Candidate): Đăng nhập nhanh bằng nút demo, làm bài thi với đồng hồ đếm ngược trực tiếp, nộp bài chấm điểm tự động và xem lịch sử làm bài.")

    add_image_with_caption(doc, "hinh_2_4_login.png", "Hình 2.4a. Giao diện Đăng nhập hệ thống với 3 nút chọn nhanh tài khoản demo.")
    add_image_with_caption(doc, "hinh_2_4_quiz_take.png", "Hình 2.4b. Giao diện Form làm bài thi trắc nghiệm trực tuyến có đồng hồ đếm ngược.")
    add_image_with_caption(doc, "hinh_2_5_result.png", "Hình 2.5a. Giao diện Kết quả thi chấm điểm tự động đạt 10.0 / 10 điểm.")
    add_image_with_caption(doc, "hinh_2_5_history.png", "Hình 2.5b. Giao diện Lịch sử bài làm của thí sinh được lưu trữ tức thời.")

    add_styled_heading(doc, "2.6. Kiểm tra dữ liệu bằng phpMyAdmin", 2)
    add_body_p(doc, "Truy cập phpMyAdmin qua cổng 8081 (http://localhost:8081). Giao diện hiển thị đầy đủ các bảng trong cơ sở dữ liệu quiz_db, dữ liệu bài thi được ghi nhận tức thời sau khi thí sinh nộp bài.")

    add_image_with_caption(doc, "hinh_2_6_phpmyadmin.png", "Hình 2.6. Bảng quiz_results và users trong phpMyAdmin chứng minh dữ liệu lưu trữ thành công.")

    # ==========================================
    # CHƯƠNG 3
    # ==========================================
    add_styled_heading(doc, "CHƯƠNG 3. CẤU HÌNH NGINX REVERSE PROXY", 1)
    add_styled_heading(doc, "3.1. Vai trò và nội dung nginx/nginx.conf", 2)
    add_body_p(doc, "Nginx đóng vai trò là điểm tiếp nhận duy nhất cho toàn bộ hệ thống. Máy chủ lắng nghe tại cổng 80 và 443 với chứng chỉ SSL tự ký, giải mã TLS rồi chuyển tiếp lưu lượng đến app:3000.")

    add_styled_heading(doc, "3.2. Security headers, HTTPS tự ký và Rate Limiting", 2)
    add_body_p(doc, "Cấu hình bảo mật tại Nginx bao gồm chứng chỉ SSL tự ký RSA 2048-bit, bộ 7 HTTP Security Headers (HSTS, X-Frame-Options: SAMEORIGIN, X-Content-Type-Options: nosniff, Content-Security-Policy), che giấu phiên bản máy chủ bằng server_tokens off.")

    add_image_with_caption(doc, "hinh_3_1_nginx_conf.png", "Hình 3.1. Cấu hình Nginx Reverse Proxy, chứng chỉ HTTPS và Security Headers.")

    add_styled_heading(doc, "3.3. Kiểm tra cấu hình và phản hồi HTTP", 2)
    add_body_p(doc, "Kiểm tra cú pháp cấu hình Nginx bằng lệnh docker compose exec nginx nginx -t cho kết quả thành công. Sử dụng curl.exe -k -I https://localhost ghi nhận phản hồi HTTP/1.1 chuyển hướng đến /login với đầy đủ các tiêu đề bảo mật.")

    add_image_with_caption(doc, "hinh_3_2_curl_https.png", "Hình 3.2. Kết quả kiểm tra Header HTTP và chứng chỉ HTTPS bằng lệnh curl.exe -kI.")

    # ==========================================
    # CHƯƠNG 4
    # ==========================================
    add_styled_heading(doc, "CHƯƠNG 4. TRIỂN KHAI PROMETHEUS VÀ GRAFANA", 1)
    add_styled_heading(doc, "4.1. Các dịch vụ giám sát trong docker-compose.yml", 2)
    add_body_p(doc, "Hạ tầng giám sát gồm Prometheus v2.51.2 lưu dữ liệu tại prometheus_data; Grafana 10.4.2 lưu cấu hình tại grafana_data, nạp tự động Datasource cùng 3 Dashboard qua cơ chế Provisioning cục bộ.")

    add_image_with_caption(doc, "hinh_4_1_prom_compose.png", "Hình 4.1. Cấu hình dịch vụ Prometheus, Grafana, cAdvisor và các Exporter trong compose.")

    add_styled_heading(doc, "4.2. prometheus/prometheus.yml và Datasource Provisioning", 2)
    add_body_p(doc, "scrape_interval được thiết lập bằng 10 giây. Các job tĩnh thu thập số liệu gồm: prometheus:9090, quiz-app:3000, cadvisor:8080, mysqld-exporter:9104 và nginx-exporter:9113.")

    add_image_with_caption(doc, "hinh_4_2_prom_yml.png", "Hình 4.2. Các job thu thập số liệu giám sát trong tệp cấu hình prometheus.yml.")

    add_styled_heading(doc, "4.3. Kiểm tra Prometheus Targets", 2)
    add_body_p(doc, "Màn hình trạng thái Targets của Prometheus tại http://localhost:9090/targets ghi nhận toàn bộ các nhóm endpoint đều hiển thị trạng thái UP (1/1) màu xanh lá.")

    add_image_with_caption(doc, "hinh_4_3_prom_targets.png", "Hình 4.3. Giao diện Prometheus Targets hiển thị đầy đủ các endpoint ở trạng thái UP.")

    add_styled_heading(doc, "4.4. Trực quan hóa 3 Dashboard chuyên sâu trên Grafana", 2)
    add_body_p(doc, "Grafana tự động nạp 3 dashboard chuyên sâu: Dashboard 1 giám sát Container (cAdvisor), Dashboard 2 giám sát Web Server Nginx & App, Dashboard 3 giám sát Database MySQL.")

    add_image_with_caption(doc, "hinh_4_4_grafana_dashboards.png", "Hình 4.4. Grafana Dashboards - Tự động nạp sẵn các dashboard giám sát hệ thống.")

    # ==========================================
    # CHƯƠNG 5
    # ==========================================
    add_styled_heading(doc, "CHƯƠNG 5. TRIỂN KHAI LOKI VÀ PROMTAIL", 1)
    add_styled_heading(doc, "5.1. Mô hình tập trung nhật ký với Loki & Promtail", 2)
    add_body_p(doc, "Hệ thống sử dụng Grafana Loki kết hợp Promtail thu thập log Nginx từ volume chia sẻ. Promtail đọc các dòng access log định dạng JSON, gắn nhãn metadata và đẩy log về Loki để lưu trữ.")

    add_image_with_caption(doc, "hinh_5_1_promtail_conf.png", "Hình 5.1. Cấu hình Promtail đọc log Nginx và đẩy về Loki.")

    add_styled_heading(doc, "5.2. Thực nghiệm truy vấn LogQL trong Grafana Explore", 2)
    add_body_p(doc, "Người quản trị có thể truy vấn nhật ký trực tiếp trên Grafana Explore (http://localhost:3001/explore) bằng câu truy vấn {job=\"quiz_nginx\"} hoặc lọc mã lỗi HTTP.")

    add_image_with_caption(doc, "hinh_5_2_grafana_explore.png", "Hình 5.2. Giao diện Grafana Explore truy vấn LogQL toàn bộ nhật ký Nginx Reverse Proxy.")

    # ==========================================
    # CHƯƠNG 6
    # ==========================================
    add_styled_heading(doc, "CHƯƠNG 6. HARDENING VÀ BẢO MẬT HỆ THỐNG", 1)
    add_styled_heading(doc, "6.1. Các biện pháp Hardening và bằng chứng thực nghiệm", 2)
    add_body_p(doc, "Hệ thống áp dụng đầy đủ 10 biện pháp bảo vệ thực tế: Non-root container (USER node uid=1000), cách ly mạng nội bộ, Least Privilege DB user (quiz_user), che giấu phiên bản Nginx, mã hóa bcrypt mật khẩu, kiểm soát biến môi trường qua .env.")

    add_image_with_caption(doc, "hinh_6_1_hardening.png", "Hình 6.1. Kiểm chứng thực tế các lệnh Hardening (Non-root, Least privilege, và trạng thái Container).")

    # ==========================================
    # CHƯƠNG 7
    # ==========================================
    add_styled_heading(doc, "CHƯƠNG 7. QUẢN LÝ MÃ NGUỒN VỚI GIT VÀ GITHUB", 1)
    add_styled_heading(doc, "7.1. Kho lưu trữ GitHub chính thức", 2)
    add_body_p(doc, "Toàn bộ mã nguồn, cấu hình hạ tầng và tài liệu được quản lý tập trung trên GitHub tại repository: https://github.com/loantranthi175-netizen/DTC245180058.")

    add_image_with_caption(doc, "hinh_7_1_github_repo.png", "Hình 7.1. Kho lưu trữ GitHub chính thức DTC245180058.")

    add_styled_heading(doc, "7.2. Lịch sử Commit và kiểm tra Git", 2)
    add_body_p(doc, "Lệnh git log --oneline hiển thị đầy đủ 3 commit chuẩn mực tương ứng 3 mốc yêu cầu của đề tài thi. Trạng thái git status xác nhận working tree sạch sẽ, đồng bộ 100% với GitHub.")

    add_image_with_caption(doc, "hinh_7_2_git_log.png", "Hình 7.2. Lệnh git log và trạng thái đồng bộ hoàn hảo với GitHub.")

    # ==========================================
    # CHƯƠNG 8 & KẾT LUẬN
    # ==========================================
    add_styled_heading(doc, "CHƯƠNG 8. KẾT QUẢ TRIỂN KHAI VÀ ĐÁNH GIÁ", 1)
    add_styled_heading(doc, "8.1. Bảng tổng hợp đối chiếu kết quả thực nghiệm", 2)
    
    # Summary Table
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Tiêu chí đánh giá"
    hdr_cells[1].text = "Minh chứng thực nghiệm"
    hdr_cells[2].text = "Trạng thái"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_margins(c, top=120, bottom=120, left=150, right=150)

    eval_data = [
        ("1. Docker Compose & Database", "11 container Up; MySQL 8.0 healthy; CSDL quiz_db lưu trữ bền vững qua volume mysql_data.", "Đạt"),
        ("2. Website qua Nginx HTTPS", "Giao diện web truy cập an toàn qua https://localhost và http://localhost; 7 Security Headers đầy đủ.", "Đạt"),
        ("3. Chức năng thi & Phân quyền 3 tác nhân", "Hỗ trợ Admin, Giáo viên, Sinh viên; Đồng hồ đếm ngược; Tự động chấm điểm 10.0/10 và lưu lịch sử.", "Đạt"),
        ("4. Prometheus Targets", "Tất cả các endpoint (app, cadvisor, nginx-exporter, mysqld-exporter) đều UP 100% màu xanh.", "Đạt"),
        ("5. Grafana 3 Dashboards", "Tự động nạp sẵn qua Provisioning giám sát Container, Web Nginx và MySQL.", "Đạt"),
        ("6. Loki & Promtail", "Thu thập log Nginx JSON, thực thi truy vấn LogQL trên Grafana Explore.", "Đạt"),
        ("7. Hardening & Bảo mật", "Non-root node (uid=1000), Least privilege DB user quiz_user, Nginx server_tokens off.", "Đạt"),
        ("8. Git & GitHub", "Đúng 3 commit chuẩn trên repo loantranthi175-netizen/DTC245180058.", "Đạt")
    ]
    for tc, mc, tt in eval_data:
        row_cells = table.add_row().cells
        row_cells[0].text = tc
        row_cells[1].text = mc
        row_cells[2].text = tt
        for c in row_cells:
            set_cell_margins(c, top=100, bottom=100, left=150, right=150)

    add_styled_heading(doc, "KẾT LUẬN", 1)
    add_body_p(doc, "Đề tài số 35 đã kết hợp thành công ứng dụng web thi trắc nghiệm trực tuyến Node.js Express với hệ sinh thái quản trị và triển khai hiện đại bằng Docker Compose. Nginx cung cấp điểm truy cập an toàn qua HTTPS; phpMyAdmin hỗ trợ quan sát dữ liệu CSDL; Prometheus và Grafana cung cấp cái nhìn trực quan về hiệu năng hệ thống qua 3 dashboard chuyên sâu; Loki và Promtail thu thập nhật ký tập trung và hỗ trợ truy vấn thông minh bằng LogQL.")
    add_body_p(doc, "Em xin chân thành cảm ơn Thầy giáo Hoàng Văn Tâm và các Thầy Cô trong Bộ môn Mạng và Hệ thống Thông tin đã tận tình hướng dẫn, truyền đạt kiến thức quý báu giúp em hoàn thành xuất sắc đề tài này!")

    add_styled_heading(doc, "TÀI LIỆU THAM KHẢO", 1)
    add_body_p(doc, "[1] Repository Đề 35 của Trần Thị Loan, nhánh main: https://github.com/loantranthi175-netizen/DTC245180058")
    add_body_p(doc, "[2] Giáo trình Triển khai và Quản trị Hệ thống Phần mềm - Bộ môn Mạng và Hệ thống Thông tin, Trường Đại học Công nghệ Thông tin và Truyền thông.")
    add_body_p(doc, "[3] Docker Documentation: Docker Compose file reference v3.8 - https://docs.docker.com/compose/")
    add_body_p(doc, "[4] Nginx Documentation: Reverse Proxy, SSL Termination and Security Headers - https://nginx.org/en/docs/")
    add_body_p(doc, "[5] Prometheus & Grafana Documentation: Provisioning Dashboards and Exporters Architecture - https://prometheus.io/ và https://grafana.com/")
    add_body_p(doc, "[6] Grafana Loki Documentation: LogQL Query Language and Promtail Service Discovery - https://grafana.com/docs/loki/latest/")

    doc.save(DOCX_OUTPUT)
    print(f"✅ BÁO CÁO WORD ĐÃ ĐƯỢC TẠO THÀNH CÔNG TẠI: {DOCX_OUTPUT}")

if __name__ == '__main__':
    build_report()
