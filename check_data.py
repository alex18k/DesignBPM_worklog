import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor(as_dict=True)
cursor.execute('SELECT TOP 5 INCIDENT, stepid, PROCESSNAME FROM UnfinishedTask')

print('UnfinishedTask:')
for row in cursor.fetchall():
    print('  INCIDENT:', row['INCIDENT'], ', stepid:', row['stepid'], ', PROCESSNAME:', row['PROCESSNAME'].strip())

cursor.execute('SELECT TOP 5 INCIDENT, STEPID, PROCESSNAME FROM TASKS WHERE PROCESSNAME LIKE %s AND STATUS = 1', ('%订单评审流程%',))

print('TASKS:')
for row in cursor.fetchall():
    print('  INCIDENT:', row['INCIDENT'], ', STEPID:', row['STEPID'], ', PROCESSNAME:', row['PROCESSNAME'].strip())

conn.close()