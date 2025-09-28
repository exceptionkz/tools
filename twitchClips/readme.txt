■動作確認してる環境
OS:Win11
Python ver:3.9.13

■どうやって動かすの
・Python3.9.13をダウンロード&インストール
https://www.python.org/downloads/release/python-3913/
画面下部の"Windows installer (64-bit)"をクリックしてダウンロード

・環境変数にPythonのパスを設定(必須じゃないけど推奨)
C:\Users\#{yourDir}\AppData\Local\Programs\Python\Python39\
#{yourDir}は自分の環境に読み替えてね

・polling_twitch_clips.pyをダウンロード
適当なディレクトリに保存しといて
間違えて消さないようにC:直下がいいかも

・twitch developersでClientIDとSecretを作成
twitchホーム画面左上の三点リーダーからデベロッパーを押す
アプリ作成するとコンソール下部に出てくるよ。
細かいことはググるかchatGPTに聞いて

・送信したいDiscordサーバーのチャンネルでWebhookを作成
対象チャンネルの設定から連携サービス→ウェブフック→新しいウェブフックの順に押す

・ダウンロードしたPythonコードの上部を書き換える
前段で取得したTwitch ClientID,Secret,Discord WebhookURLを書き換える。
あと、クリップ取得したいユーザ名も書き換える

・試しに実行してみる
コマンドプロンプト（Windowsキー→cmd→Enter）を開いて↓のコマンド入れる。
例
python C:\twitchClips\polling_twitch_clips.py
ディレクトリは自分でダウンロードしたところに読み替えてね

・多分エラー出るからchatGPTに色々聞いてみる
コマンドプロンプトに出たエラーを丸っとコピーしてchatGPTに貼り付け
原因教えてくれるから対処してみて
多分pipっていうソフト入れてエラー解消することになる

・エラー解消されたら
好きなタイミングで実行する or Windowsのタスクスケジューラに登録して定期実行する

・Windowsタスクスケジューラで定期実行する
ググって
※気が向いたら更新する
