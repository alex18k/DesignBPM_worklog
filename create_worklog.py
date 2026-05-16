import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor()

sql = '''
CREATE TABLE worklog (
    id INT IDENTITY(1,1) PRIMARY KEY,
    INCIDENT INT,
    stepid INT,
    workdate DATE,
    spendtime INT
)
'''

try:
    cursor.execute(sql)
    conn.commit()
    print('表创建成功!')
except Exception as e:
    print(f'错误: {e}')

conn.close()