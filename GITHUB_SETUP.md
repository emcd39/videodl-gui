# GitHub Actions 自动构建指南

本文档说明如何使用 GitHub Actions 自动构建 videodl 的 Windows EXE 文件。

## 前置准备

### 1. 创建 GitHub 仓库

在你的 GitHub 账号下创建一个新仓库（不需要 fork上游仓库）。

示例：`https://github.com/yourusername/videodl-build`

### 2. 准备本地文件

运行准备脚本：

**Windows:**
```bash
prepare_custom_files.bat
```

**Linux/Mac:**
```bash
./prepare_custom_files.sh
```

这会将以下文件复制到 `custom_files/` 目录：
- `main.py` - videodl 入口文件
- `videodl_gui.py` - GUI 界面程序
- `build_exe.spec` - videodl.exe 打包配置
- `build_gui_exe.spec` - videodl_gui.exe 打包配置

### 3. 推送到 GitHub

```bash
# 初始化仓库（如果还没有）
git init

# 添加 .github 工作流和 custom_files
git add .github/workflows/build.yml
git add custom_files/

# 提交
git commit -m "Add GitHub Actions workflow"

# 添加远程仓库
git remote add origin https://github.com/yourusername/videodl-build.git

# 推送
git push -u origin main
```

## 工作流程说明

### GitHub Actions 做什么？

1. **克隆上游仓库**
   - 从 `CharlesPikachu/videodl` 获取最新代码

2. **应用自定义修改**
   - 复制 `custom_files/` 中的文件到仓库根目录
   - 覆盖默认文件

3. **安装依赖**
   - Python 3.12
   - PyInstaller
   - requirements.txt 中的所有依赖

4. **构建 EXE**
   - 构建 `videodl.exe`（核心程序）
   - 构建 `videodl_gui.exe`（GUI 界面）

5. **打包发布**
   - 复制 `videodl.exe` 到 GUI 目录
   - 打包成 `videodl_gui.zip`
   - 单独的 `videodl.exe`

6. **上传构建产物**
   - 作为 GitHub Actions artifacts
   - 如果是 tag，自动创建 GitHub Release

## 触发构建

### 自动触发

- 推送到 `main` 或 `master` 分支
- 创建 Pull Request
- 修改 `.github/` 或 `custom_files/` 目录

### 手动触发

1. 进入 GitHub 仓库页面
2. 点击 "Actions" 标签
3. 选择 "Build videodl Windows EXE"
4. 点击 "Run workflow"
5. 选择分支，点击 "Run workflow"

### 创建 Release 构建

```bash
# 创建并推送 tag
git tag v1.0.0
git push origin v1.0.0
```

这将触发构建并自动创建 GitHub Release。

## 下载构建产物

### 从 Actions 下载

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择最近的构建任务
4. 滚动到底部 "Artifacts" 区域
5. 下载 `videodl-windows` ZIP 文件

### 从 Releases 下载

1. 进入 GitHub 仓库
2. 点击 "Releases" 标签
3. 选择对应的版本
4. 下载附件文件

## 文件说明

### 输出文件

构建成功后会得到：

```
videodl-windows.zip
├── videodl.exe         # 核心命令行程序（约 200-300MB）
└── videodl_gui.zip     # GUI 界面程序（解压后约 100MB）
    ├── videodl_gui.exe
    ├── videodl.exe
    └── _internal/
```

### 使用方法

#### 方式一：直接使用 GUI

1. 解压 `videodl_gui.zip`
2. 运行 `videodl_gui.exe`
3. 输入视频链接，选择保存目录
4. 点击"开始下载"

#### 方式二：命令行

```bash
# 下载视频
videodl.exe -i "视频URL"

# 指定保存目录
videodl.exe -i "视频URL" -c '{"work_dir": "保存路径"}'
```

## 自定义配置

### 修改上游仓库地址

编辑 `.github/workflows/build.yml`：

```yaml
- name: Checkout upstream repository
  uses: actions/checkout@v4
  with:
    repository: CharlesPikachu/videodl  # 修改这里
```

### 修改 Python 版本

```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.12'  # 修改这里
```

### 修改构建配置

直接修改 `custom_files/` 中的 spec 文件，然后提交推送。

## 常见问题

### Q: 构建失败怎么办？

A: 查看 Actions 日志：
1. 进入 "Actions" 标签
2. 点击失败的构建任务
3. 查看详细日志输出
4. 根据错误信息修改配置

### Q: 如何更新上游代码？

A: 无需操作！每次构建都会自动获取上游最新代码。

### Q: 构建需要多长时间？

A: 通常 10-15 分钟：
- 安装依赖：3-5 分钟
- 构建 videodl.exe：3-5 分钟
- 构建 videodl_gui.exe：1-2 分钟
- 打包上传：1-2 分钟

### Q: 可以同时构建多个版本吗？

A: 可以！修改工作流添加矩阵构建：

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
```

## 项目结构

```
your-repo/
├── .github/
│   └── workflows/
│       └── build.yml           # GitHub Actions 工作流
├── custom_files/               # 自定义文件目录
│   ├── README.md
│   ├── main.py
│   ├── videodl_gui.py
│   ├── build_exe.spec
│   └── build_gui_exe.spec
├── prepare_custom_files.bat    # Windows 准备脚本
├── prepare_custom_files.sh     # Linux/Mac 准备脚本
└── GITHUB_SETUP.md             # 本文档
```

## 相关链接

- **上游仓库**: https://github.com/CharlesPikachu/videodl
- **PyInstaller 文档**: https://pyinstaller.org/
- **GitHub Actions 文档**: https://docs.github.com/en/actions

## 许可证

请遵守上游仓库的许可证协议。
