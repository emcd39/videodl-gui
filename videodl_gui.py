# -*- coding: utf-8 -*-
"""
VideoDL GUI 应用程序
videodl 视频下载器的现代化图形界面
"""

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QTextEdit, QProgressBar, QComboBox, QFileDialog,
                             QMessageBox, QGroupBox, QGridLayout, QFrame,
                             QScrollArea, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
import threading
from videodl.videodl import VideoClient


class ParseThread(QThread):
    """解析视频链接的线程"""
    parse_finished = pyqtSignal(list)
    parse_error = pyqtSignal(str)
    
    def __init__(self, video_client, url):
        super().__init__()
        self.video_client = video_client
        self.url = url
        
    def run(self):
        try:
            video_infos = self.video_client.parsefromurl(url=self.url)
            self.parse_finished.emit(video_infos)
        except Exception as e:
            self.parse_error.emit(str(e))


class VideoInfoWidget(QWidget):
    """显示单个视频信息的组件"""
    def __init__(self, video_info, parent=None):
        super().__init__(parent)
        self.video_info = video_info
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 视频标题
        title = self.video_info.get('title', '未知标题')
        title_label = QLabel(f"📹 {title}")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # 视频详情
        details_layout = QGridLayout()
        
        # 来源
        source = self.video_info.get('source', '未知来源')
        details_layout.addWidget(QLabel("来源:"), 0, 0)
        details_layout.addWidget(QLabel(source), 0, 1)
        
        # 从 raw_data 中提取详细信息
        raw_data = self.video_info.get('raw_data', {})
        
        # 时长 - 从 raw_data 中提取
        duration = '未知'
        try:
            duration_sec = None
            if isinstance(raw_data, dict):
                if 'data' in raw_data and 'duration' in raw_data['data']:
                    duration_sec = raw_data['data']['duration']
                elif 'x/web-interface/view' in raw_data and 'data' in raw_data['x/web-interface/view']:
                    duration_sec = raw_data['x/web-interface/view']['data'].get('duration')
            
            if duration_sec is None:
                duration_sec = self.video_info.get('duration')
            
            if duration_sec and duration_sec != 'Unknown' and duration_sec != 'unknown' and duration_sec != 0:
                if isinstance(duration_sec, str):
                    if duration_sec.isdigit():
                        duration_sec = int(duration_sec)
                    else:
                        duration = duration_sec
                
                if isinstance(duration_sec, (int, float)):
                    seconds = int(duration_sec)
                    hours = seconds // 3600
                    minutes = (seconds % 3600) // 60
                    secs = seconds % 60
                    if hours > 0:
                        duration = f"{hours:02d}:{minutes:02d}:{secs:02d}"
                    else:
                        duration = f"{minutes:02d}:{secs:02d}"
        except Exception as e:
            pass
        details_layout.addWidget(QLabel("时长:"), 1, 0)
        details_layout.addWidget(QLabel(duration), 1, 1)
        
        # 大小 - 从 raw_data 中提取
        size = '未知'
        try:
            size_bytes = None
            if isinstance(raw_data, dict) and 'data' in raw_data:
                if 'durl' in raw_data['data'] and isinstance(raw_data['data']['durl'], list):
                    for durl in raw_data['data']['durl']:
                        if 'size' in durl:
                            size_bytes = durl['size']
                            break
            
            if size_bytes is None:
                size_bytes = self.video_info.get('size')
            
            if size_bytes and size_bytes != 'Unknown' and size_bytes != 'unknown' and size_bytes != 0:
                if isinstance(size_bytes, str):
                    if size_bytes.replace('.', '', 1).isdigit():
                        size_bytes = float(size_bytes)
                    else:
                        size = size_bytes
                
                if isinstance(size_bytes, (int, float)):
                    size_bytes = float(size_bytes)
                    for unit in ['B', 'KB', 'MB', 'GB']:
                        if size_bytes < 1024.0:
                            size = f"{size_bytes:.2f} {unit}"
                            break
                        size_bytes /= 1024.0
                    else:
                        size = f"{size_bytes:.2f} TB"
        except Exception as e:
            pass
        details_layout.addWidget(QLabel("大小:"), 2, 0)
        details_layout.addWidget(QLabel(size), 2, 1)
        
        # 清晰度 - 从 raw_data 中提取
        quality = ''
        try:
            if isinstance(raw_data, dict) and 'data' in raw_data:
                quality_id = raw_data['data'].get('quality')
                if 'accept_description' in raw_data['data'] and isinstance(raw_data['data']['accept_description'], list):
                    quality = raw_data['data']['accept_description'][0]
                elif quality_id:
                    quality_map = {80: '1080P', 64: '720P', 32: '480P', 16: '360P'}
                    quality = quality_map.get(quality_id, str(quality_id))
            
            if not quality:
                quality = self.video_info.get('quality', '')
        except Exception as e:
            pass
        
        if quality and quality != 'Unknown' and quality != 'unknown':
            details_layout.addWidget(QLabel("清晰度:"), 3, 0)
            details_layout.addWidget(QLabel(quality), 3, 1)
        
        # 格式 - 从 raw_data 中提取
        format_ = ''
        try:
            if isinstance(raw_data, dict) and 'data' in raw_data:
                format_ = raw_data['data'].get('format', '')
            
            if not format_:
                format_ = self.video_info.get('format', '')
                if not format_:
                    ext = self.video_info.get('ext', '')
                    if ext:
                        format_ = ext
        except Exception as e:
            pass
        
        if format_ and format_ != 'Unknown' and format_ != 'unknown':
            details_layout.addWidget(QLabel("格式:"), 4, 0)
            details_layout.addWidget(QLabel(format_), 4, 1)
        
        layout.addLayout(details_layout)
        
        # 下载链接
        download_url = self.video_info.get('download_url', '')
        if download_url and download_url != 'NULL':
            url_label = QLabel("🔗 可下载")
            url_label.setStyleSheet("color: green;")
            layout.addWidget(url_label)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        self.setLayout(layout)


