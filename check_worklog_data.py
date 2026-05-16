import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor()
cursor.execute('SELECT TOP 1 * FROM worklog')
cols = [d[0] for d in cursor.description]
print('worklog 列:', cols)

print('\nworklog 数据:')
cursor.execute('SELECT TOP 10 * FROM worklog ORDER BY id DESC')
for row in cursor.fetchall():
    print('  id:', row[0], ', INCIDENT:', row[1], ', STEPID:', row[2], ', workdate:', row[3])

conn.close()