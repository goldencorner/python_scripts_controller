# Overview
- 有些python脚本需要一直挂在后台使用，而每个脚本会留下一个控制台，非常不美观
- vbs可以隐藏控制台，但是会让你找不到这个脚本的实例（无法让其停止）

本工具解决上述两个问题，让你的python脚本更优雅

# Quick Start
1. 进入`python_scripts_controller.py`修改成你的参数
```python
script_dir = '../'
script_name_list = ["fill_password.py", 'xiaomi_mijia_mqttClient.py', 'jobs.py']
```
2. 运行`python_scripts_controller.vbs`（建议开机启动）
