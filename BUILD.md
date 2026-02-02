# videodl 打包指南

本文档介绍如何将 videodl 项目打包成独立的 Windows 可执行文件（exe），方便没有安装 Python 的用户使用。

## 环境要求

- Python 3.10+
- PyInstaller 6.0+

### 安装依赖

```bash
# 安装项目依赖
pip install -r requirements.txt

# 安装 PyInstaller
pip install pyinstaller
```

## 打包步骤

### 1. 项目结构说明

```
videodl-master/
├── build_exe.spec      # PyInstaller 配置文件（已创建）
├── main.py             # 入口启动脚本（已创建）
├── videodl/            # 主程序目录
├── requirements.txt    # 项目依赖
└── dist/               # 构建输出目录（生成后）
```

### 2. 快速打包

在项目根目录执行：

```bash
pyinstaller --clean build_exe.spec --workpath=./build --distpath=./dist
```

### 3. 构建产物

打包完成后，可执行文件位于：

```
dist/videodl.exe
```

## 配置文件说明

### build_exe.spec

PyInstaller 的配置文件，定义了打包规则：

```python
# 关键配置项
- datas: 需要打包的数据文件
- hiddenimports: 隐藏导入的模块
- binaries: 二进制文件
- exe_name: 输出的 exe 文件名
```

### main.py

入口启动脚本，用于正确初始化模块路径：

```python
from videodl.videodl import VideoClientCMD

if __name__ == '__main__':
    VideoClientCMD()
```

## 常见问题

### 1. ModuleNotFoundError

如果遇到模块未找到错误，需要在 `build_exe.spec` 的 `hiddenimports` 中添加对应模块。

### 2. 缺少数据文件

某些库（如 rich、playwright）需要额外的数据文件，需要在 `datas` 中添加：

```python
datas += collect_data_files('模块名')
```

### 3. 中文乱码

Windows 命令行可能显示中文乱码，这是终端编码问题，不影响程序功能。

## 分发说明

打包后的 `videodl.exe` 可以独立运行，无需安装 Python。

### 可选依赖

某些功能需要额外工具：

- **FFmpeg** - 下载 HLS/m3u8 视频流
- **N_m3u8DL-RE** - 加密视频下载
- **Node.js** - YouTube/CCTV/腾讯视频支持
- **aria2c** - 加速下载

用户可选择安装这些工具以获得完整功能。

## 使用示例

```bash
# 交互模式
videodl.exe

# 下载 B 站视频
videodl.exe -i "https://www.bilibili.com/video/BV1xx" -a BilibiliVideoClient

# 使用通用解析器
videodl.exe -i "视频URL" -g -a VideoFKVideoClient
```

## 重新打包

如果修改了代码或依赖，重新打包步骤：

```bash
# 清理旧构建
pyinstaller --clean build_exe.spec --workpath=./build --distpath=./dist

# 或删除 build 和 dist 目录后重新打包
rmdir /s /q build dist
pyinstaller build_exe.spec
```

## 打包优化

### 减小文件大小

1. 使用 UPX 压缩（已默认启用）
2. 排除不需要的模块（在 spec 文件的 `excludes` 中添加）
3. 使用虚拟环境打包，只包含必要依赖

### 单文件模式

如需打包成单个大文件，修改 spec 文件：

```python
exe = EXE(
    ...
    onefile=True,  # 添加此行
    ...
)
```

## GUI 图形界面

项目附带了一个基于 tkinter 的图形界面，更方便用户使用。

### 运行 GUI

```bash
# 需要 Python 环境
python videodl_gui.py
```

### GUI 功能

- 简洁友好的中文界面
- 视频 URL 输入框
- 多种解析器选择（自动检测或手动指定）
- 保存目录设置
- 实时下载日志显示
- 一键下载按钮

### 打包 GUI 为 exe

如需将 GUI 也打包成 exe，创建以下 spec 文件：

```python
# gui_exe.spec
a = Analysis(
    ['videodl_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    ...
)
```

然后执行：

```bash
pyinstaller gui_exe.spec --workpath=./build_gui --distpath=./dist_gui
```

注意：GUI 程序需要调用 `videodl.exe`，因此分发时需要同时提供：
- `videodl_gui.exe`（GUI 界面）
- `videodl.exe`（核心下载程序）

## 技术支持

- 项目地址: https://github.com/CharlesPikachu/videodl
- 问题反馈: GitHub Issues
