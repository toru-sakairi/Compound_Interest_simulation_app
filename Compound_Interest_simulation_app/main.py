from Compound_Interest_simulation_app import app
from flask import render_template, request, redirect, url_for


@app.route('/')
def index():
    # 初期表示時にも 'inputs' ディクショナリを渡す
    # これにより、テンプレートで 'inputs' が未定義になるのを防ぎます。
    initial_inputs = {'type': 'lump_sum'}
    return render_template('main.html', inputs=initial_inputs)


# 2025-06-7　変更
@app.route('/calculate', methods=['POST'])
def calculate():
    # フォームから計算タイプを取得
    calc_type = request.form.get('calculation_type','lump_sum')
    
    # 共通のデータを取得
    rate = request.form.get('rate', '0')
    years = request.form.get('years', '0')
    
    # 計算結果を初期化
    asset_history = []
    year_labels = []
    inputs = {'rate':float(rate), 'years':int(years), 'type':calc_type}
    
    # 計算タイプに応じて処理を分岐
    if calc_type == 'lump_sum':
        principal = request.form.get('principal', '0')
        asset_history, year_labels = calculate_lump_sum_history(principal, rate, years)
        inputs['principal'] = float(principal)
    elif calc_type == 'installment':
        monthly_investment = request.form.get('monthly_investment', '0')
        asset_history, year_labels = calculate_installment_history(monthly_investment, rate, years)
        inputs['monthly_investment'] = int(monthly_investment)
    
    final_result = asset_history[-1] if asset_history else 0
    
    return render_template(
        'main.html',
        result = final_result,
        inputs = inputs,
        asset_history = asset_history,
        year_labels = year_labels
    )

# １年ごとの資産推移と、グラフのラベル（X軸）を返す変数
def calculate_lump_sum_history(principal, rate, years):
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

def calculate_installment_history(monthly_investment, rate, years):
    history = []
    labels = []
    total_amount = 0.0
    #月利に変換
    monthly_rate = float(rate) / 100 / 12
    #全期間の月数
    total_months = int(years) * 12
    
    for month in range(total_months + 1):
        if month % 12 == 0:
            year = month // 12
            labels.append(f"{year}年目")
            history.append(round(total_amount, 2))
            
        #毎月の積立額を加算し、その合計に利息をつける
        total_amount = (total_amount + float(monthly_investment)) * (1 + monthly_rate)

    # 最終年がリストに含まれていない場合、追加する
    if f"{int(years)}年目" not in labels:
        labels.append(f"{int(years)}年目")
        history.append(round(total_amount, 2))
        
    return history, labels

            