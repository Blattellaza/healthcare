from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'database.db'  # 資料庫檔案路徑

# 設定健康建議的函數
def get_health_advice(blood_pressure_in, blood_pressure_out, blood_sugar, height, weight):

    health_point = 5
    # 將建議按健康指標分成字典形式
    fontLargestStrong = {'blood_pressure': [], 'blood_sugar': [], 'bmi': [], 'share': []}
    fontSecondStrong = {'blood_pressure': [], 'blood_sugar': [], 'bmi': [], 'share': []}
    fontNormalStrong = {'blood_pressure': [], 'blood_sugar': [], 'bmi': [], 'share': []}
    fontNormal = {'blood_pressure': [], 'blood_sugar': [], 'bmi': [], 'share': []}
    fontNormalStrong['share'].append("<<< 今日宜 >>>")
    # 血壓建議
    if isinstance(blood_pressure_in, float) and isinstance(blood_pressure_out, float) :
        if blood_pressure_in > 120  or blood_pressure_out > 80:
            # share page
            health_point = health_point - 1
            fontNormalStrong['share'].append("低鹽飲食")
            # result page
            fontLargestStrong['blood_pressure'].append(f"你的血壓為{blood_pressure_in}/{blood_pressure_out} mmHg")
            fontLargestStrong['blood_pressure'].append("血壓太高(・-・ꐦ)！")
            fontSecondStrong['blood_pressure'].append("！注意！")
            fontNormalStrong['blood_pressure'].append("正常情況下，你的血壓應該為：")
            fontNormalStrong['blood_pressure'].append("收縮壓90~120mmHg 和舒張壓60~80 mmHg")
            fontSecondStrong['blood_pressure'].append("！改善！")
            fontNormalStrong['blood_pressure'].append("1.戒菸：戒菸有助健康，同時可減低發生心臟病及腦中風之機率。")
            fontNormalStrong['blood_pressure'].append("2.減重：維持理想體重，可減低體重過重所增加之心臟負荷。")
            fontNormalStrong['blood_pressure'].append("3.低鹽飲食：減少鈉鹽的攝取，可使血壓下降，飲食宜採清淡，盡量避免食用醃漬食物。")
            fontNormalStrong['blood_pressure'].append("4.控制飲酒：喝酒會使高血壓藥物失去療效。要避免血壓上升，飲酒量不宜超過30公克酒精。")
            fontNormalStrong['blood_pressure'].append("5.規律運動：每天30分鐘，一個星期最好五次以上，做一些安全溫和的有氧運動，可以改善血壓過高問題。")
            
        elif blood_pressure_in < 90 or  blood_pressure_out < 60:
            # share page
            health_point = health_point - 1
            fontNormalStrong['share'].append("多喝水")
            # result page
            fontLargestStrong['blood_pressure'].append(f"你的血壓為{blood_pressure_in}/{blood_pressure_out} mmHg")
            fontLargestStrong['blood_pressure'].append("血壓太低(・-・ꐦ)！")
            fontSecondStrong['blood_pressure'].append("！注意！")
            fontNormalStrong['blood_pressure'].append("正常情況下，你的血壓應該為：")
            fontNormalStrong['blood_pressure'].append("收縮壓90~120 mmHg 和舒張壓60~80mmHg")
            fontSecondStrong['blood_pressure'].append("！改善！")
            fontNormalStrong['blood_pressure'].append("1.多喝水：增加血容量、避免脫水造成低血壓，尤其在天氣炎熱時更要注意。")
            fontNormalStrong['blood_pressure'].append("2.避免處在悶熱的環境：容易使血管舒張、血壓下降。")
            fontNormalStrong['blood_pressure'].append("3.避免穿著過緊的衣服或系過緊的領帶：容易壓迫到頸動脈竇，引起血壓驟降而昏倒。")
            fontNormalStrong['blood_pressure'].append("4.增加鹽分攝取：低血壓患者每天適量攝取約12克左右的食鹽，可改善低血壓症狀。")
            fontNormalStrong['blood_pressure'].append("5.規律運動：運動可調節神經系統、增強心血管功能，進而改善血壓過低問題。")
        elif blood_pressure_in > 120 and blood_pressure_out < 60 or blood_pressure_in < 90 and blood_pressure_out > 80:
            fontLargestStrong['blood_pressure'].append("資訊輸入錯誤")
        else:
            # share page
            health_point = health_point + 1
            # result page
            fontLargestStrong['blood_pressure'].append(f"你的血壓為{blood_pressure_in}/{blood_pressure_out} mmHg")
            fontLargestStrong['blood_pressure'].append("血壓正常٩(*´ ꒳ `*)۶")
            fontSecondStrong['blood_pressure'].append("！太棒了！")
            fontNormalStrong['blood_pressure'].append("正常情況下的血壓應該為：")
            fontNormalStrong['blood_pressure'].append("收縮壓90~120 mmHg 和舒張壓60~80mmHg")
            fontNormalStrong['blood_pressure'].append("PS.也要定期回來做檢測喔 ⑉˙ᗜ˙⑉ ")

    else:
        fontLargestStrong['blood_pressure'].append("（沒有輸入收縮壓及舒張壓）")
        fontSecondStrong['blood_pressure'].append("！注意！請完整輸入數據以獲得準確的建議！")
        

    # 血糖建議
    if isinstance(blood_sugar, float):
        if blood_sugar > 140:
            # share page
            health_point = health_point - 1
            fontNormalStrong['share'].append("不吃高GI食物")
            # result page
            fontLargestStrong['blood_sugar'].append(f"你的血糖為{blood_sugar} mg/dL")
            fontLargestStrong['blood_sugar'].append("血糖太高(・-・ꐦ)！")
            fontSecondStrong['blood_sugar'].append("！注意！")
            fontNormalStrong['blood_sugar'].append("正常情況下，你的血糖應該為：")
            fontNormalStrong['blood_sugar'].append("空腹血糖：70~100 mg/dL")
            fontNormalStrong['blood_sugar'].append("飯後兩小時血糖：70~140 mg/dL")
            fontSecondStrong['blood_sugar'].append("！改善！")
            fontNormalStrong['blood_sugar'].append("1. 避免吃高升糖指數的食物，選擇 GI 值低於 55 的低升糖指數食物，例如：糙米、燕麥、山藥、大部分蔬菜、豆魚蛋肉類、小番茄、芭樂、木瓜等。")
            fontNormalStrong['blood_sugar'].append("2. 避免吃含精緻糖的食物，像是冰糖、砂糖、高果糖漿等精製糖，避免食用麵包、冰淇淋、甜甜圈等含精緻糖的食物。")
            fontNormalStrong['blood_sugar'].append("3. 避免吃高油脂食物，選擇植物油來替代動物性脂肪（如：豬油、牛油、奶油、培根等）。")
            fontNormalStrong['blood_sugar'].append("4. 避免吃高鈉食物，並避免過度飲酒。")
        elif blood_sugar < 70:
            # share page
            health_point = health_point - 1
            fontNormalStrong['share'].append("定時三餐")
            #result page
            fontLargestStrong['blood_sugar'].append(f"你的血糖為{blood_sugar} mg/dL")
            fontLargestStrong['blood_sugar'].append("血糖太低(・-・ꐦ)！")
            fontSecondStrong['blood_sugar'].append("！注意！")
            fontNormalStrong['blood_sugar'].append("正常情況下，你的血糖應該為：")
            fontNormalStrong['blood_sugar'].append("空腹血糖：70~100 mg/dL")
            fontNormalStrong['blood_sugar'].append("飯後兩小時血糖：70~140 mg/dL")
            fontNormalStrong['blood_sugar'].append("請注意您身理上是否有虛弱、嗜睡、飢餓、臉色蒼白、冒冷汗、心跳加快、發冷、抽筋、頭暈等症狀；心理上可能會有情緒改變及行為改變。")
            fontSecondStrong['blood_sugar'].append("！改善！")
            fontNormalStrong['blood_sugar'].append("以下為可能造成低血糖的原因：")
            fontNormalStrong['blood_sugar'].append("藥物：自行調整藥物劑量不正確、用藥時間不規律等。")
            fontNormalStrong['blood_sugar'].append("飲食：三餐不定時、用藥後未進食等。")
            fontNormalStrong['blood_sugar'].append("運動：空腹運動、過度運動等。")
            fontNormalStrong['blood_sugar'].append("如果長時間處於低血糖狀態，建議就醫。")
        else:
            # share page
            health_point = health_point + 1
            #result page
            fontLargestStrong['blood_sugar'].append(f"你的血糖為{blood_sugar} mg/dL")
            fontLargestStrong['blood_sugar'].append("血糖正常٩(*´ ꒳ `*)۶")
            fontSecondStrong['blood_sugar'].append("！太棒了！")
            fontNormalStrong['blood_sugar'].append("正常情況下的血糖應該為：")
            fontNormalStrong['blood_sugar'].append("空腹血糖：70~100 mg/dL")
            fontNormalStrong['blood_sugar'].append("飯後兩小時血糖：70~140 mg/dL")
            fontNormalStrong['blood_sugar'].append("PS.也要定期回來做檢測喔 ⑉˙ᗜ˙⑉ ")
    else:
        fontLargestStrong['blood_sugar'].append("（沒有血糖資料）")
        fontSecondStrong['blood_sugar'].append("！注意！請完整輸入數據以獲得準確的建議！")

    # BMI 建議
    if isinstance(weight, float) and isinstance(height, float):
        bmi = round(weight / (height / 100) ** 2, 2)
        if bmi >= 27:
            # share page
            health_point = health_point - 2
            fontNormalStrong['share'].append("多多多多多運動")
            # result page
            fontLargestStrong['bmi'].append(f"你的BMI為{bmi} kg/m\u00B2")
            fontLargestStrong['bmi'].append("肥胖(・-・ꐦ)！")
            fontSecondStrong['bmi'].append("！注意！")
            fontNormalStrong['bmi'].append("健康的BMI應該為：18.5～24 kg/m\u00B2")
            fontNormalStrong['bmi'].append("肥胖會增加心血管疾病、糖尿病等慢性病風險，請立即採取行動！")
            fontSecondStrong['bmi'].append("！改善！")
            fontNormalStrong['bmi'].append("1.建議減少高脂肪、高糖食物的攝取（如甜點、油炸食物、含糖飲料等）。")
            fontNormalStrong['bmi'].append("2.多選擇富含纖維的食物（如蔬菜、水果和全穀類），有助於增加飽足感。")
            fontNormalStrong['bmi'].append("3.增加有氧運動（如快走、慢跑或騎自行車），每週至少進行150分鐘，幫助燃燒熱量。")
            fontNormalStrong['bmi'].append("4.每餐適量控制，避免暴飲暴食，並養成規律的飲食習慣，避免宵夜。")
        elif 24 <= bmi < 27:
            # share page
            health_point = health_point - 1
            fontNormalStrong['share'].append("拒絕久坐")
            #result page
            fontLargestStrong['bmi'].append(f"你的BMI為{bmi} kg/m\u00B2")
            fontLargestStrong['bmi'].append("過重(・-・ꐦ)！")
            fontSecondStrong['bmi'].append("！注意！")
            fontNormalStrong['bmi'].append("健康的BMI應該為：18.5～24 kg/m\u00B2")
            fontNormalStrong['bmi'].append("體重過重可能帶來健康問題，建議調整生活方式。")
            fontSecondStrong['bmi'].append("！改善！")
            fontNormalStrong['bmi'].append("1.建議控制每天的總熱量攝取，減少高熱量食物如糕點、含糖飲料等。")
            fontNormalStrong['bmi'].append("2.可以考慮多吃高蛋白低脂肪的食物，如魚、豆類、瘦肉等，有助於保持肌肉質量。")
            fontNormalStrong['bmi'].append("3.每天堅持運動，如散步、快走、爬樓梯等，逐步養成運動習慣。")
            fontNormalStrong['bmi'].append("4.避免久坐，建議每隔一段時間起身活動，讓身體保持活力。")
        elif 18.5 <= bmi < 24:
            # share page
            health_point = health_point + 1
            # result page
            fontLargestStrong['bmi'].append(f"你的BMI為{bmi} kg/m\u00B2")
            fontLargestStrong['bmi'].append("健康體重٩(*´ ꒳ `*)۶")
            fontSecondStrong['bmi'].append("！太棒了！")
            fontNormalStrong['bmi'].append("健康的BMI應該為：18.5～24 kg/m\u00B2")
            fontNormalStrong['bmi'].append("雖然健康，但仍需保持良好的生活習慣！")
            fontNormalStrong['bmi'].append("1.建議選擇均衡飲食，包含蛋白質、碳水化合物、健康脂肪以及維生素和礦物質，確保營養充足。")
            fontNormalStrong['bmi'].append("2.保持每週的運動頻率，如散步、瑜伽、慢跑等，讓身體保持健康活力。")
            fontNormalStrong['bmi'].append("3.定期檢查體重，以便及時調整生活習慣，防止體重波動。")
            fontNormalStrong['bmi'].append("PS.也要定期回來做檢測喔 ⑉˙ᗜ˙⑉ ")
        else:
            # share page
            health_point = health_point - 1
            fontNormalStrong['share'].append("吃飽飽")
            # result page
            fontLargestStrong['bmi'].append(f"你的BMI為{bmi} kg/m\u00B2")
            fontLargestStrong['bmi'].append("過輕(・-・ꐦ)！")
            fontSecondStrong['bmi'].append("！注意！")
            fontNormalStrong['bmi'].append("健康的BMI應該為：18.5～24 kg/m\u00B2")
            fontNormalStrong['bmi'].append("體重過輕可能導致營養不良和免疫力下降，請關注健康！")
            fontSecondStrong['bmi'].append("！改善！")
            fontNormalStrong['bmi'].append("需要多運動，均衡飲食，以增加體能，維持健康！")
            fontNormalStrong['bmi'].append("可以增加優質碳水化合物的攝取，如全穀類、燕麥、紅薯等，為身體提供足夠的能量。")
            fontNormalStrong['bmi'].append("每天進行適量的力量訓練，如舉重或阻力訓練，增強肌肉，幫助體重增長。")
            fontNormalStrong['bmi'].append("確保攝取足夠的營養，多吃健康的點心，如水果乾、酸奶、花生醬夾心麵包等。")
    else:
        fontLargestStrong['bmi'].append("（沒有身高或體重資料）")
        fontSecondStrong['bmi'].append("！注意！請完整輸入數據以獲得準確的建議！")

    #print(fontLargestStrong['blood_sugar'])
    
    if health_point == 5 + 3:
        fontNormalStrong['share'].append("到問答區分享你的健康密技")
        fontNormalStrong['share'].append("獲得稱號：健康老司機")
    elif 5 < health_point <= 7:
        fontNormalStrong['share'].append("繼續保持")
        fontNormalStrong['share'].append("獲得稱號：健康寶寶")
    elif 3 < health_point <= 5:
        fontNormalStrong['share'].append("向健康小幫手學習健康秘訣")
        fontNormalStrong['share'].append("獲得稱號：新手健康駕駛")
    elif 1 <= health_point <= 3:
        fontNormalStrong['share'].append("好好注意身體健康！")
        fontNormalStrong['share'].append("獲得稱號：健康菜鳥")
    fontNormalStrong['share'].append(f"今日健康評分：{health_point}")
    return fontLargestStrong, fontSecondStrong, fontNormalStrong, fontNormal


