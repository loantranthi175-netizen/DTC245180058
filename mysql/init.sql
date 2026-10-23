-- Khởi tạo Database cho Hệ thống Quiz (Đề 35)
-- Môn: Triển khai và Quản trị Hệ thống Phần mềm
-- Sinh viên: DTC245180058

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS `quiz_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `quiz_db`;

-- 1. Bảng người dùng (3 tác nhân: admin, teacher, candidate)
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `fullname` VARCHAR(100) NOT NULL,
    `role` ENUM('admin', 'teacher', 'candidate') DEFAULT 'candidate',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Bảng đề thi (Quizzes)
CREATE TABLE IF NOT EXISTS `quizzes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `time_limit` INT DEFAULT 15 COMMENT 'Thời gian làm bài tính bằng phút',
    `created_by` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_quiz_user` FOREIGN KEY (`created_by`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Bảng câu hỏi trắc nghiệm
CREATE TABLE IF NOT EXISTS `questions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `quiz_id` INT NOT NULL,
    `content` TEXT NOT NULL,
    `option_a` TEXT NOT NULL,
    `option_b` TEXT NOT NULL,
    `option_c` TEXT NOT NULL,
    `option_d` TEXT NOT NULL,
    `correct_option` CHAR(1) NOT NULL COMMENT 'A, B, C, hoặc D',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_question_quiz` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Bảng kết quả làm bài của thí sinh
CREATE TABLE IF NOT EXISTS `quiz_results` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `quiz_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `score` DECIMAL(4, 1) NOT NULL,
    `total_questions` INT NOT NULL,
    `correct_answers` INT NOT NULL,
    `submitted_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_result_quiz` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_result_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- SEED DỮ LIỆU MẪU ĐẦY ĐỦ 3 TÁC NHÂN (Admin, Giáo viên, Sinh viên)
-- ==============================================================================
-- Admin: admin@quiz.local / Admin@123
-- Giáo viên: teacher@quiz.local / Teacher@123
-- Sinh viên: student@quiz.local / Student@123
INSERT INTO `users` (`id`, `email`, `password`, `fullname`, `role`) VALUES
(1, 'admin@quiz.local', '$2a$10$hxSTRnTEjoEKw.qTSH.y.e6tdG3moOOhX6ABLWo0tZFJFL5XG0Qdu', 'Quản trị viên Hệ thống', 'admin'),
(2, 'teacher@quiz.local', '$2a$10$9rmwCS3uQ4QwsViSlzCFiOtAG48BWuCQp64RU/9YEArKTmUurjp4W', 'Thầy Giáo Viên (Giảng viên)', 'teacher'),
(3, 'student@quiz.local', '$2a$10$25W2aKt9ASHifQMdvAzfzOnHReAE.PZd/uWP8ycnQIKpGM9pxsm22', 'Nguyễn Văn Sinh Viên (DTC245180058)', 'candidate')
ON DUPLICATE KEY UPDATE `password`=VALUES(`password`), `fullname`=VALUES(`fullname`), `role`=VALUES(`role`);

-- Đề thi mẫu: Kiến thức Docker & DevOps Cơ bản (5 câu)
INSERT INTO `quizzes` (`id`, `title`, `description`, `time_limit`, `created_by`) VALUES
(1, 'Kiến thức Docker & DevOps Cơ bản', 'Bài kiểm tra đánh giá kiến thức cơ bản về container, Docker Compose, Nginx và hệ thống giám sát.', 15, 2)
ON DUPLICATE KEY UPDATE `title`=VALUES(`title`), `description`=VALUES(`description`);

-- 5 câu hỏi trắc nghiệm chuẩn tiếng Việt
INSERT INTO `questions` (`id`, `quiz_id`, `content`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_option`) VALUES
(1, 1, 'Lệnh nào trong Docker CLI dùng để xây dựng một Docker Image từ Dockerfile?', 'docker run', 'docker build', 'docker compose', 'docker pull', 'B'),
(2, 1, 'Tập tin cấu hình chuẩn nào được dùng để định nghĩa và chạy nhiều container cùng lúc?', 'Dockerfile', '.env', 'docker-compose.yml', 'nginx.conf', 'C'),
(3, 1, 'Trong docker-compose.yml, chỉ thị nào dùng để gắn kết thư mục giữa máy host và container?', 'ports', 'volumes', 'environment', 'restart', 'B'),
(4, 1, 'Vai trò chính của Nginx Reverse Proxy trong kiến trúc hệ thống là gì?', 'Thay thế hoàn toàn cơ sở dữ liệu', 'Định tuyến request, cân bằng tải, quản lý SSL/TLS và bảo mật', 'Tự động biên dịch mã nguồn Node.js', 'Lưu trữ dữ liệu dài hạn', 'B'),
(5, 1, 'Thành phần nào thu thập các thông số tài nguyên (CPU, RAM, Network) từ container cho Prometheus?', 'mysqld-exporter', 'Grafana', 'Promtail', 'cAdvisor', 'D')
ON DUPLICATE KEY UPDATE `content`=VALUES(`content`), `option_a`=VALUES(`option_a`), `option_b`=VALUES(`option_b`), `option_c`=VALUES(`option_c`), `option_d`=VALUES(`option_d`);
