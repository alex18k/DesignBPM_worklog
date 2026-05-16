#!/usr/bin/env python3
import mysql.connector

conn = mysql.connector.connect(
    unix_socket='/var/run/mysqld/mysqld.sock',
    user='root',
    password=''
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS xlsx_data CHARACTER SET utf8mb4")
cursor.execute("USE xlsx_data")

cursor.execute("DROP TABLE IF EXISTS UnfinishedTask")
cursor.execute("""
CREATE TABLE UnfinishedTask (
    PROCESSNAME VARCHAR(255),
    INCIDENT INT, stepid INT, STEPLABEL VARCHAR(255),
    ASSIGNEDTOUSER VARCHAR(255), USERID_AFTER_SLASH VARCHAR(255),
    UserID VARCHAR(255), Name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    startdate DATE, enddate DATE, newenddate DATE,
    UNIQUE KEY idx_incident_stepid (INCIDENT, stepid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")

cursor.execute("DROP TABLE IF EXISTS worklog")
cursor.execute("""
CREATE TABLE worklog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    INCIDENT INT, stepid INT, workdate DATE, spendtime INT, userid VARCHAR(50),
    UNIQUE KEY idx_incident_stepid (INCIDENT, stepid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")

tasks = [
    ('设计流程1', 1001, 1, '需求分析', 'user100', 'user100', 'user100', '张三', 'pending', None, None, None),
    ('设计流程1', 1001, 2, '方案设计', 'user100', 'user100', 'user100', '张三', 'in_progress', '2026-04-10', None, None),
    ('设计流程1', 1001, 3, '图纸绘制', 'user100', 'user100', 'user100', '张三', 'pending', None, None, None),
    ('设计流程2', 1002, 1, '初步设计', 'user100', 'user100', 'user100', '张三', 'completed', '2026-04-05', '2026-04-08', None),
    ('设计流程2', 1002, 2, '详细设计', 'user100', 'user100', 'user100', '张三', 'pending', None, None, None),
    ('设计流程3', 1003, 1, '现场勘测', 'user101', 'user101', 'user101', '李四', 'pending', None, None, None),
    ('设计流程3', 1003, 2, '方案制定', 'user101', 'user101', 'user101', '李四', 'pending', None, None, None),
    ('设计流程4', 1004, 1, '项目启动', 'admin001', 'admin001', 'admin001', '管理员', 'pending', None, None, None),
]

cursor.executemany("""
INSERT INTO UnfinishedTask VALUES 
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", tasks)

cursor.execute("INSERT INTO worklog VALUES (1001, 1, '2026-04-10', 120)")
cursor.execute("INSERT INTO worklog VALUES (1002, 1, '2026-04-06', 180)")

conn.commit()
cursor.execute("SELECT COUNT(*) FROM UnfinishedTask")
print(f"Database setup complete! {cursor.fetchone()[0]} tasks created.")

conn.close()
