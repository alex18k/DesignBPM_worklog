import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor()
cursor.execute(
    '''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME'''
)

tables = cursor.fetchall()
print(f'共 {len(tables)} 张表:')
for t in tables:
    print(f'  {t[0]}')

conn.close()