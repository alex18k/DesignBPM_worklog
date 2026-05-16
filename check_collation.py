import pymssql

conn = pymssql.connect(
    server='100.91.86.88',
    port=14330,
    user='sa',
    password='Vadmin,@3',
    database='UltimusServer_2021'
)

cursor = conn.cursor(as_dict=True)

print('数据库排序规则:')
cursor.execute('SELECT name, collation_name FROM sys.databases')
for row in cursor.fetchall():
    if 'Ultimus' in row['name']:
        print('  ', row['name'], ':', row['collation_name'])

print('表排序规则:')
cursor.execute('SELECT TABLE_NAME, TABLE_COLLATION FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ''UnfinishedTask''')
tbl = cursor.fetchone()
print('  ', tbl['TABLE_NAME'], ':', tbl['TABLE_COLLATION'])

print('列排序规则:')
cursor.execute('SELECT COLUMN_NAME, COLLATION_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ''UnfinishedTask''')
for col in cursor.fetchall():
    print('  ', col['COLUMN_NAME'], ':', col['COLLATION_NAME'])

conn.close()