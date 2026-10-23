const mysql = require('mysql2/promise');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

let mysqlPool = null;
let sqliteDb = null;
let activeEngine = 'mysql';

// Cấu hình kết nối MySQL
function createMysqlPool() {
    return mysql.createPool({
        host: process.env.DB_HOST || 'mysql',
        port: parseInt(process.env.DB_PORT || '3306', 10),
        user: process.env.DB_USER || 'quiz_user',
        password: process.env.DB_PASSWORD || '060606',
        database: process.env.DB_NAME || 'quiz_db',
        waitForConnections: true,
        connectionLimit: 10,
        queueLimit: 0,
        charset: 'utf8mb4'
    });
}

// Khởi tạo SQLite làm chế độ dự phòng nếu MySQL container chưa bật
function initSqliteFallback() {
    const dbPath = path.join(__dirname, '..', 'quiz_db.sqlite');
    sqliteDb = new sqlite3.Database(dbPath);

    sqliteDb.serialize(() => {
        // 1. Users
        sqliteDb.run(`
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                fullname TEXT NOT NULL,
                role TEXT DEFAULT 'candidate',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // 2. Quizzes
        sqliteDb.run(`
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                time_limit INTEGER DEFAULT 15,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // 3. Questions
        sqliteDb.run(`
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_option TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // 4. Quiz Results
        sqliteDb.run(`
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                score REAL NOT NULL,
                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL,
                submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // Seed data
        sqliteDb.run(`
            INSERT OR IGNORE INTO users (id, email, password, fullname, role) VALUES
            (1, 'admin@quiz.local', '$2a$10$Mf7mia1Ow27ZEiApku3Vo.7s2OT3YeuZkFEhUidXriWzLxnc88Rym', 'Quản trị viên Hệ thống', 'admin'),
            (2, 'student@quiz.local', '$2a$10$mCfL2shWR2loMo4BKkY20eRdPitghFuNaIrtpvjtrWm7k6oCx2nTK', 'Nguyễn Văn Thí Sinh', 'candidate')
        `);

        sqliteDb.run(`
            INSERT OR IGNORE INTO quizzes (id, title, description, time_limit, created_by) VALUES
            (1, 'Kiến thức Docker & DevOps Cơ bản', 'Bài kiểm tra đánh giá kiến thức cơ bản về container, Docker Compose, Nginx và hệ thống giám sát.', 15, 1)
        `);

        sqliteDb.run(`
            INSERT OR IGNORE INTO questions (id, quiz_id, content, option_a, option_b, option_c, option_d, correct_option) VALUES
            (1, 1, 'Lệnh nào trong Docker CLI dùng để xây dựng một Docker Image từ Dockerfile?', 'docker run', 'docker build', 'docker compose', 'docker pull', 'B'),
            (2, 1, 'Tập tin cấu hình chuẩn nào được dùng để định nghĩa và chạy nhiều container cùng lúc?', 'Dockerfile', '.env', 'docker-compose.yml', 'nginx.conf', 'C'),
            (3, 1, 'Trong docker-compose.yml, chỉ thị nào dùng để gắn kết thư mục giữa máy host và container?', 'ports', 'volumes', 'environment', 'restart', 'B'),
            (4, 1, 'Vai trò chính của Nginx Reverse Proxy trong kiến trúc hệ thống là gì?', 'Thay thế hoàn toàn cơ sở dữ liệu', 'Định tuyến request, cân bằng tải, quản lý SSL/TLS và bảo mật', 'Tự động biên dịch mã nguồn Node.js', 'Lưu trữ dữ liệu dài hạn', 'B'),
            (5, 1, 'Thành phần nào thu thập các thông số tài nguyên (CPU, RAM, Network) từ container cho Prometheus?', 'mysqld-exporter', 'Grafana', 'Promtail', 'cAdvisor', 'D')
        `);
    });

    console.log('[DB] Đã kích hoạt cơ sở dữ liệu SQLite dự phòng (sẵn sàng phục vụ tức thì).');
}

// Wrapper thống nhất trả về Promise dạng [rows, fields]
const pool = {
    async query(sql, params = []) {
        if (activeEngine === 'mysql' && mysqlPool) {
            try {
                return await mysqlPool.query(sql, params);
            } catch (err) {
                // Nếu mất kết nối MySQL và có SQLite, chuyển sang fallback
                if (sqliteDb) {
                    activeEngine = 'sqlite';
                    return this.querySqlite(sql, params);
                }
                throw err;
            }
        } else {
            return this.querySqlite(sql, params);
        }
    },

    querySqlite(sql, params = []) {
        return new Promise((resolve, reject) => {
            const cleanSql = sql.trim();
            const isSelect = /^SELECT/i.test(cleanSql);

            if (isSelect) {
                sqliteDb.all(cleanSql, params, (err, rows) => {
                    if (err) return reject(err);
                    resolve([rows || [], []]);
                });
            } else {
                sqliteDb.run(cleanSql, params, function (err) {
                    if (err) return reject(err);
                    resolve([{ insertId: this.lastID, affectedRows: this.changes }, []]);
                });
            }
        });
    }
};

// Kiểm tra kết nối khi khởi động
async function testConnection(retries = 3, delayMs = 1500) {
    mysqlPool = createMysqlPool();
    for (let i = 1; i <= retries; i++) {
        try {
            const connection = await mysqlPool.getConnection();
            console.log(`[DB] Kết nối MySQL thành công tới database '${process.env.DB_NAME || 'quiz_db'}'`);
            connection.release();
            activeEngine = 'mysql';
            return true;
        } catch (err) {
            if (i === retries) {
                console.warn('[DB] Không thể kết nối tới MySQL container. Chuyển sang chế độ dữ liệu cục bộ.');
                activeEngine = 'sqlite';
                initSqliteFallback();
                return true;
            }
            await new Promise(res => setTimeout(res, delayMs));
        }
    }
}

module.exports = { pool, testConnection };
