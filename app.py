from flask import Flask, render_template, request

app = Flask(__name__)

# 設定健康建議的函數
def get_health_advice(blood_pressure_in, blood_pressure_out, blood_sugar, height, weight):
    # 將建議按健康指標分成字典形式
    fontLargestStrong = {'blood_pressure': [], 'blood_sugar': [], 'bmi': []}
    fontSecondStrong = {'blood_pressure': [], 'blood_sugar': [], 'bmi': []}
    fontNormalStrong = {'blood_pressure': [], 'blood_sugar': [], 'bmi': []}
    fontNormal = {'blood_pressure': [], 'blood_sugar': [], 'bmi': []}
    
    # 血壓建議
    if isinstance(blood_pressure_in, float) and isinstance(blood_pressure_out, float) :
        if blood_pressure_in > 120  or blood_pressure_out > 80:
            fontLargestStrong['blood_pressure'].append("血壓太高>120/80")
            fontSecondStrong['blood_pressure'].append("！注意！")
            fontNormalStrong['blood_pressure'].append("正常情況下，你的血壓應該為：")
            fontNormalStrong['blood_pressure'].append("收縮壓90~120mmHg 和舒張壓60~80mmHg")
            fontSecondStrong['blood_pressure'].append("！改善！")
            fontNormalStrong['blood_pressure'].append("1.戒菸：戒菸有助健康，同時可減低發生心臟病及腦中風之機率。")
            fontNormalStrong['blood_pressure'].append("2.減重：維持理想體重，可減低體重過重所增加之心臟負荷。")
            fontNormalStrong['blood_pressure'].append("3.低鹽飲食：減少鈉鹽的攝取，可使血壓下降，飲食宜採清淡，盡量避免食用醃漬食物。")
            fontNormalStrong['blood_pressure'].append("4.控制飲酒：喝酒會使高血壓藥物失去療效。要避免血壓上升，飲酒量不宜超過30公克酒精。")
            fontNormalStrong['blood_pressure'].append("5.規律運動：每天30分鐘，一個星期最好五次以上，做一些安全溫和的有氧運動，可以改善血壓過高問題。")
        elif blood_pressure_in < 90 or  blood_pressure_out < 60:
            fontLargestStrong['blood_pressure'].append("血壓太低<90/60")
            fontSecondStrong['blood_pressure'].append("！注意！")
            fontNormalStrong['blood_pressure'].append("正常情況下，你的血壓應該為：")
            fontNormalStrong['blood_pressure'].append("收縮壓90~120mmHg 和舒張壓60~80mmHg")
            fontSecondStrong['blood_pressure'].append("！改善！")
            fontNormalStrong['blood_pressure'].append("1.多喝水：增加血容量、避免脫水造成低血壓，尤其在天氣炎熱時更要注意。")
            fontNormalStrong['blood_pressure'].append("2.避免處在悶熱的環境：容易使血管舒張、血壓下降。")
            fontNormalStrong['blood_pressure'].append("3.避免穿著過緊的衣服或系過緊的領帶：容易壓迫到頸動脈竇，引起血壓驟降而昏倒。")
            fontNormalStrong['blood_pressure'].append("4.增加鹽分攝取：低血壓患者每天適量攝取約12克左右的食鹽，可改善低血壓症狀。")
            fontNormalStrong['blood_pressure'].append("5.規律運動：運動可調節神經系統、增強心血管功能，進而改善血壓過低問題。")
        elif blood_pressure_in > 120 and blood_pressure_out < 60 or blood_pressure_in < 90 and blood_pressure_out > 80:
            fontLargestStrong['blood_pressure'].append("資訊輸入錯誤")
        else:
            fontLargestStrong['blood_pressure'].append("正常")
    else:
        fontLargestStrong['blood_pressure'].append("沒有輸入收縮壓及舒張壓")

    # 血糖建議
    if isinstance(blood_sugar, float):
        if blood_sugar > 140:
            fontLargestStrong['blood_sugar'].append("血糖太高>140")
            fontSecondStrong['blood_sugar'].append("！注意！")
            fontNormalStrong['blood_sugar'].append("正常情況下，你的血糖應該為：")
            fontNormalStrong['blood_sugar'].append("空腹血糖：70~100mg/dL")
            fontNormalStrong['blood_sugar'].append("飯後兩小時血糖：70~140mg/dL")
            fontSecondStrong['blood_sugar'].append("！改善！")
            fontNormalStrong['blood_sugar'].append("1. 避免吃高升糖指數的食物，選擇 GI 值低於 55 的低升糖指數食物，例如：糙米、燕麥、山藥、大部分蔬菜、豆魚蛋肉類、小番茄、芭樂、木瓜等。")
            fontNormalStrong['blood_sugar'].append("2. 避免吃含精緻糖的食物，像是冰糖、砂糖、高果糖漿等精製糖，避免食用麵包、冰淇淋、甜甜圈等含精緻糖的食物。")
            fontNormalStrong['blood_sugar'].append("3. 避免吃高油脂食物，選擇植物油來替代動物性脂肪（如：豬油、牛油、奶油、培根等）。")
            fontNormalStrong['blood_sugar'].append("4. 避免吃高鈉食物，並避免過度飲酒。")
        elif blood_sugar < 70:
            fontLargestStrong['blood_sugar'].append("血糖太低<70")
            fontSecondStrong['blood_sugar'].append("！注意！")
            fontNormalStrong['blood_sugar'].append("正常情況下，你的血糖應該為：")
            fontNormalStrong['blood_sugar'].append("空腹血糖：70~100mg/dL")
            fontNormalStrong['blood_sugar'].append("飯後兩小時血糖：70~140mg/dL")
            fontNormalStrong['blood_sugar'].append("請注意您身理上是否有虛弱、嗜睡、飢餓、臉色蒼白、冒冷汗、心跳加快、發冷、抽筋、頭暈等症狀；心理上可能會有情緒改變及行為改變。")
            fontSecondStrong['blood_sugar'].append("！改善！")
            fontNormalStrong['blood_sugar'].append("以下為可能造成低血糖的原因：")
            fontNormalStrong['blood_sugar'].append("藥物：自行調整藥物劑量不正確、用藥時間不規律等。")
            fontNormalStrong['blood_sugar'].append("飲食：三餐不定時、用藥後未進食等。")
            fontNormalStrong['blood_sugar'].append("運動：空腹運動、過度運動等。")
            fontNormalStrong['blood_sugar'].append("如果長時間處於低血糖狀態，建議就醫。")
        else:
            fontLargestStrong['blood_sugar'].append("正常")
    else:
        fontLargestStrong['blood_sugar'].append("沒有血糖資料")

    # BMI 建議
    if isinstance(weight, float) and isinstance(height, float):
        bmi = round(weight / (height / 100) ** 2, 2)
        if bmi >= 27:
            fontLargestStrong['bmi'].append(f"你的BMI為{bmi} -> 啊～「肥胖」，需要立刻力行「健康體重管理」囉！建議減少高脂肪、高糖食物的攝取，如甜點、油炸食物、含糖飲料等。多選擇富含纖維的食物，例如蔬菜、水果和全穀類，有助於增加飽足感。增加有氧運動，如快走、慢跑或騎自行車，每週至少進行150分鐘，幫助燃燒熱量。每餐適量控制，避免暴飲暴食，並養成規律的飲食習慣，避免宵夜。")
            fontSecondStrong['bmi'].append("！注意！肥胖會增加心血管疾病、糖尿病等慢性病風險，請立即採取行動！")
        elif 24 <= bmi < 27:
            fontLargestStrong['bmi'].append(f"你的BMI為{bmi} -> 「體重過重」，要小心囉，趕快力行「健康體重管理」！建議控制每天的總熱量攝取，減少高熱量食物如糕點、含糖飲料等。可以考慮多吃高蛋白低脂肪的食物，如魚、豆類、瘦肉等，有助於保持肌肉質量。每天堅持運動，如散步、快走、爬樓梯等，逐步養成運動習慣。避免久坐，建議每隔一段時間起身活動，讓身體保持活力。")
            fontSecondStrong['bmi'].append("！注意！體重過重可能帶來健康問題，建議調整生活方式。")
        elif 18.5 <= bmi < 24:
            fontLargestStrong['bmi'].append(f"你的BMI為{bmi} -> 恭喜！「健康體重」，要繼續保持！建議選擇均衡飲食，包含蛋白質、碳水化合物、健康脂肪以及維生素和礦物質，確保營養充足。保持每週的運動頻率，如散步、瑜伽、慢跑等，讓身體保持健康活力。定期檢查體重，以便及時調整生活習慣，防止體重波動。")
            fontSecondStrong['bmi'].append("！注意！雖然健康，但仍需保持良好的生活習慣！")
        else:
            fontLargestStrong['bmi'].append(f"你的BMI為{bmi} -> 「體重過輕」，需要多運動，均衡飲食，以增加體能，維持健康！可以增加優質碳水化合物的攝取，如全穀類、燕麥、紅薯等，為身體提供足夠的能量。每天進行適量的力量訓練，如舉重或阻力訓練，增強肌肉，幫助體重增長。確保攝取足夠的營養，多吃健康的點心，如水果乾、酸奶、花生醬夾心麵包等。")
            fontSecondStrong['bmi'].append("！注意！體重過輕可能導致營養不良和免疫力下降，請關注健康！")
    else:
        fontLargestStrong['bmi'].append("沒有身高或體重資料")
        fontSecondStrong['bmi'].append("！注意！請完整輸入數據以獲得準確的建議！")


    return fontLargestStrong, fontSecondStrong, fontNormalStrong, fontNormal


# 主頁面路由
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

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

# 新增 GI 值介紹頁面的路由
@app.route('/GI')
def GI():
    return render_template('GI.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html')


if __name__ == '__main__':
    app.run(debug=True)
