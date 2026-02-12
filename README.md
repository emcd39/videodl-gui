# videodl GUI - 视频下载工具

基于 [CharlesPikachu/videodl](https://github.com/CharlesPikachu/videodl) 的 Windows GUI 版本。

## 下载说明

### 📦 安装包（推荐）

下载 `videodl-setup.exe`，双击安装：
- 自动安装到 `%USERPROFILE%\AppData\Local\videodl`
- 自动创建桌面快捷方式 `videodl_gui`
- 支持卸载

### 📁 便携版

下载 `videodl_gui.zip`，解压后直接运行 `videodl_gui.exe`

## 功能特性

- ✅ 图形化界面，操作简单
- ✅ 支持多个视频平台
- ✅ 自动解析短链接
- ✅ 自定义下载目录
- ✅ 实时下载日志

## 系统要求

- Windows 10 或更高版本

## 开发构建

### 文件说明

| 文件 | 说明 |
|------|------|
| `main.py` | videodl 入口文件 |
| `videodl_gui.py` | tkinter GUI 界面 |
| `build_exe.spec` | PyInstaller 配置（核心程序） |
| `build_gui_exe.spec` | PyInstaller 配置（GUI） |
| `install.nsi` | NSIS 安装包脚本 |

### 本地构建

```bash
# 克隆上游仓库并复制源代码
git clone --depth=1 https://github.com/CharlesPikachu/videodl.git videodl-upstream
cp -r videodl-upstream/videodl .
cp videodl-upstream/requirements.txt .

# 安装依赖
pip install -r requirements.txt pyinstaller

# 构建 exe
pyinstaller --clean build_exe.spec --workpath=./build --distpath=./dist -y
pyinstaller --clean build_gui_exe.spec --workpath=./build_gui --distpath=./dist_gui -y

# 复制核心程序到 GUI 目录
cp dist/videodl.exe dist_gui/videodl_gui/

# 构建安装包（需要安装 NSIS）
makensis install.nsi
```

## 许可证

MIT License

---

上游项目: https://github.com/CharlesPikachu/videodl
