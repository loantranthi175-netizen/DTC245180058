require('dotenv').config();
const express = require('express');
const session = require('express-session');
const path = require('path');
const { testConnection } = require('./config/db');

const app = express();
const PORT = parseInt(process.env.PORT || '3000', 10);

// 1. Middleware ghi log request ra stdout (chuẩn DevOps phục vụ Promtail/Loki)
app.use((req, res, next) => {
    const startTime = Date.now();
    const clientIp = req.headers['x-forwarded-for'] || req.socket.remoteAddress || '-';

    res.on('finish', () => {
        const duration = Date.now() - startTime;
        const now = new Date().toISOString();
        // Định dạng log tiêu chuẩn có cấu trúc
        console.log(`[${now}] ${req.method} ${req.originalUrl} ${res.statusCode} ${duration}ms - IP: ${clientIp}`);
    });

    next();
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
