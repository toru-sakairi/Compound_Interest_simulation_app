from Compound_Interest_simulation_app import app
from flask import render_template, request, redirect, url_for


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template(
        'main.html'
    )


@app.route('/InputData', methods=['POST'])
def inputData():
    principal = float(request.form['principal'])
    rate = float(request.form['rate'])
    years = int(request.form['years'])

    # 単純計算
    #result_total = calculate_compound_interest(principal, rate, years)
    
    # 資産推移のリストと、歳のラベルリストを取得
    asset_history,year_labels = calculate_compound_interest_history(principal, rate, years)
    
    # 最終結果はリスト最後の値
    final_result = asset_history[-1]
    
    print(f"【デバッグ情報】 asset_historyの型は: {type(asset_history)} です")

    return render_template(
        'main.html',
        result=final_result,
        input_principal=principal,
        input_rate=rate,
        input_years=years,
        # グラフ用に二つのリストをHTMLに渡す
        asset_history = asset_history,
        year_labels = year_labels
    )

# １年ごとの資産推移と、グラフのラベル（X軸）を返す変数
def calculate_compound_interest_history(principal, rate, years):
    # １年ごとの資産額を入れるリスト
    history = []
    # グラフのX軸に表示する「〇年目」というラベルを入れるリスト
    labels = []

    current_amount = float(principal)
    rate_decimal = float(rate) / 100

    # 0年目から運用年数までループ
    for year in range(int(years) + 1):
        # グラフのラベルを追加
        labels.append(f"{year}年目")
        # その年の資産額をリストに追加
        history.append(current_amount)
        # 次の歳の資産額を計算
        current_amount *= (1 + rate_decimal)

    return history, labels


# 複利計算関数
def calculate_compound_interest(principal, rate, years):
    # 計算ロジック
    rate_decimal = rate / 100
    result = principal * ((1 + rate_decimal) ** years)
    return result
