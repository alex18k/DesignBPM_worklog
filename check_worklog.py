import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor()
cursor.execute('SELECT * FROM worklog')

print('worklog 表创建成功!')
print('列:', [desc[0] for desc in cursor.description])
print('当前数据: 0 条')

conn.close()