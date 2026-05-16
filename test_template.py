import sys
sys.path.insert(0, '/home/sa/app/bpmapp')

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('/home/sa/app/bpmapp/templates'))
try:
    template = env.get_template('work.html')
    print('Template syntax OK')
except Exception as e:
    print(f'Error: {e}')