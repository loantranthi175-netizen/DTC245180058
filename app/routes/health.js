const express = require('express');
const router = express.Router();
const { pool } = require('../config/db');

// Endpoint /health phục vụ giám sát và kiểm tra sức khỏe hệ thống
router.get('/health', async (req, res) => {
    let dbStatus = 'DISCONNECTED';
    let isHealthy = true;

    try {
        const [rows] = await pool.query('SELECT 1 AS ok');
        if (rows && rows[0] && rows[0].ok === 1) {
            dbStatus = 'CONNECTED';
        }
    } catch (err) {
        dbStatus = `ERROR: ${err.message}`;
        isHealthy = false;
    }

    const payload = {
        status: isHealthy ? 'UP' : 'DOWN',
        timestamp: new Date().toISOString(),
        uptime_seconds: Math.floor(process.uptime()),
        memory_usage_mb: Math.round(process.memoryUsage().rss / 1024 / 1024),
        database: dbStatus
    };

    const statusCode = isHealthy ? 200 : 503;
    res.status(statusCode).json(payload);
});

module.exports = router;
