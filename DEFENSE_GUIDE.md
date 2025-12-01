# 答辩讲稿与展示要点

面向现场展示：强调**数据封装层**与**MVC 分层**，并解释“接口”是自建 HTTP 接口（JSON），不是只有第三方 API。

## 讲稿提纲（可直接照读）
1) 场景：做一个“课程推荐/概要”接口服务，数据来自 MySQL，本地课程/评论；还整合外部 openai-proxy 生成主题概要。
2) 分层/MVC：
   - Model：`courses/models.py`（`Course`/`Review`，指定 `db_table`，只生成两张业务表）。
   - Controller(View)：`courses/views.py`，处理路由、取数、聚合、统一 JSON。
   - View(Template)：`templates/index.html`，简列可用接口，证明模板层存在；主要输出 JSON。
3) 数据封装层：
   - 本地数据：手写 `serialize_course/serialize_review`（`views.py`）把 ORM -> JSON 友好格式（Decimal -> float，datetime -> ISO）。
   - 外部数据：`openai_client.py` 调用 `gpt-4o-mini`（openai-proxy），带少量重试；成功后转换为 `{data_source, payload}` 统一格式；若仍失败，视图返回 502 + 错误信息（无 mock）。
4) 接口示例（展示 JSON）：
   - `/api/courses/` 列表（含 `data_source: mysql`）
   - `/api/courses/<id>/` 详情 + 评论（已通过 fixtures/reviews.json 预填）
   - `/api/stats/` 汇总统计
   - `/api/ai-summary?topic=Django` 外部接口封装
5) “接口”与“业务逻辑层”说明：
   - “接口”= 我们对外暴露的 HTTP JSON；不是只有第三方。
   - 控制层 `views.py` 里包含简单业务逻辑（聚合、统一返回）；若要更严格三层，可再拆出 `services.py`，本 demo 为最小实现。
6) 纯净性：`settings.py` 去掉 admin/auth/sessions，只保留必要组件，迁移只会生成两张表。
7) 总结：展示代码文件与 JSON 返回即可，无需复杂前端。

## 现场可展示的文件
- `courses/models.py`：表结构与 `db_table`。
- `courses/views.py`：路由、业务逻辑、序列化。
- `courses/openai_client.py`：外部接口封装与统一返回。
- `course_portal/settings.py`：精简配置、最少依赖。
- `mysql_init.sql`：建表与示例数据。
- `templates/index.html`：View 层存在证明。

## JSON 示例（可贴 PPT）
1) `/api/courses/`
```json
{
  "data_source": "mysql",
  "items": [
    {
      "id": 1,
      "title": "Python 基础",
      "category": "编程",
      "level": "初级",
      "duration_hours": 20,
      "teacher": "Alice",
      "price": 199.0,
      "rating_avg": 4.6,
      "rating_count": 120
    }
  ]
}
```

2) `/api/courses/1/`
```json
{
  "id": 1,
  "title": "Python 基础",
  "description": "从零学 Python，语法 + 函数 + 模块",
  "category": "编程",
  "level": "初级",
  "duration_hours": 20,
  "teacher": "Alice",
  "price": 199.0,
  "rating_avg": 4.6,
  "rating_count": 120,
  "reviews": [
    {"student_name": "学生甲", "rating": 5, "comment": "讲解通俗易懂，例子多", "created_at": "2025-01-01T10:00:00"}
  ]
}
```

3) `/api/stats/`
```json
{
  "stats": {
    "course_count": 8,
    "avg_price": 266.125,
    "avg_rating": 4.58
  }
}
```

4) `/api/ai-summary?topic=Django`
```json
{
  "data_source": "openai-proxy",
  "payload": {
    "topic": "Django",
    "summary": "Django MVC 架构与快速开发要点。",
    "provider": "openai-proxy"
  }
}
```

## 现场操作备选
- 若不现场跑：打开上述文件 + PPT JSON 示例。
- 若可现场跑：`pip install -r requirements.txt` → `python manage.py migrate` → `python manage.py runserver`，浏览器访问 `/api/...` 路由。若外部接口失败，会返回 502 + 错误信息。
