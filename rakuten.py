# Streamlitの課題に取り組む

# 楽天トラベルのデータを、取得したデータをPandasで読み込む
# グラフ化：Plotlyで読む
# ダッシュボード化：フロントに出して、インタラクティブにする（変数がさわれるようにする）
# 簡単なデプロイ？：Streamlit cloudにデプロイ

# 必要なライブラリをインポート
import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# 楽天トラベルAPIを用いて、屋久島のホテル情報を取得する

# アクセス先URLとアプリIDの指定
REQUEST_URL = "https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426"
APP_ID = "1042511151417209196"

# 必要な情報の指定
params = {
    'format':'json',
    'largeClassCode': 'japan',
    'middleClassCode': 'kagoshima',
    'smallClassCode': 'yakushima',
    'applicationId': APP_ID    
}

# 結果の取得
res = requests.get(REQUEST_URL, params)

# jsonデータの格納
result = res.json()

# 楽天トラベルのデータを、取得したデータをPandasで読み込む
# データフレームの作成
df = pd.DataFrame()

for i in range(0,len(result['hotels'])):
    hotel_info = result['hotels'][i]['hotel'][0]['hotelBasicInfo'] 
    temp_df = pd.DataFrame(hotel_info,index=[i]) 
    df = pd.concat([df,temp_df]) 

df = df[[ 'hotelName', 'hotelMinCharge', 'telephoneNo', 'reviewAverage','latitude','longitude','hotelInformationUrl',]]

# Streamlitのタイトルを表示
st.title('屋久島ホテル情報') 
st.write(df)

# hotelMinCharge × reviewAverage：reviewAverageをインタラクティブにする
slider = st.slider("最小値を確認したい平均レビューを入力してください",value=5,min_value = 1,max_value = 5,label_visibility = "visible")

df = df[ df['reviewAverage'] == slider]

fig = px.scatter(
    df,
    x="hotelMinCharge",
    y="reviewAverage",
)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)