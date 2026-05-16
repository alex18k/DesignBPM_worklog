from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymssql
from datetime import datetime, date
from config import DB_CONFIG
from bpm_sync import sync_unfinished_tasks

app = Flask(__name__)
app.secret_key = 'bpmapp_secret_key_2024'

_db_conn = None

def get_db_connection():
    global _db_conn
    try:
        if _db_conn and _db_conn.connected:
            return _db_conn
    except:
        pass
    
    try:
        _db_conn = pymssql.connect(**DB_CONFIG)
        return _db_conn
    except pymssql.Error as err:
        print(f'Database connection error: {err}')
        return None

def close_db_connection():
    global _db_conn
    try:
        if _db_conn and _db_conn.connected:
            _db_conn.close()
    except:
        pass
    _db_conn = None

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_db_connection()

def to_date(value):
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    return datetime.strptime(str(value), '%Y-%m-%d').date()

def extract_userid(assigned_to_user):
    if not assigned_to_user:
        return None
    if '/' in assigned_to_user:
        return assigned_to_user.split('/')[-1].strip()
    return assigned_to_user.strip()

def query_all(sql, params=None):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(sql, params or ())
        results = cursor.fetchall()
        cursor.close()
        return results
    except pymssql.Error as err:
        print(f'Query error: {err}')
        return []

def query_one(sql, params=None):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(sql, params or ())
        result = cursor.fetchone()
        cursor.close()
        return result
    except pymssql.Error as err:
        print(f'Query error: {err}')
        return None

def execute_sql(sql, params=None):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        cursor.close()
        return True
    except pymssql.Error as err:
        print(f'Execute error: {err}')
        return False

