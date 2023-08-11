# mappl_bot
MaPPLのDiscord鯖用予定リマインドbot

## 導入方法
[Google Cloud Platform](https://console.cloud.google.com/)にアクセスし、新しいプロジェクトを作成する。

プロジェクト名は適当に決める。

プロジェクトを作成し終えたら、左上のあたりにあるボタンから作ったプロジェクトを選択する。

左上のハンバーガーメニュー(≡みたいなやつ)をクリックし、APIとサービス>有効なAPIとサービスを押して出てきたページにある[APIとサービスの有効化]を押す。

"google drive api"と検索し、一番上に出てきたものをクリックし、[有効にする]ボタンを押す。

同様にして"google sheets api"も有効化する。

左上のハンバーガーメニューをクリックし、APIとサービス>認証情報を押して出てきたページにある[+認証情報を作成]>[サービス アカウント]の順に押す。

サービスアカウント名、アカウントIDを適当に入力し、[完了]を押す。

作成したサービスアカウントのメールアドレスをメモしておく。

作成したサービスアカウントのメールの部分をクリックし、出てきたページのキータブを選択し、[鍵を追加]>[新しい鍵を作成]を押し、キーのタイプがJSON担っていることを確認して[作成]を押す。

自動的にjsonファイルのダウンロードダイアログが出るので、credential.jsonと名前をつけて保存する。

GCP上での作業は一旦終わり。

[Google Spreadsheetのテンプレート](https://docs.google.com/spreadsheets/d/1ksaixAmJ1DKcp1AqKvngOCJo8mJHhd9vDue89mGjFHc/)を開き、ファイル>コピーを作成で自身のドライブの好きな場所にコピーする。

コピーしたスプレッドシートを開き、urlのhttps://docs.google.com/spreadsheets/d/XXXXXX/editのうち、XXXXXXに当たる部分をメモしておく。

スプレッドシートのページ右上の[共有]を押し、[ユーザーやグループを追加]にメモしておいたサービスアカウントのメールアドレスを入力、権限を編集者として[送信]を押す。

[DiscordのDeveloperポータル](https://discord.com/developers/applications)にアクセスし、[New Application]を押す。名前を適当に決めて規約に同意するにチェックを入れて[Create]を押す。

アイコン画像やDESCRIPTIONは適当に入力する。

左側のメニューからBotを押し、出てきたページの[Reset Token]を押して出力されたトークン(長い文字列)をメモしておく。

Privileged Gateway Intentsの欄の3つのボタンすべてをONにする。

左側のメニューからOAuth2>URL Generatorの順に押し、出てきたページのSCOPESからbotを選択、さらに出てくるBOT PERMISSIONSからAdministratorを選択する。

一番下に出てくるGENERATED URLをコピーし、ブラウザで開く。

botを導入したいサーバーを選択して[Continue]を押し、Administratorにチェックを入れて[Authorize]を押す。

私は人間ですのチェックを入れて完了し、botを導入したDiscordの鯖を開く。

自身のアカウント設定画面から詳細設定>開発者モードをONにして、botが通知を行うチャンネルを右クリック(スマホだと長押し)してチャンネルIDをコピーし、メモしておく。

再び[Google Cloud Platform](https://console.cloud.google.com/)にアクセスし、左上のメニューからCompute Engine>VM インスタンスを押し、Compute Engine APIの[有効にする]ボタンを押す。

課金が必要というダイアログが出たら[課金を有効にする]を押す。(実際はクレジットカードの情報を入力するだけ。完全無料枠を使うので実際にお金が請求されることはない)

いい感じに情報を入力し、[無料トライアルを開始]を押す。

Compute Engine APIのページに戻ってきたら再度[有効にする]ボタンを押す。

くるくるマークの途中でもいいから左上のメニューからCompute Engine>VM インスタンスを押し、出てきたページの[インスタンスを作成]ボタンを押す。

名前は適当に決めて、リージョンはus-west1(オレゴン)、マシンタイプはe2-micro、ブートディスクは[変更]を押してブートディスクの種類を標準永続ディスクに変更して[選択]を押す。(※注意！この設定を守らないと無料枠から外れて請求される可能性がある！！)

作成を押してしばらくすると、VMインスタンスの一覧に作成したインスタンスが表示される。

[SSH]と書かれた部分をクリックし、しばらく待つと表示されるダイアログの[Authorize]をクリック。

出てきたポップアップウィンドウの[自身のアカウント名]@[インスタンス名]:~$の右隣をクリックし、カーソルが点滅することを確認する。

その状態で以下のコマンドを順に実行していく。

`sudo apt update`

`sudo apt install python3 python3-dev python3-venv wget`

`wget https://bootstrap.pypa.io/get-pip.py`

`sudo python3 get-pip.py`

`sudo pip install discord.py[voice] gspread oauth2client`

ターミナルの画面は開いたまま、当リポジトリからmain.py data_operation.py discord_bot.py jst_time.pyを自身のPCに保存する。

main.pyをメモ帳なりvscodeなりで開いて、以下の部分に自身がメモしてきた文字列を挿入する。

```python
# 定数の宣言
try:
    TOKEN = ""
    CHANNEL_ID = ""
    jsonf = "credential.json"
    sheet_key = ""
    logger.info("Variable set.")
```

TOKENはDiscordBotのトークン、CHANNEL_IDはBotが通知するようのチャンネルのID、sheet_keyはGoogleスプレッドシートのIDに対応する。ダブルクオーテーションに挟まれた部分に文字列を貼り付ける。

編集したmain.pyとダウンロードしたdata_operation.py、discord_bot.py、jst_time.py、credential.jsonをターミナルの[ファイルをアップロード]ボタンからアップロードする。

アップロードが終わったらターミナルに`ls -a`と打ち込んで、ちゃんとアップロードできているか確認する。できていなかったらもう一度アップロードする。

続けてターミナルに`pwd`と打ち込み、出力された文字をコピーする。

最後に、GoogleCloudPlatformのVMインスタンスのページから自分の作成したインスタンスを選択し、[編集]を押す。

下の方にある自動化の項目の起動スクリプトの欄に、以下の内容を入力する。

```
cd [pwdの出力結果] && python3 main.py
```

保存を押したあとに出るページで[停止]を押したあと[開始/再開]を押して完成。お疲れ様！