# 主頁面路由
@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, problem_subject, problem_type, problem_lastEditDate, problem_status FROM HealthQA ORDER BY problem_lastEditDate DESC")
    questions = cursor.fetchall()
    #print(questions)
    conn.close()
    return render_template("index.html", questions=questions)

# 結果頁面路由
@app.route('/result', methods=['POST'])
def result():
    # 取得表單數據
    blood_pressure_in = float(request.form.get('blood_pressure_in')) if request.form.get('blood_pressure_in') else None
    blood_pressure_out = float(request.form.get('blood_pressure_out')) if request.form.get('blood_pressure_out') else None
    blood_sugar = float(request.form.get('blood_sugar')) if request.form.get('blood_sugar') else None
    height = float(request.form.get('height')) if request.form.get('height') else None
    weight = float(request.form.get('weight')) if request.form.get('weight') else None

    # 取得健康建議
    fontLargestStrong, fontSecondStrong, fontNormalStrong, fontNormal = get_health_advice(blood_pressure_in, blood_pressure_out, blood_sugar, height, weight)

    return render_template(
        'result.html',
        fontLargestStrong=fontLargestStrong,
        fontSecondStrong=fontSecondStrong,
        fontNormalStrong=fontNormalStrong,
        fontNormal=fontNormal
    )