@app.route('/')
def index():
    if 'userid' in session:
        return redirect(url_for('work'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('userid', '').strip()
        
        if not userid:
            flash('请输入用户ID', 'error')
            return render_template('login.html')
        
        sql = '''
            SELECT DISTINCT ASSIGNEDTOUSER
            FROM TASKS 
            WHERE SUBSTRING(ASSIGNEDTOUSER, CHARINDEX('/', ASSIGNEDTOUSER) + 1, LEN(ASSIGNEDTOUSER)) = %s
              AND ASSIGNEDTOUSER <> 'SYSTEMUSER'
        '''
        users = query_all(sql, (userid,))
        
        if users:
            session['userid'] = userid
            user = query_one('SELECT Name FROM QMS_Basic_Users WHERE USERID = %s', (userid,))
            session['username'] = user['Name'] if user and user.get('Name') else userid
            sync_unfinished_tasks()
            return redirect(url_for('work'))
        else:
            flash('用户不存在', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/work', methods=['GET', 'POST'])
def work():
    if 'userid' not in session:
        return redirect(url_for('login'))
    
    userid = session['userid']
    action = request.args.get('action')
    
    if action == 'delete':
        log_id = request.args.get('id')
        sql = 'DELETE FROM worklog WHERE id = %s'
        execute_sql(sql, (log_id,))
        flash('工时记录已删除', 'success')
        return redirect(url_for('work'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        incident = request.form.get('incident')
        stepid = request.form.get('stepid')
        workdate = request.form.get('workdate')
        spendtime = request.form.get('spendtime')
        
        if action == 'edit':
            log_id = request.form.get('log_id')
            sql = 'UPDATE worklog SET workdate = %s, spendtime = %s, userid = %s WHERE id = %s'
            execute_sql(sql, (workdate, spendtime, userid, log_id))
            flash('工时记录已修改', 'success')
        elif action == 'add':
            if incident and stepid and workdate and spendtime:
                sql = 'INSERT INTO worklog (INCIDENT, stepid, workdate, spendtime, userid) VALUES (%s, %s, %s, %s, %s)'
                execute_sql(sql, (incident, stepid, workdate, spendtime, userid))
                flash('工时记录已保存', 'success')
    
    sql = f'''
        SELECT PROCESSNAME, INCIDENT, STEPID, STEPLABEL, ASSIGNEDTOUSER, STATUS
        FROM TASKS 
        WHERE SUBSTRING(ASSIGNEDTOUSER, CHARINDEX('/', ASSIGNEDTOUSER) + 1, LEN(ASSIGNEDTOUSER)) = %s
          AND STATUS = 1
          AND ASSIGNEDTOUSER <> 'SYSTEMUSER'
        ORDER BY INCIDENT, STEPID
    '''
    tasks = query_all(sql, (userid,))
    
    for task in tasks:
        task['USERID'] = extract_userid(task['ASSIGNEDTOUSER'])
    
    sql_log = 'SELECT id, INCIDENT, stepid, workdate, spendtime, userid FROM worklog ORDER BY workdate DESC'
    logs = query_all(sql_log)
    logs_dict = {}
    for log in logs:
        key = (log['INCIDENT'], log['stepid'])
        if key not in logs_dict:
            logs_dict[key] = []
        logs_dict[key].append(log)
    
    return render_template('work.html', tasks=tasks, logs=logs_dict, userid=userid, username=session.get('username', userid))

@app.route('/task', methods=['GET', 'POST'])
def task():
    if 'userid' not in session:
        return redirect(url_for('login'))
    
    userid = session['userid']
    
    if request.method == 'POST':
        action = request.form.get('action')
        incident = request.form.get('incident')
        stepid = request.form.get('stepid')
        
        if action == 'update_status':
            status = request.form.get('status')
            sql = 'UPDATE UnfinishedTask SET status = %s WHERE INCIDENT = %s AND RTRIM(stepid) = %s'
            execute_sql(sql, (status, incident, stepid))
            flash('状态已更新', 'success')
        elif action == 'update_date':
            field = request.form.get('field')
            value = request.form.get('value')
            
            if not value:
                flash('日期不能为空', 'error')
                return redirect(url_for('task'))
            
            # 查询当前任务的日期状态
            current = query_one('SELECT startdate, enddate, newenddate FROM UnfinishedTask WHERE INCIDENT = %s AND RTRIM(stepid) = %s', (incident, stepid))
            if not current:
                flash('任务不存在', 'error')
                return redirect(url_for('task'))
            
            # 验证日期逻辑
            startdate = current.get('startdate')
            enddate = current.get('enddate')
            newenddate = current.get('newenddate')
            
            if field == 'startdate':
                if enddate and value > enddate.strftime('%Y-%m-%d'):
                    flash('开始日期不能大于结束日期', 'error')
                    return redirect(url_for('task'))
                if newenddate and value > newenddate.strftime('%Y-%m-%d'):
                    flash('开始日期不能大于延期日期', 'error')
                    return redirect(url_for('task'))
            elif field == 'enddate':
                if not startdate:
                    flash('请先设置开始日期', 'error')
                    return redirect(url_for('task'))
                if value < startdate.strftime('%Y-%m-%d'):
                    flash('结束日期不能小于开始日期', 'error')
                    return redirect(url_for('task'))
                if newenddate and value > newenddate.strftime('%Y-%m-%d'):
                    flash('结束日期不能大于延期日期', 'error')
                    return redirect(url_for('task'))
            elif field == 'newenddate':
                if not startdate or not enddate:
                    flash('请先设置开始日期和结束日期', 'error')
                    return redirect(url_for('task'))
                if value < startdate.strftime('%Y-%m-%d'):
                    flash('延期日期不能小于开始日期', 'error')
                    return redirect(url_for('task'))
                if value < enddate.strftime('%Y-%m-%d'):
                    flash('延期日期不能小于结束日期', 'error')
                    return redirect(url_for('task'))
            
            sql = f'UPDATE UnfinishedTask SET {field} = %s WHERE INCIDENT = %s AND RTRIM(stepid) = %s'
            execute_sql(sql, (value, incident, stepid))
            flash('日期已更新', 'success')
    
    sql = '''
        SELECT PROCESSNAME, INCIDENT, stepid, STEPLABEL, ASSIGNEDTOUSER, status, startdate, enddate, newenddate
        FROM UnfinishedTask 
        WHERE RTRIM(USERID_AFTER_SLASH) = %s
        ORDER BY INCIDENT, stepid
    '''
    tasks = query_all(sql, (userid,))
    
    for task in tasks:
        task['USERID'] = extract_userid(task['ASSIGNEDTOUSER'])
    
    return render_template('task.html', tasks=tasks, userid=userid, username=session.get('username', userid))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)