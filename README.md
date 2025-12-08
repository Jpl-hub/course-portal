## 运行
```bash
python manage.py runserver 0.0.0.0:8000
```
访问：
- `http://127.0.0.1:8000/` 路由说明页
- `http://127.0.0.1:8000/api/courses/` 课程列表 JSON
- `http://127.0.0.1:8000/api/courses/1/` 详情+评论
- `http://127.0.0.1:8000/api/students/S001/reviews/` 学生评价过的课程
- `http://127.0.0.1:8000/api/stats/` 汇总统计
- `http://127.0.0.1:8000/api/ai-summary?topic=Django` 外部接口封装



## 路由
- `/`：模板页，列出 API
- `/api/courses/`：课程列表
- `/api/courses/<id>/`：课程详情 + 评论
- `/api/students/<student_id>/reviews/`：按学生 ID 查询其已评价课程
- `/api/stats/`：汇总统计
- `/api/ai-summary?topic=xxx`：外部接口封装

