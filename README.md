# 设计任务管理系统

基于现有 SQL Server 数据库开发，用于管理设计任务的流程记录和工时统计。

## 技术栈

| 组件 | 选择 |
|------|------|
| 后端框架 | Python Flask |
| 数据库 | SQL Server (UltimusServer_2021) |
| 前端 | Bootstrap 5 + Jinja2 模板 |
| 运行环境 | Python 3.x |
| 数据库驱动 | pymssql |

## 项目结构

```
/home/sa/app/bpmapp/
├── app.py                 # Flask 主程序
├── config.py              # 数据库配置
├── requirements.txt      # 依赖清单
└── templates/
    ├── login.html        # 登录页面
    ├── work.html         # 工时记录页面
    └── task.html         # 任务管理页面
```

## 功能模块

### 1. 用户登录
- 根据 userid 登录，验证用户是否存在
- 支持 user100、user101 等测试用户登录

### 2. 工时记录
- 显示当前用户的进行中任务
- 同一任务可记录多条工时
- 支持添加、修改、删除工时记录
- 显示工时合计

### 3. 任务管理
- 显示当前用户所有任务
- 更新任务状态 (pending/in_progress/completed)
- 按规则更新日期字段 (startdate/enddate/newenddate)

## 快速开始

### 1. 安装依赖

```bash
pip3 install flask pymssql
```

### 2. 启动服务

```bash
cd /home/sa/app/bpmapp
python3 app.py
```

### 3. 访问系统

打开浏览器访问 http://localhost:5000

## 测试用户

| UserID | 角色 |
|--------|------|
| user100 | 普通用户 |
| user101 | 普通用户 |
| admin001 | 管理员 |

## 数据库配置

默认配置 (config.py):
```python
DB_CONFIG = {
    'server': '100.91.86.88',
    'port': 14330,
    'database': 'UltimusServer_2021',
    'user': 'sa',
    'password': 'Vadmin,@3'
}
```

## 后续优化建议

1. **AD域登录集成**: 对接 Windows AD 域认证
2. **权限管理**: 不同角色查看不同范围的任务
3. **数据导出**: 导出工时报表为 Excel
4. **移动端适配**: 优化手机端使用体验
5. **消息通知**: 任务状态变更提醒