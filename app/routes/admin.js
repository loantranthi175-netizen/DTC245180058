const express = require('express');
const router = express.Router();
const { pool } = require('../config/db');

// Middleware xác thực quyền Admin
function requireAdmin(req, res, next) {
    if (!req.session || !req.session.user) {
        return res.redirect('/login');
    }
    if (req.session.user.role !== 'admin') {
        return res.status(403).send('Truy cập bị từ chối: Chỉ quản trị viên mới có quyền vào khu vực này.');
    }
    next();
}

router.use(requireAdmin);

// Dashboard Quản trị viên
router.get('/', async (req, res) => {
    try {
        const [quizzes] = await pool.query(`
            SELECT q.*, 
                   COUNT(DISTINCT qu.id) AS question_count,
                   COUNT(DISTINCT qr.id) AS submission_count
            FROM quizzes q
            LEFT JOIN questions qu ON q.id = qu.quiz_id
            LEFT JOIN quiz_results qr ON q.id = qr.quiz_id
            GROUP BY q.id
            ORDER BY q.created_at DESC
        `);

        const [users] = await pool.query('SELECT COUNT(*) AS total_users FROM users WHERE role = "candidate"');
        const [results] = await pool.query(`
            SELECT qr.*, u.fullname, u.email, q.title AS quiz_title
            FROM quiz_results qr
            JOIN users u ON qr.user_id = u.id
            JOIN quizzes q ON qr.quiz_id = q.id
            ORDER BY qr.submitted_at DESC
            LIMIT 10
        `);

        res.render('admin/dashboard', {
            quizzes,
            totalCandidates: users[0].total_users,
            recentResults: results,
            error: null,
            success: req.query.success || null
        });
    } catch (err) {
        console.error('[ADMIN] Lỗi tải dashboard:', err);
        res.status(500).send('Lỗi máy chủ khi tải trang quản trị.');
    }
});

// Trang tạo đề thi mới
router.get('/quizzes/create', (req, res) => {
    res.render('admin/create-quiz', { error: null });
});

// Xử lý tạo đề thi mới
router.post('/quizzes/create', async (req, res) => {
    const { title, description, time_limit } = req.body;

    if (!title) {
        return res.render('admin/create-quiz', { error: 'Tiêu đề bài thi không được để trống.' });
    }

    try {
        const [result] = await pool.query(
            'INSERT INTO quizzes (title, description, time_limit, created_by) VALUES (?, ?, ?, ?)',
            [title.trim(), description ? description.trim() : '', parseInt(time_limit || '15', 10), req.session.user.id]
        );

        // Chuyển hướng sang trang thêm câu hỏi cho đề vừa tạo
        res.redirect(`/admin/quizzes/${result.insertId}/questions?created=1`);
    } catch (err) {
        console.error('[ADMIN] Lỗi tạo bài thi:', err);
        res.render('admin/create-quiz', { error: 'Không thể tạo bài thi lúc này.' });
    }
});

// Trang quản lý câu hỏi của một đề thi
router.get('/quizzes/:id/questions', async (req, res) => {
    const quizId = req.params.id;
    try {
        const [quizRows] = await pool.query('SELECT * FROM quizzes WHERE id = ?', [quizId]);
        if (quizRows.length === 0) {
            return res.status(404).send('Không tìm thấy bài thi.');
        }

        const [questions] = await pool.query(
            'SELECT * FROM questions WHERE quiz_id = ? ORDER BY id ASC',
            [quizId]
        );

        res.render('admin/questions', {
            quiz: quizRows[0],
            questions,
            error: null,
            success: req.query.created ? 'Tạo đề thi thành công! Bây giờ hãy thêm các câu hỏi.' : (req.query.added ? 'Đã thêm câu hỏi thành công!' : null)
        });
    } catch (err) {
        console.error('[ADMIN] Lỗi lấy câu hỏi:', err);
        res.status(500).send('Lỗi máy chủ khi tải câu hỏi.');
    }
});

// Thêm câu hỏi vào đề thi
router.post('/quizzes/:id/questions', async (req, res) => {
    const quizId = req.params.id;
    const { content, option_a, option_b, option_c, option_d, correct_option } = req.body;

    if (!content || !option_a || !option_b || !option_c || !option_d || !correct_option) {
        return res.redirect(`/admin/quizzes/${quizId}/questions?error=missing_fields`);
    }

    try {
        await pool.query(
            'INSERT INTO questions (quiz_id, content, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?)',
            [quizId, content.trim(), option_a.trim(), option_b.trim(), option_c.trim(), option_d.trim(), correct_option.toUpperCase()]
        );

        res.redirect(`/admin/quizzes/${quizId}/questions?added=1`);
    } catch (err) {
        console.error('[ADMIN] Lỗi thêm câu hỏi:', err);
        res.status(500).send('Lỗi máy chủ khi lưu câu hỏi.');
    }
});

// Xóa câu hỏi
router.post('/quizzes/:quizId/questions/:questionId/delete', async (req, res) => {
    const { quizId, questionId } = req.params;
    try {
        await pool.query('DELETE FROM questions WHERE id = ? AND quiz_id = ?', [questionId, quizId]);
        res.redirect(`/admin/quizzes/${quizId}/questions`);
    } catch (err) {
        console.error('[ADMIN] Lỗi xóa câu hỏi:', err);
        res.status(500).send('Lỗi máy chủ khi xóa câu hỏi.');
    }
});

// Xóa đề thi
router.post('/quizzes/:id/delete', async (req, res) => {
    const quizId = req.params.id;
    try {
        await pool.query('DELETE FROM quizzes WHERE id = ?', [quizId]);
        res.redirect('/admin?success=deleted');
    } catch (err) {
        console.error('[ADMIN] Lỗi xóa bài thi:', err);
        res.status(500).send('Lỗi máy chủ khi xóa bài thi.');
    }
});

module.exports = router;
