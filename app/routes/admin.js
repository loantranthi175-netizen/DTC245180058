const express = require('express');
const router = express.Router();
const { pool } = require('../config/db');

// Middleware xác thực quyền Admin hoặc Giáo viên
function requireAdminOrTeacher(req, res, next) {
    if (!req.session || !req.session.user) {
        return res.redirect('/login');
    }
    if (req.session.user.role !== 'admin' && req.session.user.role !== 'teacher') {
        return res.status(403).send('Truy cập bị từ chối: Chỉ Quản trị viên hoặc Giáo viên mới có quyền vào khu vực này.');
    }
    next();
}

// Middleware chỉ dành riêng cho Quản trị viên tối cao (Admin)
function requireOnlyAdmin(req, res, next) {
    if (!req.session || !req.session.user) {
        return res.redirect('/login');
    }
    if (req.session.user.role !== 'admin') {
        return res.status(403).send('Truy cập bị từ chối: Chức năng này yêu cầu quyền Quản trị viên (Admin).');
    }
    next();
}

router.use(requireAdminOrTeacher);

// Dashboard Quản trị viên & Giáo viên
router.get('/', async (req, res) => {
    try {
        const isTeacher = (req.session.user.role === 'teacher');
        let quizQuery = `
            SELECT q.*, 
                   COUNT(DISTINCT qu.id) AS question_count,
                   COUNT(DISTINCT qr.id) AS submission_count,
                   u.fullname AS creator_name
            FROM quizzes q
            LEFT JOIN questions qu ON q.id = qu.quiz_id
            LEFT JOIN quiz_results qr ON q.id = qr.quiz_id
            LEFT JOIN users u ON q.created_by = u.id
        `;
        let quizParams = [];
        if (isTeacher) {
            quizQuery += ` WHERE q.created_by = ? `;
            quizParams.push(req.session.user.id);
        }
        quizQuery += ` GROUP BY q.id ORDER BY q.created_at DESC`;

        const [quizzes] = await pool.query(quizQuery, quizParams);

        const [counts] = await pool.query(`
            SELECT 
                SUM(CASE WHEN role = 'candidate' THEN 1 ELSE 0 END) AS total_candidates,
                SUM(CASE WHEN role = 'teacher' THEN 1 ELSE 0 END) AS total_teachers,
                SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END) AS total_admins
            FROM users
        `);

        let resultsQuery = `
            SELECT qr.*, u.fullname, u.email, q.title AS quiz_title
            FROM quiz_results qr
            JOIN users u ON qr.user_id = u.id
            JOIN quizzes q ON qr.quiz_id = q.id
        `;
        let resultsParams = [];
        if (isTeacher) {
            resultsQuery += ` WHERE q.created_by = ? `;
            resultsParams.push(req.session.user.id);
        }
        resultsQuery += ` ORDER BY qr.submitted_at DESC LIMIT 15`;

        const [results] = await pool.query(resultsQuery, resultsParams);

        res.render('admin/dashboard', {
            quizzes,
            totalCandidates: counts[0].total_candidates || 0,
            totalTeachers: counts[0].total_teachers || 0,
            totalAdmins: counts[0].total_admins || 0,
            recentResults: results,
            isTeacher,
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

// ==============================================================================
// QUẢN LÝ NGƯỜI DÙNG (Dành riêng cho Quản trị viên - Admin)
// ==============================================================================
router.get('/users', requireOnlyAdmin, async (req, res) => {
    try {
        const [users] = await pool.query(`
            SELECT u.id, u.email, u.fullname, u.role, u.created_at,
                   COUNT(DISTINCT qr.id) as quiz_taken_count
            FROM users u
            LEFT JOIN quiz_results qr ON u.id = qr.user_id
            GROUP BY u.id
            ORDER BY u.created_at DESC
        `);

        res.render('admin/users', {
            users,
            success: req.query.success || null,
            error: req.query.error || null
        });
    } catch (err) {
        console.error('[ADMIN] Lỗi lấy danh sách người dùng:', err);
        res.status(500).send('Lỗi máy chủ khi tải danh sách người dùng.');
    }
});

// Đổi vai trò người dùng (Admin, Giáo viên, Sinh viên)
router.post('/users/:id/role', requireOnlyAdmin, async (req, res) => {
    const userId = req.params.id;
    const { role } = req.body;

    if (!['admin', 'teacher', 'candidate'].includes(role)) {
        return res.redirect('/admin/users?error=invalid_role');
    }

    try {
        await pool.query('UPDATE users SET role = ? WHERE id = ?', [role, userId]);
        res.redirect('/admin/users?success=role_updated');
    } catch (err) {
        console.error('[ADMIN] Lỗi cập nhật vai trò:', err);
        res.redirect('/admin/users?error=update_failed');
    }
});

// Xóa người dùng
router.post('/users/:id/delete', requireOnlyAdmin, async (req, res) => {
    const userId = req.params.id;

    // Không cho phép tự xóa tài khoản của chính mình
    if (parseInt(userId, 10) === req.session.user.id) {
        return res.redirect('/admin/users?error=cannot_delete_self');
    }

    try {
        await pool.query('DELETE FROM users WHERE id = ?', [userId]);
        res.redirect('/admin/users?success=user_deleted');
    } catch (err) {
        console.error('[ADMIN] Lỗi xóa người dùng:', err);
        res.redirect('/admin/users?error=delete_failed');
    }
});

module.exports = router;
