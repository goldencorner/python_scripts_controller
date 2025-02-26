import asyncio
import subprocess
import sys
import time

import psutil
import os

import logging
from datetime import datetime
import csv

# CSV 文件路径
csv_file = 'app_logs.csv'

# 写入 CSV 文件的列名
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Level', 'ProcessID', 'Message'])


def write_to_csv(level, message):
    """将日志写入 CSV 文件"""
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), level, os.getpid(), message])


write_to_csv('INFO', 'started')


# 查找并关闭指定名称的 Python 程序
def find_and_kill_python_processes(script_name):
    print('查找', script_name)
    current_pid = os.getpid()
    python_processes = []

    # 遍历系统中的所有进程
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python':
            if proc.info['pid'] != current_pid:
                cmdline = proc.info['cmdline']
                if len(cmdline) > 1 and cmdline[1].endswith(script_name):
                    python_processes.append(proc.info['pid'])
    # 关闭找到的 Python 进程
    for pid in python_processes:
        try:
            process = psutil.Process(pid)
            process.terminate()
            print(f"关闭进程：{pid}")
        except psutil.NoSuchProcess:
            pass


# 要关闭的脚本名称
script_dir = '../'
script_name_list = ["fill_password.py", 'xiaomi_mijia_mqttClient.py', 'jobs.py']

#首先关闭上一个脚本控制台
find_and_kill_python_processes(os.path.basename(__file__))

for script_name in script_name_list:
    # 运行查找并关闭指定名称的 Python 程序的函数
    find_and_kill_python_processes(script_name)
    p = subprocess.Popen([sys.executable, script_name],cwd=script_dir)

#实测发现，主进程结束后，子进程虽然没有退出但是无法响应，因此此处阻止主进程退出
print("now waiting")
while True:
    time.sleep(30)
    write_to_csv('INFO', f'working...')

write_to_csv('INFO', f'exit')
