import os
import subprocess

# VISSIM安装目录（请根据实际安装路径修改）
vissim_path = r"E:/PTV Vision/VISSIM430/Exe/vissim.exe"

# 注册VISSIM COM服务器
subprocess.run([vissim_path, "-RegServer"], check=True)

print("VISSIM COM服务器注册成功")
