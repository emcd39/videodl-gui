# videodl-gui 仓库上传指南

## 仓库信息

- **仓库名**: videodl-gui
- **上游仓库**: https://github.com/CharlesPikachu/videodl
- **自动构建**: 使用 GitHub Actions

## 一键清理并上传

### 步骤 1：运行清理脚本

```bash
clean_and_upload.bat
```

这会：
- ✅ 删除构建产物（build/, dist/, *.exe）
- ✅ 准备 custom_files 目录
- ✅ 删除 videodl 源码（会从上游克隆）
- ✅ 删除临时文件
- ✅ 初始化 Git 仓库（如果需要）

### 步骤 2：修改远程仓库地址

```bash
# 将 YOUR_USERNAME 替换为你的 GitHub 用户名
git remote set-url origin https://github.com/YOUR_USERNAME/videodl-gui.git
```

### 步骤 3：查看状态

```bash
git status
```

应该看到：
```
已添加的文件:
  .github/workflows/build.yml
  custom_files/
  prepare_custom_files.bat
  prepare_custom_files.sh
  QUICKSTART.md
  GITHUB_SETUP.md
  README_GITHUB.md
  PACKAGE.md
  .gitignore

已删除的文件:
  build/
  build_gui/
  dist/
  dist_gui/
  videodl/
  *.exe
```

### 步骤 4：提交并推送

```bash
# 添加所有文件
git add .

# 提交
git commit -m "Add GitHub Actions workflow for videodl

- Automatic build from upstream repository
- Custom GUI with tkinter
- Windows EXE artifacts
- Build documentation"

# 推送（首次推送）
git push -u origin main
```

## 如果仓库已有文件

### 方式一：强制覆盖（⚠️ 会删除远程所有文件）

```bash
# 清理远程仓库
git push origin main --force
```

### 方式二：保留远程文件（推荐）

```bash
# 先拉取远程文件
git pull origin main --allow-unrelated-histories

# 解决冲突后提交
git add .
git commit -m "Merge with existing files"
git push
```

## 验证上传

### 1. 检查 GitHub 仓库

访问：`https://github.com/YOUR_USERNAME/videodl-gui`

应该看到这些文件：
- `.github/workflows/build.yml` ✅
- `custom_files/` ✅
- `QUICKSTART.md` ✅
- `GITHUB_SETUP.md` ✅

### 2. 检查 Actions

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 应该看到 "Build videodl Windows EXE" 工作流
4. 点击查看运行状态

### 3. 等待构建完成

- 首次构建：约 15 分钟
- 后续构建：约 10 分钟

## 下载构建产物

### 从 Actions 下载

1. Actions → 点击最新的构建任务
2. 滚动到底部 "Artifacts" 区域
3. 下载 `videodl-windows.zip`

### 从 Releases 下载（创建 tag 后）

```bash
# 创建并推送 tag
git tag v1.0.0
git push origin v1.0.0
```

## 文件结构说明

### 上传后的仓库结构

```
videodl-gui/
├── .github/
│   └── workflows/
│       └── build.yml           # 自动构建配置
├── custom_files/               # 自定义修改（应用）
│   ├── main.py
│   ├── videodl_gui.py
│   ├── build_exe.spec
│   └── build_gui_exe.spec
├── prepare_custom_files.bat    # 准备脚本
├── prepare_custom_files.sh
├── QUICKSTART.md               # 快速开始
├── GITHUB_SETUP.md             # 完整指南
├── README_GITHUB.md            # 项目总结
├── PACKAGE.md                  # 打包文档
└── .gitignore                  # Git 忽略规则
```

### 不会上传的文件

- `build/`, `build_gui/` - 构建临时文件
- `dist/`, `dist_gui/` - 构建输出
- `*.exe` - 可执行文件
- `videodl/` - 源代码（从上游克隆）
- `__pycache__/` - Python 缓存

## 自动构建流程

```
GitHub 仓库 (videodl-gui)
    ↓ 触发构建
GitHub Actions
    ↓ clone 上游
CharlesPikachu/videodl
    ↓ 应用修改
custom_files/*
    ↓ 构建
videodl.exe (3-5分钟)
videodl_gui.exe (1-2分钟)
    ↓ 打包
videodl_gui.zip
    ↓ 上传
Artifacts / Release
```

## 常见问题

### Q1: 推送时提示 "remote origin already exists"

A: 更新远程仓库地址：
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/videodl-gui.git
```

### Q2: 推送时提示 "failed to push"

A: 强制推送（会删除远程文件）：
```bash
git push -f origin main
```

### Q3: Actions 构建失败

A: 查看构建日志：
1. Actions → 点击失败的构建
2. 展开查看详细日志
3. 根据错误信息修改配置

### Q4: 想要恢复被删除的文件

A: 从上游仓库重新克隆：
```bash
git clone https://github.com/CharlesPikachu/videodl.git temp_videodl
xcopy /e /i temp_videodl\videodl videodl
rmdir /s /q temp_videodl
```

## 下一步

上传完成后：

1. ✅ 等待 GitHub Actions 自动构建
2. ✅ 下载构建产物
3. ✅ 测试 videodl.exe 和 videodl_gui.exe
4. ✅ 分发给用户使用

## 相关链接

- **你的仓库**: https://github.com/YOUR_USERNAME/videodl-gui
- **上游仓库**: https://github.com/CharlesPikachu/videodl
- **Actions 页面**: https://github.com/YOUR_USERNAME/videodl-gui/actions

---

**提示**: 将 `YOUR_USERNAME` 替换为你的实际 GitHub 用户名。
