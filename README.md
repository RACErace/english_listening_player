# 介绍
本项目融合了机器学习

用于将英语听力自动分节

## 运行环境
win10、python3.16.9

(目前只在该环境经过测试，其他环境未经测试，可自行尝试)

## 安装
建议使用conda
```bash
conda create -n elp python=3.9.16 -y
```

激活虚拟环境
```bash
activate elp
```

首先安装基本依赖
```bash
pip install -r requirements.txt
```

安装ffmpeg(要将ffmpeg加入环境变量)

[github](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip)

[百度网盘](https://pan.baidu.com/s/1e8C_dWc_-sPzUxkrdL-OQQ?pwd=1024)
提取码：1024

## 运行程序
```bash
python player.py
```"# english_listening_player" 
