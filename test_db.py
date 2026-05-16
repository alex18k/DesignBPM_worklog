import pymssql

try:
    conn = pymssql.connect(
        server='100.91.86.88',
        port=14330,
        user='sa',
        password='Vadmin,@3',
        database='UltimusServer_2021'
    )
    print('连接成功!')
    cursor = conn.cursor()
    cursor.execute('SELECT @@VERSION')
    print(cursor.fetchone()[0][:100])
    conn.close()
except Exception as e:
    print(f'连接失败: {e}')