from Compound_Interest_simulation_app import app
from flask import render_template, request, redirect, url_for
from . import calculations


@app.route('/')
def index():
    # 初期表示時にも 'inputs' ディクショナリを渡す
    # これにより、テンプレートで 'inputs' が未定義になるのを防ぎます。
    initial_outputs = {'type': 'total'}
    return render_template('main.html', outputs=initial_outputs)


@app.route('/calculate', methods=['POST'])
def calculates():
    # フォームから計算タイプを取得
    calc_type = request.form.get('calculation_type', 'How_much')

    asset_history = []
    year_labels = []

    # 先に全ての可能性のある値を取得し、数値に変換しておく
    principal = float(request.form.get('principal', 0))
    rate = float(request.form.get('rate', 0))
    years = int(request.form.get('years', 10))
    monthly_investment = float(request.form.get('monthly_investment', 0))
    total = float(request.form.get('total', 0))

    # 初期化
    outputs = {'principal': principal, 'rate': rate, 'years': years,
               'monthly_investment': monthly_investment, 'total': total, 'type': calc_type}

    if (calc_type == 'total'):
        asset_history, year_labels, outputs['total'] = calculations.calculate_total(
            principal, rate, years, monthly_investment)

    elif (calc_type == 'monthly_investment'):
        asset_history, year_labels, outputs['monthly_investment'] = calculations.calculate_monthly_investment(
            principal, rate, years, total)

    elif (calc_type == 'years'):
        asset_history, year_labels, outputs['years'] =calculations.calculate_years(
            principal, rate, monthly_investment, total
        )

    return render_template(
        'main.html',
        # 入力されたものと出力するものを含むからoutputsにした
        outputs=outputs,
        # グラフ用:グラフは書くこと変わらないから
        asset_history=asset_history,
        year_labels=year_labels
    )
