#!/bin/bash

echo "========================================"
echo "  videodl 打包脚本 v1.0"
echo "========================================"

echo ""
echo "[检查环境]"
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装 Python"
    exit 1
fi

if ! pip3 show pyinstaller &> /dev/null; then
    echo "[安装] PyInstaller..."
    pip3 install pyinstaller
fi

echo ""
echo "[1/2] 打包 videodl（核心下载程序）..."
echo "----------------------------------------"
pyinstaller --clean build_exe.spec --workpath=./build --distpath=./dist -y
if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] videodl 打包失败！"
    exit 1
fi
echo "[成功] videodl 打包完成！"

echo ""
echo "[2/2] 打包 videodl_gui（GUI界面）..."
echo "----------------------------------------"
pyinstaller --clean build_gui_exe.spec --workpath=./build_gui --distpath=./dist_gui -y
if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] videodl_gui 打包失败！"
    exit 1
fi
echo "[成功] videodl_gui 打包完成！"

echo ""
echo "========================================"
echo "  打包完成！"
echo "========================================"
echo "  输出文件："
echo "  - videodl     → dist/videodl"
echo "  - videodl_gui → dist_gui/videodl_gui/videodl_gui"
echo ""
echo "  分发说明："
echo "  将 dist/videodl 复制到 dist_gui/videodl_gui/ 目录"
echo "  然后分发整个 videodl_gui 文件夹"
echo "========================================"

# 询问是否复制 videodl 到 GUI 目录
echo ""
read -p "是否复制 videodl 到 GUI 目录？(Y/N): " copy_exe
if [[ "$copy_exe" == "Y" || "$copy_exe" == "y" ]]; then
    echo ""
    echo "[复制] videodl → dist_gui/videodl_gui/"
    cp -f "dist/videodl" "dist_gui/videodl_gui/videodl"
    if [ $? -eq 0 ]; then
        echo "[成功] 文件已复制，现在可以直接分发 videodl_gui 目录"
    else
        echo "[错误] 文件复制失败，请手动复制"
    fi
fi

echo ""
