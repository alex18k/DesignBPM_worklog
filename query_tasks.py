import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor(as_dict=True)

sql = '''
SELECT 
    TASKS.PROCESSNAME,
    TASKS.INCIDENT,
    tasks.STEPID,
    TASKS.STEPLABEL,
    TASKS.ASSIGNEDTOUSER,
    SUBSTRING(TASKS.ASSIGNEDTOUSER, CHARINDEX('/', TASKS.ASSIGNEDTOUSER) + 1, LEN(TASKS.ASSIGNEDTOUSER)) AS USERID_AFTER_SLASH,
    QMS_Basic_Users.*
FROM TASKS
LEFT JOIN QMS_Basic_Users 
    ON SUBSTRING(TASKS.ASSIGNEDTOUSER, CHARINDEX('/', TASKS.ASSIGNEDTOUSER) + 1, LEN(TASKS.ASSIGNEDTOUSER)) = QMS_Basic_Users.USERID 
WHERE 
    PROCESSNAME LIKE N'%订单评审流程%' 
    AND STEPID NOT LIKE N'%522202%' 
    AND STEPID NOT LIKE N'%457928%' 
    AND STEPID NOT LIKE N'%5629532B%' 
    AND STEPID NOT LIKE N'%425236%' 
    AND STATUS = 1  
    AND ASSIGNEDTOUSER<>'SYSTEMUSER'
ORDER BY QMS_Basic_Users.UserId
'''

cursor.execute(sql)
rows = cursor.fetchall()

print(f'共 {len(rows)} 条记录:\n')
for row in rows:
    print(f'INCIDENT: {row['INCIDENT']}, STEPID: {row['STEPID']}, USERID: {row['USERID_AFTER_SLASH']}, NAME: {row.get('UserName', '')}')

conn.close()