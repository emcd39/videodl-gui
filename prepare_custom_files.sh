#!/bin/bash

echo "========================================"
echo "  准备 GitHub Actions 自定义文件"
echo "========================================"

echo ""
echo "[检查目录]"
if [ ! -d "custom_files" ]; then
    echo "[创建] custom_files 目录"
    mkdir -p custom_files
fi

echo ""
echo "[复制文件]"
echo "----------------------------------------"

if [ -f "main.py" ]; then
    echo "[复制] main.py → custom_files/"
    cp -f main.py custom_files/main.py
else
    echo "[跳过] main.py (文件不存在)"
fi

if [ -f "videodl_gui.py" ]; then
    echo "[复制] videodl_gui.py → custom_files/"
    cp -f videodl_gui.py custom_files/videodl_gui.py
else
    echo "[跳过] videodl_gui.py (文件不存在)"
fi

if [ -f "build_exe.spec" ]; then
    echo "[复制] build_exe.spec → custom_files/"
    cp -f build_exe.spec custom_files/build_exe.spec
else
    echo "[跳过] build_exe.spec (文件不存在)"
fi

if [ -f "build_gui_exe.spec" ]; then
    echo "[复制] build_gui_exe.spec → custom_files/"
    cp -f build_gui_spec custom_files/build_gui_exe.spec
else
    echo "[跳过] build_gui_exe.spec (文件不存在)"
fi

echo ""
echo "========================================"
echo "  准备完成！"
echo "========================================"
echo ""
echo "custom_files 目录内容:"
ls -la custom_files/
echo ""
echo "下一步:"
echo "1. 提交代码到 GitHub"
echo "2. 推送后会自动触发构建"
echo "========================================"
