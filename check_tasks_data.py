import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor(as_dict=True)
cursor.execute('SELECT TOP 5 PROCESSNAME, STEPLABEL FROM TASKS WHERE PROCESSNAME LIKE %s', ('%订单评审流程%',))

for row in cursor.fetchall():
    print('PROCESSNAME:', repr(row['PROCESSNAME']))
    print('STEPLABEL:', repr(row['STEPLABEL']))
    print('---')

conn.close()