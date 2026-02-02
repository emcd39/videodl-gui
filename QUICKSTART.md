# GitHub Actions 自动构建快速开始

## 一分钟快速设置

### 步骤 1：准备文件

运行准备脚本：

```bash
# Windows
prepare_custom_files.bat

# Linux/Mac
./prepare_custom_files.sh
```

### 步骤 2：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 创建新仓库（例如：`videodl-windows-build`）
3. 不要初始化 README

### 步骤 3：推送代码

```bash
git init
git add .github/workflows/build.yml
git add custom_files/
git add .gitignore
git commit -m "Add GitHub Actions workflow"

git remote add origin https://github.com/yourusername/videodl-windows-build.git
git branch -M main
git push -u origin main
```

### 步骤 4：获取构建产物

1. 等待 GitHub Actions 完成（约 15 分钟）
2. 进入仓库的 "Actions" 标签
3. 下载构建产物

## 文件说明

```
your-repo/
├── .github/
│   └── workflows/
│       └── build.yml              # 自动构建工作流
├── custom_files/                  # 自定义修改
│   ├── main.py
│   ├── videodl_gui.py
│   ├── build_exe.spec
│   └── build_gui_exe.spec
└── prepare_custom_files.bat       # 准备脚本
```

## 修改说明

### 1. main.py
```python
from videodl.videodl import VideoClientCMD
if __name__ == '__main__':
    VideoClientCMD()
```

### 2. videodl_gui.py
- 简洁的 tkinter GUI 界面
- 支持粘贴链接、选择目录
- 自动解析短链接
- 彩色日志输出

### 3. build_exe.spec
- 动态获取 rich Unicode 路径
- 包含所有 videodl 模块
- 单文件 exe 输出

### 4. build_gui_exe.spec
- 轻量级 GUI 打包
- 排除大型依赖库
- 调用 videodl.exe

## 工作流程

```
上游仓库 (CharlesPikachu/videodl)
    ↓ clone
GitHub Actions
    ↓ 复制 custom_files/
构建 videodl.exe
构建 videodl_gui.exe
    ↓ 打包
Artifacts / Release
```

## 常用命令

### 手动触发构建

GitHub 网页操作：
1. Actions → Build videodl Windows EXE
2. Run workflow → 选择分支 → Run

### 创建 Release 构建

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 更新上游代码

无需任何操作！每次构建都会自动获取上游最新代码。

如需固定上游版本，修改 `.github/workflows/build.yml`:

```yaml
- name: Checkout upstream repository
  uses: actions/checkout@v4
  with:
    repository: CharlesPikachu/videodl
    ref: v0.6.2  # 固定到特定版本
```

## 问题排查

### 构建失败

查看 Actions 日志，常见问题：

1. **依赖安装失败**
   - 检查 requirements.txt
   - 确认所有包可安装

2. **PyInstaller 打包失败**
   - 检查 spec 文件语法
   - 确认所有数据文件路径正确

3. **Rich Unicode 数据错误**
   - 已使用动态路径，应该不会出现

### 自定义配置

修改 `custom_files/` 中的文件后：

```bash
# 更新 custom_files
prepare_custom_files.bat

# 提交更改
git add custom_files/
git commit -m "Update build config"
git push
```

## 相关文档

- [完整设置指南](GITHUB_SETUP.md)
- [打包文档](PACKAGE.md)
- [上游仓库](https://github.com/CharlesPikachu/videodl)
