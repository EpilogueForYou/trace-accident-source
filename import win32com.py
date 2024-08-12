import win32com.client
import tkinter as tk
from tkinter import filedialog

# 创建Tkinter根窗口（隐藏）
root = tk.Tk()
root.withdraw()

# 弹出文件选择对话框
network_file_path = filedialog.askopenfilename(title="选择VISSIM网络文件", filetypes=[("VISSIM文件", "*.inp")])

# 创建VISSIM对象并加载网络
vissim = win32com.client.Dispatch("VISSIM.Vissim")
vissim.LoadNet(network_file_path)

# 获取Simulation对象
simulation = vissim.Simulation
simulation.Period = 5200  # 设置仿真时长（例如3600秒）
simulation.Resolution = 1  # 设置仿真分辨率为1步/秒

# 运行仿真，并在特定时间段内设置信号灯状态
for i in range(int(simulation.Period * simulation.Resolution)):
    simulation.RunSingleStep()
    if 3285 <= simulation.SimulationSecond <= 4300:
        sg.AttValue("STATE", 1)  # 设置为红灯
    else:
        sg.AttValue("STATE", 5)  # 设置为关闭
