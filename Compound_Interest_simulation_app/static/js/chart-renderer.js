// HTMLドキュメントが完全に読み込まれた後に、中のコードを実行するおまじない
document.addEventListener('DOMContentLoaded', () => {

    // データを保持しているdiv要素を取得
    const chartDataElement = document.getElementById('chart-data');

    // div要素が存在する場合のみ、グラフを描画
    if (chartDataElement) {
        // データ属性からJSON文字列を取得し、JavaScriptのオブジェクト（配列）に変換
        const labels = JSON.parse(chartDataElement.dataset.labels);
        const history = JSON.parse(chartDataElement.dataset.history);

        const ctx = document.getElementById('assetChart');
        if (!ctx) return; // もしcanvas要素がなければ何もしない

        // Chart.jsを使ってグラフを新規作成
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: '資産額 (万円)',
                    data: history,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: true,
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function (value, index, values) {
                                return value + "万円";
                            }
                        }
                    }
                }
            }
        });
    }
});