#share
# @app.route('/share', methods=['GET'])
# def share():
#     # 模擬固定數據，或者可以根據需求實現更動態的邏輯
#     fontLargestStrong, fontSecondStrong, fontNormalStrong, fontNormal = get_health_advice(120, 80, 70, 170, 65)
#     return render_template('share.html', fontNormalStrong=fontNormalStrong)


@app.route('/share', methods=['GET', 'POST'])
def share():
    # 使用 POST 接受用戶輸入，或者使用 GET 來獲取一些默認數據
    if request.method == 'POST':
        blood_pressure_in = float(request.form.get('blood_pressure_in')) if request.form.get('blood_pressure_in') else None
        blood_pressure_out = float(request.form.get('blood_pressure_out')) if request.form.get('blood_pressure_out') else None
        blood_sugar = float(request.form.get('blood_sugar')) if request.form.get('blood_sugar') else None
        height = float(request.form.get('height')) if request.form.get('height') else None
        weight = float(request.form.get('weight')) if request.form.get('weight') else None
    else:
        # 默認值或基於 session 的值
        blood_pressure_in = 120
        blood_pressure_out = 80
        blood_sugar = 70
        height = 170
        weight = 65

    fontLargestStrong, fontSecondStrong, fontNormalStrong, fontNormal = get_health_advice(blood_pressure_in, blood_pressure_out, blood_sugar, height, weight)
    
    return render_template('share.html', fontNormalStrong=fontNormalStrong)

