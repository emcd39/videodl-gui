# 自定义文件说明

此目录包含 videodl 项目的自定义修改文件，用于 GitHub Actions 自动构建。

## 文件列表

### 1. main.py
videodl 的入口文件，用于正确初始化模块路径。

### 2. videodl_gui.py
tkinter GUI 界面程序，提供友好的图形界面。

### 3. build_exe.spec
PyInstaller 配置文件，用于打包 videodl.exe（核心下载程序）。

### 4. build_gui_exe.spec
PyInstaller 配置文件，用于打包 videodl_gui.exe（GUI界面）。

## 准备步骤

在推送到 GitHub 之前，需要将以下文件复制到此目录：

```bash
# 从项目根目录复制文件到 custom_files 目录
cp main.py custom_files/
cp videodl_gui.py custom_files/
cp build_exe.spec custom_files/
cp build_gui_exe.spec custom_files/
```

## 注意事项

⚠️ **重要**: build_exe.spec 中包含用户特定的路径，需要在构建前动态修改。

修改 build_exe.spec 中的这一行：
```python
rich_unicode_path = 'C:/Users/EMCD/AppData/Local/Programs/Python/Python312/Lib/site-packages/rich/_unicode_data'
```

改为动态路径：
```python
import site
rich_unicode_path = os.path.join(site.getsitepackages()[0], 'rich/_unicode_data')
```

## GitHub Actions 工作流程

1. 克隆上游仓库 (CharlesPikachu/videodl)
2. 复制 custom_files 中的文件到仓库根目录
3. 安装依赖
4. 构建 videodl.exe
5. 构建 videodl_gui.exe
6. 打包并上传构建产物

## 输出文件

- `videodl.exe` - 核心命令行下载程序
- `videodl_gui.zip` - GUI 界面程序（包含 videodl.exe）
