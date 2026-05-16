import pymssql
from datetime import datetime

DB_CONFIG = {
    'server': '100.91.86.88',
    'port': 14330,
    'database': 'UltimusServer_2021',
    'user': 'sa',
    'password': 'Vadmin,@3'
}

def get_db_connection():
    return pymssql.connect(**DB_CONFIG)

def fix_collation(conn):
    cursor = conn.cursor()
    print('   修正列排序规则...')
    sql = '''
        ALTER TABLE UnfinishedTask ALTER COLUMN PROCESSNAME NVARCHAR(200) COLLATE Chinese_PRC_CI_AS;
        ALTER TABLE UnfinishedTask ALTER COLUMN STEPLABEL NVARCHAR(200) COLLATE Chinese_PRC_CI_AS;
        ALTER TABLE UnfinishedTask ALTER COLUMN ASSIGNEDTOUSER NVARCHAR(500) COLLATE Chinese_PRC_CI_AS;
        ALTER TABLE UnfinishedTask ALTER COLUMN USERID_AFTER_SLASH NVARCHAR(100) COLLATE Chinese_PRC_CI_AS;
        ALTER TABLE UnfinishedTask ALTER COLUMN UserID NVARCHAR(100) COLLATE Chinese_PRC_CI_AS;
        ALTER TABLE UnfinishedTask ALTER COLUMN Name NVARCHAR(100) COLLATE Chinese_PRC_CI_AS;
        ALTER TABLE UnfinishedTask ALTER COLUMN status NVARCHAR(50) COLLATE Chinese_PRC_CI_AS;
    '''
    try:
        for stmt in sql.split(';'):
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)
        conn.commit()
    except Exception as e:
        pass

def sync_unfinished_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(as_dict=True)
    
    fix_collation(conn)
    
    print('1. 获取未完成任务 (订单评审流程)...')
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
    print(f'   获取到 {len(tasks)} 条任务')
    
    print('2. 获取 UnfinishedTask 现有记录...')
    cursor.execute('SELECT INCIDENT, stepid FROM UnfinishedTask')
    existing = {(row['INCIDENT'], row['stepid']) for row in cursor.fetchall()}
    print(f'   现有 {len(existing)} 条记录')
    
    print('3. 对比并插入新数据...')
    insert_sql = '''
        INSERT INTO UnfinishedTask (
            PROCESSNAME, INCIDENT, stepid, STEPLABEL, 
            ASSIGNEDTOUSER, USERID_AFTER_SLASH, UserID, Name
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    '''
    
    inserted = 0
    skipped = 0
    errors = 0
    for task in tasks:
        key = (task['INCIDENT'], task['STEPID'])
        if key in existing:
            skipped += 1
            continue
        
        try:
            cursor.execute(insert_sql, (
                task['PROCESSNAME'],
                task['INCIDENT'],
                task['STEPID'],
                task['STEPLABEL'],
                task['ASSIGNEDTOUSER'],
                task['USERID_AFTER_SLASH'],
                task['USERID'],
                task['Name']
            ))
            inserted += 1
        except Exception as e:
            errors += 1
    
    conn.commit()
    print(f'   跳过 {skipped} 条, 新增 {inserted} 条, 错误 {errors} 条')
    
    print('4. 验证结果...')
    cursor.execute('SELECT COUNT(*) AS cnt FROM UnfinishedTask')
    count = cursor.fetchone()['cnt']
    print(f'   UnfinishedTask 表当前记录数: {count}')
    
    cursor.execute('SELECT TOP 3 PROCESSNAME, STEPLABEL FROM UnfinishedTask')
    for row in cursor.fetchall():
        print('   ', row['PROCESSNAME'].strip(), '-', row['STEPLABEL'].strip())
    
    conn.close()
    print('同步完成!')
    return {'inserted': inserted, 'skipped': skipped, 'total': count}

if __name__ == '__main__':
    result = sync_unfinished_tasks()
    print(f'同步完成: 新增 {result["inserted"]} 条, 跳过 {result["skipped"]} 条, 总计 {result["total"]} 条')