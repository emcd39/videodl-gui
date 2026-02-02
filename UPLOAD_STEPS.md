# 🚀 videodl-gui 上传步骤

## 方式一：一键上传（推荐）⭐

### 运行快速上传脚本

```bash
quick_upload.bat
```

**脚本会自动：**
1. 清理所有构建产物
2. 准备 custom_files 目录
3. 删除 videodl 源码（从上游克隆）
4. 初始化 Git 仓库
5. 设置远程仓库地址
6. 提交所有文件
7. 提示你执行推送命令

### 完成推送

```bash
git push -u origin main --force
```

**注意**:
- 使用 `--force` 会覆盖远程仓库的所有文件
- 如果要保留远程文件，请使用"方式二"

---

## 方式二：手动清理后上传

### 步骤 1：运行清理脚本

```bash
clean_and_upload.bat
```

### 步骤 2：修改远程仓库地址

```bash
# 将 YOUR_USERNAME 替换为你的用户名
git remote set-url origin https://github.com/YOUR_USERNAME/videodl-gui.git
```

### 步骤 3：查看状态

```bash
git status
```

### 步骤 4：提交并推送

```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push -u origin main
```

---

## 方式三：完全手动操作

### 1. 删除不需要的文件

```bash
# Windows PowerShell
Remove-Item -Recurse -Force build, build_gui, dist, dist_gui, videodl
Remove-Item -Force *.exe
```

### 2. 准备 custom_files

```bash
# 运行准备脚本
prepare_custom_files.bat
```

### 3. 初始化 Git

```bash
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/videodl-gui.git
```

### 4. 提交并推送

```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push -u origin main
```

---

## 上传后验证

### ✅ 检查文件

访问 `https://github.com/YOUR_USERNAME/videodl-gui`

应该看到：
```
.github/
  └── workflows/
      └── build.yml
custom_files/
prepare_custom_files.bat
QUICKSTART.md
GITHUB_SETUP.md
README_GITHUB.md
PACKAGE.md
.gitignore
```

### ✅ 触发构建

推送后会自动触发 GitHub Actions，等待 15 分钟

### ✅ 下载产物

1. 进入仓库 → Actions 标签
2. 点击最新的构建任务
3. 滚动到底部下载 `videodl-windows.zip`

---

## 构建产物

### 下载后得到

```
videodl-windows.zip
├── videodl.exe         # 核心程序（200-300MB）
└── videodl_gui.zip     # GUI 程序
    ├── videodl_gui.exe
    ├── videodl.exe
    └── _internal/
```

### 使用方式

**GUI 方式**（推荐）：
1. 解压 `videodl_gui.zip`
2. 运行 `videodl_gui.exe`
3. 输入视频链接，选择保存目录
4. 点击"开始下载"

**命令行方式**：
```bash
videodl.exe -i "视频URL"
```

---

## 📋 脚本说明

### clean_and_upload.bat
完整的清理和上传脚本，包含详细提示。

### quick_upload.bat
快速上传脚本，只需输入用户名即可。

### prepare_custom_files.bat
准备 custom_files 目录的辅助脚本。

---

## ⚠️ 注意事项

1. **force 推送**
   - 会覆盖远程仓库的所有文件
   - 确保仓库是新建的或不重要

2. **首次推送**
   - 可能需要 GitHub 身份验证
   - 使用 Personal Access Token 或 SSH key

3. **构建时间**
   - 首次构建：约 15 分钟
   - 后续构建：约 10 分钟

4. **上游代码**
   - 每次构建都从上游获取最新代码
   - 无需手动同步

---

## 🎯 完成！

上传完成后：
- ✅ GitHub Actions 自动构建
- ✅ 每次推送都会触发构建
- ✅ 从 Actions 下载 EXE 文件
- ✅ 分发给用户使用

---

**详细指南**: [UPLOAD_GUIDE.md](UPLOAD_GUIDE.md)
**快速开始**: [QUICKSTART.md](QUICKSTART.md)
**完整文档**: [GITHUB_SETUP.md](GITHUB_SETUP.md)
