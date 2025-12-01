-- Minimal MySQL schema for the demo (no Django auth/admin tables).
CREATE DATABASE IF NOT EXISTS course_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE course_portal;

DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS course;

CREATE TABLE course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    level VARCHAR(50) NOT NULL,
    duration_hours INT NOT NULL,
    teacher VARCHAR(100) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    rating_avg DECIMAL(3,2) NOT NULL DEFAULT 0.0,
    rating_count INT NOT NULL DEFAULT 0
);

CREATE TABLE review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    rating TINYINT NOT NULL,
    comment TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE
);

INSERT INTO course (title, description, category, level, duration_hours, teacher, price, rating_avg, rating_count) VALUES
('Python 基础', '从零学 Python，语法 + 函数 + 模块', '编程', '初级', 20, 'Alice', 199.00, 4.6, 120),
('Django Web 开发', '搭建 MVC 风格的 Web 应用', '后端', '中级', 24, 'Bob', 299.00, 4.7, 85),
('前端快速入门', 'HTML/CSS/JS 速成', '前端', '初级', 16, 'Carol', 149.00, 4.5, 140),
('数据分析入门', 'Pandas + 可视化案例', '数据', '中级', 18, 'David', 259.00, 4.8, 95),
('数据库设计', '范式、索引、事务案例', '数据库', '中级', 22, 'Ellen', 279.00, 4.6, 70),
('机器学习概览', '常见模型与应用场景', 'AI', '进阶', 26, 'Frank', 359.00, 4.4, 60),
('小程序开发', '微信小程序端到端', '移动', '初级', 14, 'Grace', 189.00, 4.3, 40),
('微服务基础', '服务拆分、接口设计、网关', '后端', '进阶', 28, 'Henry', 399.00, 4.5, 55),
('Go 微服务进阶', 'Go 语言实现微服务与并发模式', '后端', '进阶', 30, 'Ivan', 429.00, 4.6, 45),
('React 全栈', 'React + API 集成 + 部署', '前端', '中级', 26, 'Jenny', 329.00, 4.5, 80),
('数据可视化实战', 'ECharts/Matplotlib/交互式报表', '数据', '中级', 20, 'Ken', 279.00, 4.7, 65),
('NLP 基础', '文本预处理、常见模型、应用示例', 'AI', '中级', 24, 'Lucy', 349.00, 4.4, 50),
('DevOps 入门', 'CI/CD、容器化、监控告警', '运维', '中级', 22, 'Mike', 309.00, 4.6, 58),
('Redis 高级应用', '缓存模式、分布式锁、持久化', '后端', '中级', 18, 'Nina', 259.00, 4.5, 62);

INSERT INTO review (course_id, student_name, rating, comment) VALUES
(1, '学生甲', 5, '讲解通俗易懂，例子多'),
(1, '学生乙', 4, '适合零基础'),
(2, '学生丙', 5, 'MVC 思路清晰，代码规范'),
(2, '学生丁', 4, '案例贴近实战'),
(3, '学生戊', 4, '对初学者友好'),
(4, '学生己', 5, '数据可视化部分很实用'),
(5, '学生庚', 5, '数据库范式讲得很细'),
(6, '学生辛', 4, '对常见算法有概览'),
(7, '学生壬', 4, '微信端流程清楚'),
(8, '学生癸', 5, '接口设计部分收获最大'),
(9, '学生甲甲', 5, 'Go 并发部分讲得清楚'),
(10, '学生乙乙', 4, '前后端联调示例很实用'),
(11, '学生丙丙', 5, '配色与交互案例丰富'),
(12, '学生丁丁', 4, 'NLP 入门易懂，有实战'),
(13, '学生戊戊', 5, 'CI/CD 和容器化演示到位'),
(14, '学生己己', 4, '缓存与分布式锁讲得透');
