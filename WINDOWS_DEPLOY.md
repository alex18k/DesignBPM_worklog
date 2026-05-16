# Windows Server 部署指南

## 环境要求
- Windows Server 2016/2019/2022
- Python 3.8+
- SQL Server 2016+

## 步骤 1: 安装 Python

下载并安装 Python: https://www.python.org/downloads/

建议使用 Python 3.10 或更高版本。

安装时勾选 "Add Python to PATH"

## 步骤 2: 安装 SQL Server ODBC 驱动

下载地址: https://docs.microsoft.com/zh-cn/sql/connect/odbc/download-odbc-driver-for-sql-server

选择 "ODBC Driver 17 for SQL Server" 或 "ODBC Driver 18"

## 步骤 3: 安装 Python 依赖

```powershell
pip install pymssql flask
```

或安装项目依赖:
```powershell
pip install -r requirements.txt
```

## 步骤 4: 配置数据库连接

编辑 `config.py`，修改数据库地址:

```python
# Windows Server 上的配置
DB_CONFIG = {
    'server': 'localhost',      # 或 SQL Server 服务器地址
    'port': 1433,
    'database': 'bpmapp',
    'user': 'sa',
    'password': 'BpmApp2024!'
}
```

## 步骤 5: 确保 SQL Server 允许 TCP/IP 连接

1. 打开 SQL Server 配置管理器
2. 确保 "TCP/IP" 协议已启用
3. 端口设置为 1433

## 步骤 6: 开放防火墙端口 (如需远程连接)

```powershell
New-NetFirewallRule -DisplayName "SQL Server" -Direction Inbound -Protocol TCP -LocalPort 1433 -Action Allow
```

## 步骤 7: 启动应用

```powershell
python app.py
```

## 常见问题

### 1. pymssql 连接报错
如遇编码问题，改用 pyodbc:
```python
pip install pyodbc
```

### 2. 中文乱码
在连接字符串添加 charset:
```python
conn = pymssql.connect(..., charset='utf8')
```

### 3. 请确保 SQL Server 允许混合身份验证
在 SQL Server 配置管理器中确认。