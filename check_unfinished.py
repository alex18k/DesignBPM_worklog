import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor()
cursor.execute('SELECT TOP 1 * FROM UnfinishedTask')
cols = [d[0] for d in cursor.description]

print('UnfinishedTask 表字段:')
for col in cols:
    print(f'  {col}')

conn.close()