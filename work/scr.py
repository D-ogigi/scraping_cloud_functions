import requests
from bs4 import BeautifulSoup
from datetime import date,datetime
import json

#event contextを入れないとcloud functionで動かなかった
#あと全部を関数化しないと自動実行する際の呼び出しができない
#テスト実行の際には
#python -c "import scr; scr.mscr()" で実行できる
# def mscr(event, context):
def mscr():
#tokenはjsonファイルで管理"token.json"を作ってます
  with open("token.json","r") as f:
    data = json.load(f)

#line notify
  def send_message(toban):
    tokenurl = data["token_url"]
    token = data["test_token"]
    headers = {"Authorization":"Bearer " + token}
    files = {"message":(None,toban)}
    requests.post(tokenurl, headers = headers, files = files)

#曜日を変換用
  def henkan(lines):
    d_week = {"(日)":"(Sun)", "(月)":"(Mon)", "(火)":"(Tue)", "(水)":"(Wed)",
              "(木)":"(Thu)", "(金)":"(Fri)", "(土)":"(Sat)"}
    for key, value in d_week.items():
      lines = lines.replace(key,value)
    return lines

  now = date.today()
  d = now.strftime("%Y-%m-%d 00:00:00")
  d_week = {"Sun": "日", "Mon": "月", "Tue": "火", "Wed": "水",
            "Thu": "木", "Fri": "金", "Sat": "土"}
  key = now.strftime("%a")
  w = d_week[key]
  md_time = now.strftime("%m月%d日") + f"({w})"
  toban = "\n" + md_time + "\n"#LINE二行目に表示させる日付

#スクレイピング用サイト
  url = data["scr_url"]
  r= BeautifulSoup(requests.get(url).content,"html.parser")
  get_elements = r.find_all("div",{"class":"calendar-box"})

  # 特定のクラスだけを抜き出して色々と整形
  for a in range(len(get_elements)):
    for b in range(len(get_elements[a].find_all("div",{"class":"box2"}))):
      for c in range(len(get_elements[a].find_all("div",{"class":"box2"})[b].find_all("h5",{"class":"title4"}))):
        date_data = get_elements[a].find("div",{"class":"title2"}).get_text(strip=True).replace(",","").replace("　"," ")
        date_data = str(date.today().year) +"年"+ date_data
        date_ = henkan(date_data)
        date_ = datetime.strptime(date_,"%Y年%m月%d日(%a)")#日付を変換して設定
        title3 = get_elements[a].find_all("div",{"class":"title3"})[b].get_text(strip=True).replace(",","").replace("　"," ")
        title4 = get_elements[a].find_all("div",{"class":"box2"})[b].find_all("h5",{"class":"title4"})[c].get_text(strip=True).replace(",","").replace("　"," ")
        subject = get_elements[a].find_all("div",{"class":"box2"})[b].find_all("p",{"class":"subject"})[c].get_text(strip=True).replace(",","").replace("　"," ")
        tel = get_elements[a].find_all("div",{"class":"box2"})[b].find_all("p",{"class":"tel"})[c].get_text(strip=True).replace(",","").replace("　"," ")

        #指定の日のデータのみ抽出
        if str(date_)==d:
          toban = toban + "\n" + title3 + "\n" + title4 + "\n" + subject + "\n" + tel + "\n"

  send_message(toban)

