"""
NASA Worldview から 過去7日間分の衛星画像（PNG形式） を自動でダウンロードするPythonスクリプトで
NASA EarthdataのAPIキーや認証は不要な範囲でWorldview Snapshot APIを利用します。
スクリプトと同じディレクトリに nasa_worldview_images フォルダが作られ、その中に画像が保存されます。
"""
import requests
from datetime import datetime, timedelta
import os

# 出力ディレクトリを作成
output_dir = "nasa_worldview_images"
os.makedirs(output_dir, exist_ok=True)

# Worldview Snapshot API のベースURL
BASE_URL = "https://wvs.earthdata.nasa.gov/api/v1/snapshot"

# パラメータ設定
params_template = {
    "REQUEST": "GetSnapshot",
    "TIME": "",  # 日付（後で埋める）
    "BBOX": "30,129,46,146",  # 日本周辺 (south,west,north,east)
    "CRS": "EPSG:4326",
    "LAYERS": "MODIS_Terra_CorrectedReflectance_TrueColor",
    "WRAP": "DAY",
    "FORMAT": "image/png",
    "WIDTH": 1200,
    "HEIGHT": 800
}

# 過去7日分の画像を取得
for i in range(7):
    date = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
    params = params_template.copy()
    params["TIME"] = date
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        filename = os.path.join(output_dir, f"japan_{date}.png")
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"[OK] {date} 保存完了: {filename}")
    else:
        print(f"[NG] {date} の取得に失敗（ステータス: {response.status_code}）")
