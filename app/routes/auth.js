const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const { pool } = require('../config/db');

// Trang đăng nhập
router.get('/login', (req, res) => {
    if (req.session && req.session.user) {
        return res.redirect(req.session.user.role === 'admin' ? '/admin' : '/quizzes');
    }
    res.render('auth/login', { error: null, success: req.query.registered ? 'Đăng ký thành công! Hãy đăng nhập.' : null });
});

// Xử lý đăng nhập
router.post('/login', async (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return res.render('auth/login', { error: 'Vui lòng nhập đầy đủ Email và Mật khẩu.', success: null });
    }

    try {
        const [rows] = await pool.query('SELECT * FROM users WHERE email = ?', [email.trim()]);
        if (rows.length === 0) {
            return res.render('auth/login', { error: 'Email hoặc mật khẩu không chính xác.', success: null });
        }

        const user = rows[0];
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.render('auth/login', { error: 'Email hoặc mật khẩu không chính xác.', success: null });
        }

        // Lưu thông tin người dùng vào session
        req.session.user = {
            id: user.id,
            email: user.email,
            fullname: user.fullname,
            role: user.role
        };

        if (user.role === 'admin') {
            return res.redirect('/admin');
        } else {
            return res.redirect('/quizzes');
        }
    } catch (err) {
        console.error('[AUTH] Lỗi đăng nhập:', err);
        return res.render('auth/login', { error: 'Có lỗi xảy ra trong quá trình xử lý, vui lòng thử lại.', success: null });
    }
});

// Trang đăng ký
router.get('/register', (req, res) => {
    if (req.session && req.session.user) {
        return res.redirect('/');
    }
    res.render('auth/register', { error: null });
});

// Xử lý đăng ký
router.post('/register', async (req, res) => {
    const { email, password, fullname, role } = req.body;

    if (!email || !password || !fullname) {
        return res.render('auth/register', { error: 'Vui lòng điền đầy đủ các thông tin bắt buộc.' });
    }

    if (password.length < 6) {
        return res.render('auth/register', { error: 'Mật khẩu phải chứa ít nhất 6 ký tự.' });
    }

    const assignedRole = (role === 'admin') ? 'admin' : 'candidate';

    try {
        // Kiểm tra email trùng lặp
        const [existing] = await pool.query('SELECT id FROM users WHERE email = ?', [email.trim()]);
        if (existing.length > 0) {
            return res.render('auth/register', { error: 'Email này đã được sử dụng. Vui lòng chọn email khác.' });
        }

        // Băm mật khẩu với bcrypt
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        await pool.query(
            'INSERT INTO users (email, password, fullname, role) VALUES (?, ?, ?, ?)',
            [email.trim(), hashedPassword, fullname.trim(), assignedRole]
        );

        return res.redirect('/login?registered=1');
    } catch (err) {
        console.error('[AUTH] Lỗi đăng ký:', err);
        return res.render('auth/register', { error: 'Không thể tạo tài khoản lúc này, vui lòng thử lại.' });
    }
});

// Đăng xuất
router.get('/logout', (req, res) => {
    req.session.destroy(() => {
        res.redirect('/login');
    });
});

module.exports = router;
