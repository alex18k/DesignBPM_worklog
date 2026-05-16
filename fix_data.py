import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor()

print('1. 修改列的排序规则为 Chinese_PRC_CI_AS...')
sql = '''
    ALTER TABLE UnfinishedTask 
    ALTER COLUMN PROCESSNAME NVARCHAR(200) COLLATE Chinese_PRC_CI_AS;
    ALTER TABLE UnfinishedTask 
    ALTER COLUMN STEPLABEL NVARCHAR(200) COLLATE Chinese_PRC_CI_AS;
    ALTER TABLE UnfinishedTask 
    ALTER COLUMN ASSIGNEDTOUSER NVARCHAR(500) COLLATE Chinese_PRC_CI_AS;
    ALTER TABLE UnfinishedTask 
    ALTER COLUMN USERID_AFTER_SLASH NVARCHAR(100) COLLATE Chinese_PRC_CI_AS;
    ALTER TABLE UnfinishedTask 
    ALTER COLUMN UserID NVARCHAR(100) COLLATE Chinese_PRC_CI_AS;
    ALTER TABLE UnfinishedTask 
    ALTER COLUMN Name NVARCHAR(100) COLLATE Chinese_PRC_CI_AS;
    ALTER TABLE UnfinishedTask 
    ALTER COLUMN status NVARCHAR(50) COLLATE Chinese_PRC_CI_AS;
'''
try:
    for stmt in sql.split(';'):
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)
    conn.commit()
    print('   修改完成')
except Exception as e:
    print('   错误:', e)

print('2. 清空并重新同步...')
cursor.execute('DELETE FROM UnfinishedTask')
conn.commit()

sql = '''
    SELECT 
        TASKS.PROCESSNAME,
        TASKS.INCIDENT,
        TASKS.STEPID,
        TASKS.STEPLABEL,
        TASKS.ASSIGNEDTOUSER,
        SUBSTRING(TASKS.ASSIGNEDTOUSER, CHARINDEX('/', TASKS.ASSIGNEDTOUSER) + 1, LEN(TASKS.ASSIGNEDTOUSER)) AS USERID_AFTER_SLASH,
        QMS_Basic_Users.USERID,
        QMS_Basic_Users.Name
    FROM TASKS
    LEFT JOIN QMS_Basic_Users 
        ON SUBSTRING(TASKS.ASSIGNEDTOUSER, CHARINDEX('/', TASKS.ASSIGNEDTOUSER) + 1, LEN(TASKS.ASSIGNEDTOUSER)) = QMS_Basic_Users.USERID 
    WHERE 
        PROCESSNAME LIKE %s 
        AND STEPID NOT LIKE %s 
        AND STEPID NOT LIKE %s 
        AND STEPID NOT LIKE %s 
        AND STEPID NOT LIKE %s 
        AND STATUS = 1  
        AND ASSIGNEDTOUSER <> %s
'''
params = ('%订单评审流程%', '%522202%', '%457928%', '%5629532B%', '%425236%', 'SYSTEMUSER')
cursor.execute(sql, params)
tasks = cursor.fetchall()

insert_sql = '''
    INSERT INTO UnfinishedTask (
        PROCESSNAME, INCIDENT, stepid, STEPLABEL, 
        ASSIGNEDTOUSER, USERID_AFTER_SLASH, UserID, Name
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s
    )
'''

for task in tasks:
    cursor.execute(insert_sql, (
        task[0],  # PROCESSNAME
        task[1],  # INCIDENT
        task[2],  # STEPID
        task[3],  # STEPLABEL
        task[4],  # ASSIGNEDTOUSER
        task[5],  # USERID_AFTER_SLASH
        task[6],  # USERID
        task[7]   # Name
    ))

conn.commit()
print('   插入完成')

print('3. 验证结果...')
cursor.execute('SELECT TOP 5 PROCESSNAME FROM UnfinishedTask')
for row in cursor.fetchall():
    print('   PROCESSNAME:', repr(row[0]))

conn.close()
print('完成!')