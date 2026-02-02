@echo off
chcp 65001 >nul
echo ========================================
echo   准备 GitHub Actions 自定义文件
echo ========================================

echo.
echo [检查目录]
if not exist "custom_files" (
    echo [创建] custom_files 目录
    mkdir custom_files
)

echo.
echo [复制文件]
echo ----------------------------------------

if exist "main.py" (
    echo [复制] main.py → custom_files\
    copy /Y "main.py" "custom_files\main.py" >nul
) else (
    echo [跳过] main.py (文件不存在)
)

if exist "videodl_gui.py" (
    echo [复制] videodl_gui.py → custom_files\
    copy /Y "videodl_gui.py" "custom_files\videodl_gui.py" >nul
) else (
    echo [跳过] videodl_gui.py (文件不存在)
)

if exist "build_exe.spec" (
    echo [复制] build_exe.spec → custom_files\
    copy /Y "build_exe.spec" "custom_files\build_exe.spec" >nul
) else (
    echo [跳过] build_exe.spec (文件不存在)
)

if exist "build_gui_exe.spec" (
    echo [复制] build_gui_exe.spec → custom_files\
    copy /Y "build_gui_exe.spec" "custom_files\build_gui_exe.spec" >nul
) else (
    echo [跳过] build_gui_exe.spec (文件不存在)
)

echo.
echo ========================================
echo   准备完成！
echo ========================================
echo.
echo custom_files 目录内容:
dir /B custom_files
echo.
echo 下一步:
echo 1. 提交代码到 GitHub
echo 2. 推送后会自动触发构建
echo ========================================
pause
