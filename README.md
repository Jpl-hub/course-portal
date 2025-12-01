# 课程门户接口封装（course_portal）— Django 小项目

聚焦两点：**封装对外接口（JSON）** 与 **MVC 分层**。本项目不做前端页面，API 可直接供前端/移动端/其他服务调用；本文件主要说明项目结构、安装、运行、自测；答辩讲稿与展示要点见 `DEFENSE_GUIDE.md`。

## 项目结构
- `course_portal/settings.py`：精简配置，去掉 admin/auth/sessions，避免生成多余表。
- `courses/models.py`：`Course`、`Review` 两张表。
- `courses/views.py`：控制层（Django 视图），处理请求、调用数据层/外部接口、封装 JSON。
- `courses/openai_client.py`：外部接口封装，统一输出格式，并带简单重试降低偶发网络抖动。
- `courses/urls.py` / `course_portal/urls.py`：路由。
- `templates/index.html`：极简模板，列出 API。
- 数据脚本：`mysql_init.sql`（建表+示例数据），`fixtures/courses.json`（课程 fixture），`fixtures/reviews.json`（评论 fixture）。
- 文档：`README.md`（本地运行），`DEFENSE_GUIDE.md`（答辩要点）。

## 准备隔离环境（推荐）
```powershell
cd D:\code\finalwork\course_portal
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

## 配置与数据
- MySQL 连接：在 `.env` 写入（示例见 `.env.example`）
  - `MYSQL_DATABASE=course_portal`
  - `MYSQL_USER=root`
  - `MYSQL_PASSWORD=example`
  - `MYSQL_HOST=localhost`
  - `MYSQL_PORT=3306`
- 外部接口 key（可选）：`OPENAI_API_KEY=your_key`。默认调用 `gpt-4o-mini`；
- 本项目已在 `settings.py` 中自动加载 `.env`，只需复制 `.env.example` 为 `.env` 并填值，无需手工导出环境变量。
- 准备数据（推荐：Django 迁移 + fixture）：
  ```bash
  # 先确保数据库存在
  mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS course_portal CHARACTER SET utf8mb4;"
  python manage.py migrate      # 只会生成 course/review 两表（已提供迁移文件，无需 makemigrations）
  python manage.py loaddata fixtures/courses.json fixtures/reviews.json
  ```

## 运行项目
```bash
python manage.py runserver 0.0.0.0:8000
```
访问：
- `http://127.0.0.1:8000/` 路由说明页
- `http://127.0.0.1:8000/api/courses/` 课程列表 JSON
- `http://127.0.0.1:8000/api/courses/1/` 详情+评论
- `http://127.0.0.1:8000/api/stats/` 汇总统计
- `http://127.0.0.1:8000/api/ai-summary?topic=Django` 外部接口封装

## 数据封装位置（代码速览）
- 手写序列化：`courses/views.py` 中 `serialize_course/serialize_review` 将 ORM -> JSON 友好结构（Decimal -> float，datetime -> ISO）。
- 外部接口封装：`courses/openai_client.py` 将第三方响应转为统一轻量结构，不透传原始字段；内置少量重试，若仍失败会抛出异常，由视图包装为错误响应。
- 控制层：`courses/views.py` 负责路由、调用封装、统一返回 JSON；在“三层”视角下也可以理解为控制层 + 简单业务逻辑层。

## 路由
- `/`：模板页，列出 API
- `/api/courses/`：课程列表
- `/api/courses/<id>/`：课程详情 + 评论
- `/api/stats/`：汇总统计
- `/api/ai-summary?topic=xxx`：外部接口封装

## 关于“接口/业务逻辑层”的说明
- 这里的“接口”是指我们自己对外暴露的 HTTP 接口（JSON），不是狭义的第三方 API；外部 openai-proxy 只是展示“多数据源 + 封装”的例子。
- 代码里的 `views.py` 同时承担控制层和简单的业务逻辑（聚合、统一返回），数据访问由 ORM 模型完成；如果要严格分层，可再加 `services.py` 把业务逻辑拆出去（当前示例保持最小化）。
