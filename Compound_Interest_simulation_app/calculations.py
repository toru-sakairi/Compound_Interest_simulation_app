# 計算ロジック専門
import math

def calculate_total(principal , rate, years, monthly_investment):
    history = []
    labels = []
    # 初期投資を最初にtotalに代入しておく
    total_amount = principal
    # 月利に変換
    monthly_rate = float(rate) / 100 / 12
    # 全期間の月数
    total_months = int(years) * 12
    
    for month in range(total_months + 1):
        if month % 12 == 0:
            year = month // 12
            labels.append(f"{year}年目")
            history.append(round(total_amount, 2))
            
        if month == total_months:
            break
            
        #毎月の積立額を加算し、その合計に利息をつける
        total_amount = (total_amount + float(monthly_investment)) * (1 + monthly_rate)

    # 最終年がリストに含まれていない場合、追加する
    if f"{int(years)}年目" not in labels:
        labels.append(f"{int(years)}年目")
        history.append(round(total_amount, 2))
        
    return history, labels, float(total_amount)
    
def calculate_monthly_investment(principal , rate, years, total):
    """
    目標金額に必要な月額を計算し、その場合の資産推移(history)も同時に生成する。

    :return: (必要な毎月の積立額, 資産推移リスト, 年数ラベルリスト) のタプル
    """
    # =================================================================
    # ステップ1：必要な毎月の積立額を計算する (逆算ロジックはそのまま)
    # =================================================================
    principal_yen = float(principal)
    total_goal_yen = float(total)
    
    # 年利が0、または期間が0の場合は計算不能（または短銃計算）
    if float(rate) == 0:
        if int(years) == 0: return [], [], 0 # 期間が0の時は積み立てられない
        # 利息が付かない場合、単純計算
        needed_total_investment = total_goal_yen - principal_yen
        # 必要な積立額がマイナスなら0円
        required_monthly = needed_total_investment / (int(years) * 12) if needed_total_investment > 0 else 0
    else:
        # 単位を月ベースに変換
        monthly_rate = float(rate) / 100 / 12
        total_months = int(years) * 12
        # 期間が0の場合は積立額も0
        if total_months == 0: return [], [], 0

        # 初期投資額だけで目標を達成できるかチェック　模試でキルならば積立不要
        if principal_yen * ((1 + monthly_rate) ** total_months) >= total_goal_yen:
            required_monthly = 0
        # 積立で増やすべき金額を計算する
        else:
            # 目標金額から、初期投資額が将来増える分を差し引く
            future_value_of_principal = principal_yen * ((1 + monthly_rate) ** total_months)
            target_from_installments = total_goal_yen - future_value_of_principal
            # 年金終価の公式を使う。
            # 係数 = ((1 × 月利)^月数 - 1) / 月利
            coefficient = (((1 + monthly_rate) ** total_months) - 1) / monthly_rate
            # 必要な積立額が0以下の場合は0を返す
            required_monthly = target_from_installments / coefficient if coefficient > 0 else 0
    
    # required_monthly がマイナスになる場合を考慮し、0以上にする
    required_monthly = max(0, required_monthly)

    # =================================================================
    # ステップ2：求めた月額を使って、資産推移（history, labels）を計算する
    # =================================================================
    history = []
    labels = []
    total_amount = principal_yen  # スタートは初期投資額
    monthly_rate_for_history = float(rate) / 100 / 12
    total_months_for_history = int(years) * 12

    for month in range(total_months_for_history + 1):
        if month % 12 == 0:
            year = month // 12
            labels.append(f"{year}年目")
            history.append(total_amount)
        
        if month == total_months_for_history:
            break
            
        # ★★★ ここでステップ1で計算した required_monthly を使う ★★★
        total_amount = (total_amount + required_monthly) * (1 + monthly_rate_for_history)

    # =================================================================
    # ステップ3：計算した3つの値をすべて返す
    # =================================================================
    return history, labels, float(required_monthly)
    
def calculate_years(principal , rate, monthly_investment, total):
    """
    目標金額に必要な積立期間(年数)を計算し、その場合の資産推移も生成する。

    :return: (必要な年数, 資産推移リスト, 年数ラベルリスト) のタプル
             計算不可能な場合は (-1, [], []) を返す
    """
    # =================================================================
    # ステップ1：必要な期間（年数）を計算する (逆算ロジック)
    # =================================================================
    
    # 0.【準備】単位を計算用に変換
    principal_yen = float(principal)
    total_goal_yen = float(total)
    monthly_investment_yen = float(monthly_investment)
    
    # 目標額が初期投資額以下なら、期間は0年
    if total_goal_yen <= principal_yen:
        # この場合でも0年時点のグラフは表示できるようにデータを返す
        return [principal_yen], ["0年目"], 0

    # 年利が0の場合の特別処理
    if float(rate) == 0:
        # 積立額も0なら目標達成は不可能
        if monthly_investment_yen <= 0:
            return [], [], -1 # 計算不能を示す-1を返す
        
        needed_to_save = total_goal_yen - principal_yen
        total_months = math.ceil(needed_to_save / monthly_investment_yen)
        required_years = total_months / 12
    
    # 年利が0でない場合の通常処理
    else:
        monthly_rate = float(rate) / 100 / 12

        # 積立をしても資産が減るような非現実的なケースは計算不能
        if principal_yen * monthly_rate + monthly_investment_yen <= 0:
            return [], [], -1

        # ★★★★★ ここが対数(log)を使った計算の核心部 ★★★★★
        # log( (目標額*月利 + 月積立額) / (元本*月利 + 月積立額) )
        log_numerator = math.log(total_goal_yen * monthly_rate + monthly_investment_yen)
        log_denominator = math.log(principal_yen * monthly_rate + monthly_investment_yen)
        
        # log(1 + 月利)
        log_rate = math.log(1 + monthly_rate)
        
        # 月数を計算
        total_months = (log_numerator - log_denominator) / log_rate
        required_years = total_months / 12

    # =================================================================
    # ステップ2：求めた年数を使って、資産推移を計算する
    # =================================================================
    history = []
    labels = []
    total_amount = principal_yen
    
    # 計算で求めた月数（切り上げ）を使ってループ
    final_total_months = math.ceil(required_years * 12)

    for month in range(final_total_months + 1):
        if month % 12 == 0:
            year = month // 12
            labels.append(f"{year}年目")
            history.append(total_amount)
        
        if month == final_total_months:
            # 最終月は目標額を超えているはずなので、正確な目標額で上書きするとグラフが綺麗になる
            if history[-1] < total_goal_yen:
                 history.append(total_goal_yen)
                 labels.append(f"{required_years:.1f}年目")
            break
            
        total_amount = (total_amount + monthly_investment_yen) * (1 + monthly_rate)
        
    # =================================================================
    # ステップ3：計算した3つの値をすべて返す
    # =================================================================
    return history, labels, int(required_years)
    
