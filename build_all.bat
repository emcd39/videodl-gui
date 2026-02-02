@echo off
chcp 65001 >nul
echo ========================================
echo   videodl 打包脚本 v1.0
echo ========================================

echo.
echo [检查环境]
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [安装] PyInstaller...
    pip install pyinstaller
)

echo.
echo [1/2] 打包 videodl.exe（核心下载程序）...
echo ----------------------------------------
pyinstaller --clean build_exe.spec --workpath=./build --distpath=./dist -y
if %errorlevel% neq 0 (
    echo.
    echo [错误] videodl.exe 打包失败！
    pause
    exit /b 1
)
echo [成功] videodl.exe 打包完成！

echo.
echo [2/2] 打包 videodl_gui.exe（GUI界面）...
echo ----------------------------------------
pyinstaller --clean build_gui_exe.spec --workpath=./build_gui --distpath=./dist_gui -y
if %errorlevel% neq 0 (
    echo.
    echo [错误] videodl_gui.exe 打包失败！
    pause
    exit /b 1
)
echo [成功] videodl_gui.exe 打包完成！

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo   输出文件：
echo   - videodl.exe     → dist\videodl.exe
echo   - videodl_gui.exe → dist_gui\videodl_gui\videodl_gui.exe
echo.
echo   分发说明：
echo   将 dist\videodl.exe 复制到 dist_gui\videodl_gui\ 目录
echo   然后分发整个 videodl_gui 文件夹
echo ========================================

REM 询问是否复制 videodl.exe 到 GUI 目录
echo.
set /p copy_exe="是否复制 videodl.exe 到 GUI 目录？(Y/N): "
if /i "%copy_exe%"=="Y" (
    echo.
    echo [复制] videodl.exe → dist_gui\videodl_gui\
    copy /Y "dist\videodl.exe" "dist_gui\videodl_gui\videodl.exe" >nul
    if %errorlevel% equ 0 (
        echo [成功] 文件已复制，现在可以直接分发 videodl_gui 目录
    ) else (
        echo [错误] 文件复制失败，请手动复制
    )
)

echo.
pause
