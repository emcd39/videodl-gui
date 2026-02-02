"""
videodl GUI - 视频下载工具图形界面
VideoDL GUI - Video Downloader Graphical Interface
"""
import os
import sys
import subprocess
import threading
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import requests


class VideoDLGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("videodl 视频下载工具 v0.6.2")
        self.root.geometry("600x500")

        # exe 路径
        self.exe_path = os.path.join(os.path.dirname(__file__), 'dist', 'videodl.exe')
        if not os.path.exists(self.exe_path):
            self.exe_path = 'videodl.exe'

        # 配置文件路径（我的文档）
        self.config_file = os.path.join(os.path.expanduser('~'), 'Documents', 'videodl_config.json')

        # 加载配置
        self.load_config()

        self.setup_ui()

    def get_default_download_dir(self):
        """获取默认下载目录（桌面\videodl_outputs）"""
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        return os.path.join(desktop, 'videodl_outputs')

    def load_config(self):
        """加载配置文件"""
        self.last_download_dir = None
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.last_download_dir = config.get('last_download_dir')
            except:
                pass

    def save_config(self, download_dir):
        """保存配置文件"""
        try:
            config = {'last_download_dir': download_dir}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def setup_ui(self):
        """设置界面"""
        # 主容器
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="videodl 视频下载工具",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))

        # URL 输入区
        url_frame = tk.LabelFrame(main_frame, text="视频地址", padx=10, pady=10)
        url_frame.pack(fill=tk.X, pady=(0, 15))

        self.url_entry = tk.Entry(url_frame, font=('Arial', 10))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 5))

        tk.Button(
            url_frame,
            text="粘贴",
            command=self.paste_url,
            width=8
        ).pack(side=tk.LEFT)

        # 下载目录区
        dir_frame = tk.LabelFrame(main_frame, text="保存目录", padx=10, pady=10)
        dir_frame.pack(fill=tk.X, pady=(0, 15))

        # 使用上次下载目录或默认目录
        default_dir = self.last_download_dir if self.last_download_dir else self.get_default_download_dir()
        self.download_dir = tk.StringVar(value=default_dir)

        dir_entry = tk.Entry(dir_frame, textvariable=self.download_dir, font=('Arial', 10))
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 5))
        tk.Button(dir_frame, text="浏览", command=self.browse_directory, width=8).pack(side=tk.LEFT)

        # 操作按钮区
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))

        self.download_btn = tk.Button(
            button_frame,
            text="开始下载",
            command=self.start_download,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            height=2,
            cursor='hand2'
        )
        self.download_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.clear_btn = tk.Button(
            button_frame,
            text="清空日志",
            command=self.clear_log,
            font=('Arial', 10),
            height=2,
            cursor='hand2'
        )
        self.clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # 日志输出区
        log_frame = tk.LabelFrame(main_frame, text="下载日志", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 配置日志颜色标签
        self.log_text.tag_config('info', foreground='#3498db')
        self.log_text.tag_config('success', foreground='#27ae60')
        self.log_text.tag_config('error', foreground='#e74c3c')
        self.log_text.tag_config('warning', foreground='#f39c12')

        # 底部状态栏
        status_frame = tk.Frame(self.root, bg='#ecf0f1', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="就绪",
            font=('Arial', 9),
            bg='#ecf0f1',
            fg='#7f8c8d',
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

    def paste_url(self):
        """从剪贴板粘贴URL"""
        try:
            url = self.root.clipboard_get()
            if url:
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, url.strip())
                self.status_label.config(text="链接已粘贴", fg='#27ae60')
                self.root.after(3000, lambda: self.status_label.config(text="就绪", fg='#7f8c8d'))
            else:
                self.status_label.config(text="剪贴板为空", fg='#e74c3c')
        except tk.TclError:
            self.status_label.config(text="剪贴板为空", fg='#e74c3c')

    def resolve_short_url(self, url):
        """解析短链接，跟随302重定向获取长链接"""
        try:
            from urllib.parse import urlparse, parse_qs

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
            resolved_url = response.url

            # 特殊处理微博访客页面
            if 'passport.weibo.com/visitor' in resolved_url:
                parsed = urlparse(resolved_url)
                params = parse_qs(parsed.query)
                if 'url' in params:
                    return params['url'][0]

            if resolved_url != url:
                self.log(f"检测到短链接，已自动解析为: {resolved_url}", 'info')
            return resolved_url if resolved_url != url else url
        except Exception as e:
            self.log(f"短链接解析失败: {e}", 'warning')
            return url

    def browse_directory(self):
        """浏览目录"""
        directory = filedialog.askdirectory(initialdir=self.download_dir.get())
        if directory:
            self.download_dir.set(directory)

    def log(self, message, level='info'):
        """添加日志"""
        self.log_text.insert(tk.END, message + '\n', level)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)

    def start_download(self):
        """开始下载"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("提示", "请输入视频地址！")
            return

        download_dir = self.download_dir.get()

        # 保存下载目录到配置文件
        self.save_config(download_dir)

        # 禁用下载按钮
        self.download_btn.config(state=tk.DISABLED, text="下载中...")
        self.status_label.config(text="正在下载...", fg='#e67e22')

        # 在新线程中执行下载
        thread = threading.Thread(target=self.run_download, args=(url, download_dir))
        thread.daemon = True
        thread.start()

    def run_download(self, url, download_dir):
        """执行下载（在后台线程中）"""
        try:
            self.log("=" * 50, 'info')
            self.log(f"原始链接: {url}", 'info')

            # 解析短链接
            url = self.resolve_short_url(url)

            self.log(f"最终链接: {url}", 'info')
            self.log(f"保存目录: {download_dir}", 'info')
            self.log("=" * 50, 'info')

            # 构建命令
            cmd = [self.exe_path, '-i', url]

            self.log(f"开始下载...\n", 'info')

            # 执行下载（在指定目录下运行）
            process = subprocess.Popen(cmd, cwd=download_dir)
            return_code = process.wait()

            if return_code == 0:
                self.log("\n" + "=" * 50, 'success')
                self.log("下载完成！", 'success')
                self.log("=" * 50, 'success')
                self.status_label.config(text="下载完成", fg='#27ae60')
                messagebox.showinfo("完成", "视频下载完成！")
            else:
                self.log(f"\n下载失败，返回码: {return_code}", 'error')
                self.status_label.config(text="下载失败", fg='#e74c3c')

        except FileNotFoundError:
            self.log(f"错误: 找不到 videodl.exe", 'error')
            self.status_label.config(text="找不到程序", fg='#e74c3c')
            messagebox.showerror("错误", f"找不到 videodl.exe\n请确保文件在: {self.exe_path}")

        except Exception as e:
            self.log(f"\n错误: {str(e)}", 'error')
            self.status_label.config(text="发生错误", fg='#e74c3c')
            messagebox.showerror("错误", f"下载失败: {str(e)}")

        finally:
            # 恢复下载按钮
            self.download_btn.config(state=tk.NORMAL, text="开始下载")


def main():
    """主函数"""
    root = tk.Tk()
    app = VideoDLGUI(root)

    # 窗口居中
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == '__main__':
    main()
