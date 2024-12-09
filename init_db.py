import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')  # 連接到資料庫檔案，若無檔案則自動創建
    cursor = conn.cursor()

    # 建立 HealthQA 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HealthQA (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_subject TEXT NOT NULL,
            problem_detail TEXT NOT NULL,
            problem_type TEXT,
            problem_lastEditDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            answer_detail TEXT,
            answer_lastEditDate DATETIME DEFAULT NULL,
            problem_status TEXT DEFAULT '待回答'
        )
    ''')
    conn.commit()
    conn.close()
    init_db()  # 執行資料庫初始化
    print("資料表已初始化完成！")


    
