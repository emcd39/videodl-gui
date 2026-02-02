@echo off
chcp 65001 >nul
echo ========================================
echo   清理并准备上传到 videodl-gui
echo ========================================

echo.
echo [1/5] 清理构建产物...
if exist "build" (
    echo [删除] build/
    rmdir /s /q "build"
)
if exist "build_gui" (
    echo [删除] build_gui/
    rmdir /s /q "build_gui"
)
if exist "dist" (
    echo [删除] dist/
    rmdir /s /q "dist"
)
if exist "dist_gui" (
    echo [删除] dist_gui/
    rmdir /s /q "dist_gui"
)
if exist "*.exe" (
    echo [删除] *.exe
    del /q "*.exe" 2>nul
)

echo.
echo [2/5] 准备 custom_files 目录...
if not exist "custom_files" mkdir custom_files

if exist "main.py" (
    echo [复制] main.py → custom_files/
    copy /Y "main.py" "custom_files\main.py" >nul
)
if exist "videodl_gui.py" (
    echo [复制] videodl_gui.py → custom_files/
    copy /Y "videodl_gui.py" "custom_files\videodl_gui.py" >nul
)
if exist "build_exe.spec" (
    echo [复制] build_exe.spec → custom_files/
    copy /Y "build_exe.spec" "custom_files\build_exe.spec" >nul
)
if exist "build_gui_exe.spec" (
    echo [复制] build_gui_exe.spec → custom_files/
    copy /Y "build_gui_exe.spec" "custom_files\build_gui_exe.spec" >nul
)

echo.
echo [3/5] 删除 videodl 源码目录（会从上游克隆）...
if exist "videodl" (
    echo [删除] videodl/
    rmdir /s /q "videodl"
)

echo.
echo [4/5] 删除其他不必要的文件...
if exist "*.pyc" (
    del /s /q "*.pyc" 2>nul
)
if exist "__pycache__" (
    rmdir /s /q "__pycache__" 2>nul
)

echo.
echo [5/5] Git 操作...
echo.

REM 检查是否是 git 仓库
if not exist ".git" (
    echo [初始化] Git 仓库
    git init
    git branch -M main
)

REM 添加远程仓库
echo [检查] 远程仓库
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo [添加] 远程仓库: origin
    git remote add origin https://github.com/YOUR_USERNAME/videodl-gui.git
) else (
    echo [更新] 远程仓库已存在
)

echo.
echo ========================================
echo   清理完成！准备上传
echo ========================================
echo.
echo 当前保留的文件:
echo.
echo - .github/workflows/build.yml (GitHub Actions)
echo - custom_files/ (自定义修改)
echo - prepare_custom_files.bat/sh (准备脚本)
echo - QUICKSTART.md (快速开始)
echo - GITHUB_SETUP.md (完整指南)
echo - README_GITHUB.md (项目总结)
echo - PACKAGE.md (打包文档)
echo - .gitignore (Git 忽略规则)
echo.
echo 下一步操作:
echo.
echo 1. 修改远程仓库地址（如果需要）:
echo    git remote set-url origin https://github.com/你的用户名/videodl-gui.git
echo.
echo 2. 查看将要提交的文件:
echo    git status
echo.
echo 3. 提交并推送:
echo    git add .
echo    git commit -m "Add GitHub Actions workflow for videodl"
echo    git push -u origin main
echo.
echo ========================================
pause
