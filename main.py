"""
videodl - 视频下载工具主入口
VideoDL - Video Downloader Main Entry Point
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from videodl.videodl import VideoClientCMD

if __name__ == '__main__':
    VideoClientCMD()
