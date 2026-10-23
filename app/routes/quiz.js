const express = require('express');
const router = express.Router();
const { pool } = require('../config/db');

// Middleware yêu cầu đăng nhập
function requireAuth(req, res, next) {
    if (!req.session || !req.session.user) {
        return res.redirect('/login');
    }
    next();
}

router.use(requireAuth);

// Trang chủ điều hướng
router.get('/', (req, res) => {
    if (req.session.user.role === 'admin') {
        return res.redirect('/admin');
    }
    res.redirect('/quizzes');
});

// Danh sách đề thi cho thí sinh
router.get('/quizzes', async (req, res) => {
    try {
        const [quizzes] = await pool.query(`
            SELECT q.*, COUNT(qu.id) AS question_count
            FROM quizzes q
            LEFT JOIN questions qu ON q.id = qu.quiz_id
            GROUP BY q.id
            ORDER BY q.created_at DESC
        `);

        // Lấy lịch sử làm bài gần đây của thí sinh
        const [myRecentResults] = await pool.query(`
            SELECT qr.*, q.title AS quiz_title
            FROM quiz_results qr
            JOIN quizzes q ON qr.quiz_id = q.id
            WHERE qr.user_id = ?
            ORDER BY qr.submitted_at DESC
            LIMIT 5
        `, [req.session.user.id]);

        res.render('quiz/index', {
            quizzes,
            myRecentResults
        });
    } catch (err) {
        console.error('[QUIZ] Lỗi lấy danh sách đề thi:', err);
        res.status(500).send('Lỗi máy chủ khi tải danh sách đề thi.');
    }
});

// Trang làm bài thi
router.get('/quizzes/:id/take', async (req, res) => {
    const quizId = req.params.id;

    try {
        const [quizRows] = await pool.query('SELECT * FROM quizzes WHERE id = ?', [quizId]);
        if (quizRows.length === 0) {
            return res.status(404).send('Không tìm thấy bài thi.');
        }

        const [questions] = await pool.query(
            'SELECT id, quiz_id, content, option_a, option_b, option_c, option_d FROM questions WHERE quiz_id = ? ORDER BY id ASC',
            [quizId]
        );

        if (questions.length === 0) {
            return res.render('quiz/take', {
                quiz: quizRows[0],
                questions: [],
                error: 'Đề thi này hiện tại chưa có câu hỏi nào để làm bài.'
            });
        }

        res.render('quiz/take', {
            quiz: quizRows[0],
            questions,
            error: null
        });
    } catch (err) {
        console.error('[QUIZ] Lỗi tải đề thi:', err);
        res.status(500).send('Lỗi máy chủ khi tải bài thi.');
    }
});

// Xử lý nộp bài & Chấm điểm tự động
router.post('/quizzes/:id/submit', async (req, res) => {
    const quizId = req.params.id;
    const userAnswers = req.body; // { q_1: 'B', q_2: 'C', ... }

    try {
        const [questions] = await pool.query(
            'SELECT id, correct_option FROM questions WHERE quiz_id = ?',
            [quizId]
        );

        const totalQuestions = questions.length;
        if (totalQuestions === 0) {
            return res.redirect('/quizzes');
        }

        let correctCount = 0;
        for (const q of questions) {
            const answerKey = `q_${q.id}`;
            const chosenAnswer = userAnswers[answerKey];
            if (chosenAnswer && chosenAnswer.toUpperCase() === q.correct_option.toUpperCase()) {
                correctCount++;
            }
        }

        // Tính điểm trên thang điểm 10
        const calculatedScore = Math.round((correctCount / totalQuestions) * 10 * 10) / 10;

        const [insertResult] = await pool.query(
            'INSERT INTO quiz_results (quiz_id, user_id, score, total_questions, correct_answers) VALUES (?, ?, ?, ?, ?)',
            [quizId, req.session.user.id, calculatedScore, totalQuestions, correctCount]
        );

        res.redirect(`/quizzes/results/${insertResult.insertId}`);
    } catch (err) {
        console.error('[QUIZ] Lỗi chấm bài thi:', err);
        res.status(500).send('Lỗi máy chủ khi xử lý nộp bài.');
    }
});

// Xem kết quả bài thi
router.get('/quizzes/results/:resultId', async (req, res) => {
    const resultId = req.params.resultId;

    try {
        const [rows] = await pool.query(`
            SELECT qr.*, q.title AS quiz_title, q.description AS quiz_description, u.fullname, u.email
            FROM quiz_results qr
            JOIN quizzes q ON qr.quiz_id = q.id
            JOIN users u ON qr.user_id = u.id
            WHERE qr.id = ?
        `, [resultId]);

        if (rows.length === 0) {
            return res.status(404).send('Không tìm thấy kết quả.');
        }

        const result = rows[0];
        // Đảm bảo chính thí sinh làm bài, giáo viên hoặc admin mới xem được
        if (result.user_id !== req.session.user.id && req.session.user.role !== 'admin' && req.session.user.role !== 'teacher') {
            return res.status(403).send('Bạn không có quyền xem kết quả bài thi này.');
        }

        res.render('quiz/result', { result });
    } catch (err) {
        console.error('[QUIZ] Lỗi lấy kết quả bài thi:', err);
        res.status(500).send('Lỗi máy chủ khi tải kết quả.');
    }
});

// Lịch sử làm bài của thí sinh
router.get('/history', async (req, res) => {
    try {
        const [results] = await pool.query(`
            SELECT qr.*, q.title AS quiz_title
            FROM quiz_results qr
            JOIN quizzes q ON qr.quiz_id = q.id
            WHERE qr.user_id = ?
            ORDER BY qr.submitted_at DESC
        `, [req.session.user.id]);

        res.render('quiz/history', { results });
    } catch (err) {
        console.error('[QUIZ] Lỗi tải lịch sử:', err);
        res.status(500).send('Lỗi máy chủ khi tải lịch sử.');
    }
});

module.exports = router;