# 新增 GI 值介紹頁面的路由
@app.route('/GI')
def GI():
    return render_template('GI.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html')

@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "POST":
        problem_subject = request.form["subject"]
        problem_detail = request.form["detail"]
        problem_type = request.form["type"]
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO HealthQA (problem_subject, problem_detail, problem_type) 
            VALUES (?, ?, ?)
        """, (problem_subject, problem_detail, problem_type))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("ask.html")

@app.route("/question/<int:question_id>", methods=["GET", "POST"])
def question_detail(question_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 獲取問題詳細資訊
    cursor.execute("SELECT id, problem_subject, problem_type, problem_detail, answer_detail, problem_status FROM HealthQA WHERE id = ?", (question_id,))
    question = cursor.fetchone()
    #print(question)

    if not question:
        return "問題未找到", 404  # 如果没有找到问题
    
    if request.method == "POST":  # 處理新增回答
        answer = request.form["answer"]
        cursor.execute("""
            UPDATE HealthQA 
            SET answer_detail = ?, answer_lastEditDate = ?, problem_status = '已解決'
            WHERE id = ?
        """, (answer, datetime.now(), question_id))
        conn.commit()
        conn.close()
        return redirect(url_for("question_detail", question_id=question_id))

    conn.close()
    return render_template("question_detail.html", question=question)

@app.route("/delete/<int:question_id>", methods=["POST"])
def delete_question(question_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 获取问题详细信息
    cursor.execute("DELETE FROM HealthQA WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