class VideoDLGUI(QMainWindow):
    """VideoDL 主窗口"""
    
    def __init__(self):
        super().__init__()
        self.video_client = None
        self.current_video_infos = []
        self.output_dir = os.path.join(os.getcwd(), 'videodl_outputs')
        self.setup_ui()
        self.setup_style()
        self.init_video_client()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("VideoDL - 视频下载器")
        self.setMinimumSize(900, 700)
        
        # 主部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("🎬 VideoDL - 视频下载器")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # URL 输入区域
        url_group = QGroupBox("📎 视频链接")
        url_layout = QHBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("请粘贴视频链接 (例如：https://www.bilibili.com/video/...)")
        self.url_input.setMinimumHeight(40)
        url_layout.addWidget(self.url_input)
        
        self.parse_button = QPushButton("🔍 解析链接")
        self.parse_button.setMinimumHeight(40)
        self.parse_button.setMinimumWidth(120)
        self.parse_button.clicked.connect(self.parse_url)
        url_layout.addWidget(self.parse_button)
        
        url_group.setLayout(url_layout)
        main_layout.addWidget(url_group)
        
        # 输出目录区域
        dir_group = QGroupBox("📁 保存目录")
        dir_layout = QHBoxLayout()
        
        self.dir_input = QLineEdit()
        self.dir_input.setText(self.output_dir)
        self.dir_input.setPlaceholderText("选择保存目录")
        dir_layout.addWidget(self.dir_input)
        
        self.browse_button = QPushButton("📂 浏览")
        self.browse_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.browse_button)
        
        dir_group.setLayout(dir_layout)
        main_layout.addWidget(dir_group)
        
        # 状态和进度区域
        status_group = QGroupBox("📊 状态与进度")
        status_layout = QVBoxLayout()
        
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(150)
        self.status_text.setReadOnly(True)
        status_layout.addWidget(self.status_text)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)
        
        # 视频信息区域
        video_group = QGroupBox("📋 解析结果")
        video_layout = QVBoxLayout()
        
        self.video_list = QListWidget()
        self.video_list.setAlternatingRowColors(True)
        video_layout.addWidget(self.video_list)
        
        video_group.setLayout(video_layout)
        main_layout.addWidget(video_group)
        
        # 下载按钮
        self.download_button = QPushButton("⬇️ 开始下载")
        self.download_button.setMinimumHeight(50)
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.download_videos)
        main_layout.addWidget(self.download_button)
        
        # 初始化视频客户端
        self.log_message("VideoDL 初始化成功！")
        self.log_message("支持的平台：哔哩哔哩、抖音、快手、YouTube、小红书等...")
        
    def setup_style(self):
        """设置应用程序样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QPushButton#parse_button {
                background-color: #2196F3;
            }
            QPushButton#parse_button:hover {
                background-color: #1976D2;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            QTextEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
            QListWidget {
                border: 2px solid #ddd;
                border-radius: 5px;
            }
            QListWidget::item:alternate {
                background-color: #f0f0f0;
            }
        """)
        
    def init_video_client(self):
        """初始化视频客户端"""
        try:
            self.video_client = VideoClient()
            self.log_message("✓ 视频客户端初始化成功")
        except Exception as e:
            self.log_message(f"✗ 初始化视频客户端失败: {e}")
            QMessageBox.critical(self, "错误", f"初始化视频客户端失败: {e}")
            
    def log_message(self, message):
        """在状态文本区域记录消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.append(f"[{timestamp}] {message}")
        
    def browse_directory(self):
        """打开目录浏览器对话框"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择保存目录",
            self.output_dir
        )
        if directory:
            self.output_dir = directory
            self.dir_input.setText(directory)
            self.log_message(f"保存目录已设置为: {directory}")
            
    def parse_url(self):
        """解析输入的URL"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "警告", "请输入视频链接")
            return
        
        # 预处理微博短链接
        original_url = url
        if 't.cn/' in url:
            self.log_message(f"检测到微博短链接，尝试获取真实 URL...")
            try:
                import requests
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                }
                resp = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
                if resp.status_code == 200:
                    # 检查重定向历史，找到视频页面 URL
                    # 短链接会重定向到登录页面，但历史中包含视频页面 URL
                    for history in resp.history:
                        redirect_url = history.url
                        # 查找包含 /tv/show/ 的 URL
                        if '/tv/show/' in redirect_url:
                            url = redirect_url
                            self.log_message(f"✓ 短链接已重定向到: {url}")
                            self.url_input.setText(url)  # 更新输入框显示
                            break
                    # 如果没有找到视频页面 URL，使用最后一个重定向
                    if url == original_url and resp.history:
                        url = resp.history[-1].url
                        self.log_message(f"✓ 短链接已重定向到: {url}")
                        self.url_input.setText(url)  # 更新输入框显示
            except Exception as err:
                self.log_message(f"✗ 短链接重定向失败: {str(err)}")
                self.log_message("将尝试使用原链接解析...")
        
        self.log_message(f"正在解析: {url}")
        self.parse_button.setEnabled(False)
        self.download_button.setEnabled(False)
        self.video_list.clear()
        self.current_video_infos = []
        
        # 启动解析线程
        self.parse_thread = ParseThread(self.video_client, url)
        self.parse_thread.parse_finished.connect(self.on_parse_finished)
        self.parse_thread.parse_error.connect(self.on_parse_error)
        self.parse_thread.start()
        
    def on_parse_finished(self, video_infos):
        """处理解析完成的视频信息"""
        self.parse_button.setEnabled(True)
        self.current_video_infos = video_infos
        
        if not video_infos:
            self.log_message("未找到视频信息")
            QMessageBox.information(self, "提示", "未找到该链接的视频信息")
            return
            
        self.log_message(f"✓ 成功解析 {len(video_infos)} 个视频")
        
        # 显示视频信息
        for i, video_info in enumerate(video_infos):
            item = QListWidgetItem()
            widget = VideoInfoWidget(video_info)
            item.setSizeHint(widget.sizeHint())
            self.video_list.addItem(item)
            self.video_list.setItemWidget(item, widget)
            
        self.download_button.setEnabled(True)
        self.log_message("点击「开始下载」按钮下载视频")
        
    def on_parse_error(self, error_message):
        """处理解析错误"""
        self.parse_button.setEnabled(True)
        self.log_message(f"✗ 解析错误: {error_message}")
        QMessageBox.critical(self, "错误", f"解析链接失败: {error_message}")
        
    def download_videos(self):
        """下载解析的视频 - 使用 Python 模块直接调用"""
        if not self.current_video_infos:
            return
        
        # 确保输出目录与界面一致
        self.output_dir = self.dir_input.text().strip()
        if not self.output_dir:
            self.output_dir = os.path.join(os.getcwd(), 'videodl_outputs')
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 获取视频 URL
        video_url = self.url_input.text().strip()
        if not video_url:
            QMessageBox.warning(self, "警告", "请先解析视频链接")
            return
        
        self.log_message(f"正在下载视频...")
        self.log_message(f"下载目录: {self.output_dir}")
        
        # 使用 Python 模块直接调用下载功能
        try:
            # 为每个视频信息创建下载线程
            for i, video_info in enumerate(self.current_video_infos):
                self.log_message(f"开始下载第 {i+1} 个视频: {video_info.get('title', '未知标题')}")
                
                # 直接调用下载方法
                self.video_client.download(video_infos=[video_info], outputdir=self.output_dir)
                
                self.log_message(f"✓ 第 {i+1} 个视频下载完成")
            
            self.log_message("✓ 所有视频下载完成！")
            
            # 显示提示信息
            QMessageBox.information(
                self,
                "下载完成",
                f"所有视频已成功下载\n\n"
                f"保存目录: {self.output_dir}"
            )
            
        except Exception as e:
            self.log_message(f"✗ 下载失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"下载视频失败: {str(e)}")


def main():
    """主入口函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 设置应用程序全局字体
    font = QFont()
    font.setPointSize(10)
    app.setFont(font)
    
    window = VideoDLGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
