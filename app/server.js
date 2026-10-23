require('dotenv').config();
const express = require('express');
const session = require('express-session');
const path = require('path');
const { testConnection } = require('./config/db');

const app = express();
const PORT = parseInt(process.env.PORT || '3000', 10);

// 1. Bộ đếm và Middleware ghi log request ra stdout (chuẩn DevOps phục vụ Prometheus/Loki)
let totalHttpRequests = 0;
let totalHttpErrors = 0;

app.use((req, res, next) => {
    totalHttpRequests++;
    const startTime = Date.now();
    const clientIp = req.headers['x-forwarded-for'] || req.socket.remoteAddress || '-';

    res.on('finish', () => {
        if (res.statusCode >= 500) totalHttpErrors++;
        const duration = Date.now() - startTime;
        const now = new Date().toISOString();
        // Định dạng log tiêu chuẩn có cấu trúc
        console.log(`[${now}] ${req.method} ${req.originalUrl} ${res.statusCode} ${duration}ms - IP: ${clientIp}`);
    });

    next();
});

// Endpoint metrics chuẩn Prometheus (không cần thư viện bên ngoài)
app.get('/metrics', (req, res) => {
    const mem = process.memoryUsage();
    const uptime = process.uptime();
    const lines = [
        '# HELP nodejs_uptime_seconds Process uptime in seconds.',
        '# TYPE nodejs_uptime_seconds gauge',
        `nodejs_uptime_seconds ${uptime}`,
        '# HELP nodejs_memory_heap_used_bytes Process heap memory used in bytes.',
        '# TYPE nodejs_memory_heap_used_bytes gauge',
        `nodejs_memory_heap_used_bytes ${mem.heapUsed}`,
        '# HELP nodejs_memory_heap_total_bytes Process heap memory total in bytes.',
        '# TYPE nodejs_memory_heap_total_bytes gauge',
        `nodejs_memory_heap_total_bytes ${mem.heapTotal}`,
        '# HELP nodejs_memory_rss_bytes Process RSS memory in bytes.',
        '# TYPE nodejs_memory_rss_bytes gauge',
        `nodejs_memory_rss_bytes ${mem.rss}`,
        '# HELP http_requests_total Total number of HTTP requests.',
        '# TYPE http_requests_total counter',
        `http_requests_total ${totalHttpRequests}`,
        '# HELP http_errors_total Total number of 5xx HTTP errors.',
        '# TYPE http_errors_total counter',
        `http_errors_total ${totalHttpErrors}`
    ];
    res.set('Content-Type', 'text/plain; version=0.0.4');
    res.send(lines.join('\n') + '\n');
});

// 2. Parse request body
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// 3. Static files
app.use(express.static(path.join(__dirname, 'public')));

// 4. View engine (EJS)
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// 5. Session
app.use(session({
    secret: process.env.SESSION_SECRET || 'quiz_super_secure_session_key_2026',
    resave: false,
    saveUninitialized: false,
    cookie: {
        maxAge: 1000 * 60 * 60 * 8, // 8 giờ
        httpOnly: true,
        sameSite: 'lax'
    }
}));

// 6. Truyền user session vào biến toàn cục của view EJS
app.use((req, res, next) => {
    res.locals.user = req.session.user || null;
    res.locals.currentPath = req.path;
    next();
});

// 7. Định tuyến ứng dụng
const healthRoutes = require('./routes/health');
const authRoutes = require('./routes/auth');
const adminRoutes = require('./routes/admin');
const quizRoutes = require('./routes/quiz');

app.use(healthRoutes); // /health
app.use(authRoutes);   // /login, /register, /logout
app.use('/admin', adminRoutes);
app.use('/', quizRoutes); // /quizzes, /history, /take...

// 8. Xử lý trang 404
app.use((req, res) => {
    res.status(404).render('404', { title: 'Trang không tồn tại' });
});

// 9. Xử lý lỗi tập trung
app.use((err, req, res, next) => {
    console.error('[SERVER ERROR]', err);
    res.status(500).send('Đã xảy ra lỗi nội bộ máy chủ.');
});

// Khởi chạy server và kiểm tra kết nối DB
async function startServer() {
    console.log('[APP] Đang khởi tạo ứng dụng Quiz System...');
    testConnection().catch(err => console.error('[DB Startup Error]', err));

    app.listen(PORT, '0.0.0.0', () => {
        console.log(`[APP] 🚀 Quiz App đang chạy tại http://0.0.0.0:${PORT}`);
        console.log(`[APP] 👉 Health check endpoint: http://0.0.0.0:${PORT}/health`);
    });
}

startServer();
