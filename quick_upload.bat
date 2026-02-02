@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   快速上传到 videodl-gui
echo ========================================

echo.
echo 请输入你的 GitHub 用户名:
set /p USERNAME=用户名:

if "%USERNAME%"=="" (
    echo [错误] 用户名不能为空！
    pause
    exit /b 1
)

set REPO_URL=https://github.com/%USERNAME%/videodl-gui.git

echo.
echo [确认] 仓库地址: %REPO_URL%
echo.
set /p CONFIRM=确认继续？(Y/N):

if /i not "%CONFIRM%"=="Y" (
    echo [取消] 操作已取消
    pause
    exit /b 0
)

echo.
echo ========================================
echo   开始清理和上传...
echo ========================================

REM 清理文件
echo.
echo [1/4] 清理构建产物...
for /d %%d in (build build_gui dist dist_gui) do (
    if exist "%%d" (
        rmdir /s /q "%%d" 2>nul
    )
)
if exist "*.exe" del /q "*.exe" 2>nul
if exist "videodl" rmdir /s /q "videodl" 2>nul

REM 准备 custom_files
echo [2/4] 准备 custom_files...
if not exist "custom_files" mkdir custom_files
copy /Y "main.py" "custom_files\" >nul 2>&1
copy /Y "videodl_gui.py" "custom_files\" >nul 2>&1
copy /Y "build_exe.spec" "custom_files\" >nul 2>&1
copy /Y "build_gui_exe.spec" "custom_files\" >nul 2>&1

REM Git 操作
echo [3/4] Git 操作...
if not exist ".git" (
    git init
    git branch -M main
)

REM 设置远程仓库
git remote get-url origin >nul 2>&1
if !errorlevel! equ 0 (
    git remote set-url origin %REPO_URL%
    echo [更新] 远程仓库地址
) else (
    git remote add origin %REPO_URL%
    echo [添加] 远程仓库
)

REM 添加文件
echo [4/4] 提交文件...
git add .

REM 检查是否有更改
git diff --cached --quiet
if !errorlevel! equ 0 (
    echo.
    echo [提示] 没有需要提交的更改
    pause
    exit /b 0
)

git commit -m "Add GitHub Actions workflow for videodl

- Automatic build from upstream repository
- Custom GUI with tkinter
- Windows EXE artifacts"

echo.
echo ========================================
echo   准备推送到 GitHub
echo ========================================
echo.
echo 仓库地址: %REPO_URL%
echo.
echo 下一步: 手动执行以下命令推送
echo.
echo   git push -u origin main --force
echo.
echo ========================================
pause
