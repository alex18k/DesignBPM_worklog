import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor()

print('检查类型...')
cursor.execute('''
    SELECT 
        t.INCIDENT AS t_inc, t.STEPID AS t_step,
        w.INCIDENT AS w_inc, w.stepid AS w_step
    FROM worklog w
    LEFT JOIN TASKS t ON w.INCIDENT = t.INCIDENT AND w.stepid = t.STEPID
''')

for row in cursor.fetchall():
    print('TASKS: INCIDENT=', row[0], type(row[0]), 'STEPID=', row[1], type(row[1]))
    print('worklog: INCIDENT=', row[2], type(row[2]), 'stepid=', row[3], type(row[3]))
    print('Match:', (row[0], row[1]) == (row[2], row[3]))
    print('---')

conn.close()