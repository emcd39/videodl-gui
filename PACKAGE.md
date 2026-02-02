# videodl 打包文档

本文档详细说明 videodl 项目的打包配置和打包命令。

## 目录

- [项目结构](#项目结构)
- [打包文件说明](#打包文件说明)
- [打包命令](#打包命令)
- [打包产物](#打包产物)
- [分发说明](#分发说明)
- [常见问题](#常见问题)

---

## 项目结构

```
videodl-master/
├── build_exe.spec           # videodl.exe 打包配置（核心下载程序）
├── build_gui_exe.spec       # videodl_gui.exe 打包配置（GUI界面）
├── main.py                  # videodl 入口文件
├── videodl_gui.py           # tkinter GUI 界面
├── videodl/                 # 核心模块目录
│   ├── videodl.py          # VideoClient 核心类
│   └── modules/            # 各平台下载器模块
├── build/                   # videodl 构建临时目录
├── build_gui/              # GUI 构建临时目录
├── dist/                   # videodl.exe 输出目录
└── dist_gui/               # videodl_gui.exe 输出目录
```

---

## 打包文件说明

### 1. build_exe.spec

用于打包 **videodl.exe**（核心命令行下载程序）

**关键配置项：**

```python
# 入口文件
['main.py']

# 数据文件
datas += collect_data_files('videodl')        # videodl 模块数据
datas += collect_data_files('playwright')     # Playwright 驱动
datas += collect_data_files('curl_cffi')      # curl_cffi 数据
# rich Unicode 数据文件（手动添加）

# 隐藏导入
hiddenimports += collect_submodules('videodl')
hiddenimports += ['click', 'rich', 'prettytable', ...]

# 输出配置
name='videodl'           # 输出文件名
console=True             # 显示控制台
upx=True                 # 启用 UPX 压缩
```

**特点：**
- 包含所有视频下载器模块
- 支持 40+ 视频平台
- 单文件 exe，包含所有依赖
- 显示控制台输出

### 2. build_gui_exe.spec

用于打包 **videodl_gui.exe**（GUI 图形界面）

**关键配置项：**

```python
# 入口文件
['videodl_gui.py']

# 隐藏导入
hiddenimports=['requests', 'urllib3']

# 排除大型库
excludes=['numpy', 'pandas', 'matplotlib']

# 输出配置
name='videodl_gui'
console=False            # 不显示控制台（GUI程序）
upx=True
```

**特点：**
- 轻量级 GUI 界面
- 需要配合 videodl.exe 使用
- macOS 风格设计
- 不显示控制台窗口

---

## 打包命令

### 前置要求

```bash
# 安装 PyInstaller
pip install pyinstaller

# 安装项目依赖
pip install -r requirements.txt
```

### 打包 videodl.exe（核心程序）

```bash
# 基础打包命令
pyinstaller build_exe.spec

# 完整命令（指定路径）
pyinstaller build_exe.spec --workpath=./build --distpath=./dist

# 清理后重新打包
pyinstaller --clean build_exe.spec --workpath=./build --distpath=./dist -y
```

**打包时间：** 约 2-5 分钟

### 打包 videodl_gui.exe（GUI界面）

```bash
# 基础打包命令
pyinstaller build_gui_exe.spec

# 完整命令（指定路径）
pyinstaller build_gui_exe.spec --workpath=./build_gui --distpath=./dist_gui

# 清理后重新打包
pyinstaller --clean build_gui_exe.spec --workpath=./build_gui --distpath=./dist_gui -y
```

**打包时间：** 约 1-2 分钟

### 一键打包脚本

创建 `build_all.bat`（Windows）或 `build_all.sh`（Linux/Mac）：

**Windows (build_all.bat):**
```batch
@echo off
echo ========================================
echo   videodl 打包脚本
echo ========================================

echo.
echo [1/2] 打包 videodl.exe...
pyinstaller --clean build_exe.spec --workpath=./build --distpath=./dist -y
if %errorlevel% neq 0 (
    echo videodl.exe 打包失败！
    pause
    exit /b 1
)

echo.
echo [2/2] 打包 videodl_gui.exe...
pyinstaller --clean build_gui_exe.spec --workpath=./build_gui --distpath=./dist_gui -y
if %errorlevel% neq 0 (
    echo videodl_gui.exe 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo   videodl.exe    → dist\videodl.exe
echo   videodl_gui.exe → dist_gui\videodl_gui\videodl_gui.exe
echo ========================================
pause
```

**Linux/Mac (build_all.sh):**
```bash
#!/bin/bash
echo "========================================"
echo "  videodl 打包脚本"
echo "========================================"

echo ""
echo "[1/2] 打包 videodl.exe..."
pyinstaller --clean build_exe.spec --workpath=./build --distpath=./dist -y
if [ $? -ne 0 ]; then
    echo "videodl.exe 打包失败！"
    exit 1
fi

echo ""
echo "[2/2] 打包 videodl_gui.exe..."
pyinstaller --clean build_gui_exe.spec --workpath=./build_gui --distpath=./dist_gui -y
if [ $? -ne 0 ]; then
    echo "videodl_gui.exe 打包失败！"
    exit 1
fi

echo ""
echo "========================================"
echo "  打包完成！"
echo "========================================"
echo "  videodl.exe    → dist/videodl"
echo "  videodl_gui.exe → dist_gui/videodl_gui/videodl_gui"
echo "========================================"
```

---

## 打包产物

### videodl.exe 输出

```
dist/
└── videodl.exe          # 约 200-300MB（单文件）
```

**功能：**
- 支持 40+ 视频平台下载
- 命令行交互模式
- 直接下载模式：`videodl.exe -i <URL>`
- 配置文件模式：`videodl.exe -i <URL> -c <config.json>`

### videodl_gui.exe 输出

```
dist_gui/
└── videodl_gui/
    ├── videodl_gui.exe  # GUI 程序（约 30-50MB）
    └── _internal/        # 依赖库目录
```

**功能：**
- 图形化界面
- 视频链接输入
- 保存目录选择
- 下载日志显示
- 短链接自动解析

---

## 分发说明

### 方式一：分开分发（当前方案）

**需要分发：**
- `dist/videodl.exe`（核心下载程序）
- `dist_gui/videodl_gui/` 整个目录（GUI界面）

**使用方式：**
```bash
# 运行 GUI
dist_gui/videodl_gui/videodl_gui.exe

# 或直接运行命令行
dist/videodl.exe -i "https://www.bilibili.com/video/BV1xx"
```

**打包成 ZIP：**
```bash
# 创建分发包
videodl-release/
├── videodl.exe
└── videodl_gui/
    ├── videodl_gui.exe
    └── _internal/
```

### 方式二：集成打包（推荐）

修改 GUI 直接调用 videodl 模块，打包成单个 exe。

**优点：**
- 只需分发一个 exe 文件
- 用户体验更好

**缺点：**
- 文件体积较大（约 300-400MB）
- 首次启动较慢

---

## 常见问题

### 1. 打包失败：ModuleNotFoundError

**原因：** 缺少隐藏导入

**解决：** 在 `build_exe.spec` 的 `hiddenimports` 中添加对应模块

```python
hiddenimports += ['缺失的模块名']
```

### 2. 打包后运行失败：找不到数据文件

**原因：** 数据文件未正确打包

**解决：** 在 `build_exe.spec` 的 `datas` 中添加

```python
datas += collect_data_files('模块名')
```

### 3. 中文乱码

**原因：** Windows 控制台编码问题

**解决：** 在命令前添加 `chcp 65001`（UTF-8）

```batch
chcp 65001
dist\videodl.exe
```

### 4. UPX 压缩失败

**原因：** 某些 DLL 文件不支持 UPX 压缩

**解决：** 在 spec 文件中添加到 `upx_exclude`

```python
upx_exclude=['python3.dll', 'vcruntime140.dll']
```

或禁用 UPX：

```python
upx=False
```

### 5. 打包体积过大

**优化方案：**

1. **排除不需要的模块：**
```python
excludes=['numpy', 'pandas', 'matplotlib', 'scipy']
```

2. **使用虚拟环境打包：**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pyinstaller build_exe.spec
```

3. **启用 UPX 压缩：**
```python
upx=True
```

### 6. GUI 找不到 videodl.exe

**原因：** 路径配置不正确

**解决：** 确保两个文件在同一目录，或修改 `videodl_gui.py` 中的路径：

```python
# 开发环境
self.exe_path = os.path.join(os.path.dirname(__file__), 'dist', 'videodl.exe')

# 打包后环境
if getattr(sys, 'frozen', False):
    self.exe_path = os.path.join(os.path.dirname(sys.executable), 'videodl.exe')
```

---

## 测试验证

### 测试 videodl.exe

```bash
# 测试 B站视频
dist\videodl.exe -i "https://www.bilibili.com/video/BV1Cx6wByEFw"

# 测试微博短链接
dist\videodl.exe -i "http://t.cn/AXqnEjzp"
```

### 测试 videodl_gui.exe

```bash
# 运行 GUI
dist_gui\videodl_gui\videodl_gui.exe

# 测试流程：
# 1. 输入视频链接
# 2. 选择保存目录
# 3. 点击"开始下载"
# 4. 查看日志输出
```

---

## 版本发布

### 发布前检查清单

- [ ] 确认版本号更新
- [ ] 测试主要平台视频下载（B站、抖音、YouTube等）
- [ ] 测试短链接解析
- [ ] 测试 GUI 界面功能
- [ ] 检查打包体积
- [ ] 准备发布说明

### 版本命名

```
videodl-vX.X.X-windows/
├── videodl.exe
├── videodl_gui/
│   ├── videodl_gui.exe
│   └── _internal/
├── README.txt
└── 使用说明.txt
```

---

## 技术支持

- **项目地址：** https://github.com/CharlesPikachu/videodl
- **问题反馈：** GitHub Issues
- **PyInstaller 文档：** https://pyinstaller.org/en/stable/
