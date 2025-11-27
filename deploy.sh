#!/bin/bash

# --- 設定區 ---
REPO_URL="https://github.com/112303542/ME2025_Midterm3"
PROJECT_DIR="ME2025_Midterm3" 

# 檢查專案資料夾是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    # ==========================================
    # 首次執行 (First Run)
    # ==========================================
    echo "Directory $PROJECT_DIR does not exist. Starting first deployment..."

    # 1. 自動 clone repository
    git clone "$REPO_URL"
    
    # 進入專案資料夾
    cd "$PROJECT_DIR" || exit

    # 2. 建立虛擬環境，命名為 .venv
    python3 -m venv .venv

    # 3. 自動安裝 requirements.txt 中的套件
    # 啟動虛擬環境
    source .venv/bin/activate
    # 升級 pip (選用，但建議)
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "Error: requirements.txt not found."
    fi

    # 4. 啟動 app.py
    # > app.log 2>&1 代表將輸出存到 app.log 方便除錯
    echo "Starting app.py..."
    nohup python3 app.py > app.log 2>&1 &
    
    echo "First deployment finished."

else
    # ==========================================
    # 第二次以後執行 (Subsequent Run)
    # ==========================================
    echo "Directory $PROJECT_DIR exists. Updating deployment..."

    # 進入專案資料夾
    cd "$PROJECT_DIR" || exit

    # 1. 自動更新專案版本
    git pull

    # 2. 檢查 requirements.txt 中未安裝的套件並安裝
    # 啟動虛擬環境
    source .venv/bin/activate
    # pip install 會自動檢查，只安裝缺失的套件
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi

    # 3. 重啟 app.py
    echo "Restarting app.py..."
    
    # 尋找正在執行的 app.py process 並強制結束 (kill)
    # pkill -f 會搜尋完整的指令行參數
    pkill -f "python3 app.py"
    
    # 等待 2 秒確保釋放 port
    sleep 2
    
    # 重新啟動
    nohup python3 app.py > app.log 2>&1 &
    
    echo "Update and restart finished."
fi
