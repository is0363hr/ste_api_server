.
├── common
│   └── models  ---  DBのテーブルを定義
│       └── cloud.py
├── config　---  設定フォルダ
│   ├── base_setting.py
│   └── local_setting.py
├── controllers  ---  コントローラー（ルーティングなどを定義）
│   └── index.py
├── interceptors
│   ├── Auth.py  ---  認証系処理
│   └── errorHandler.py  ---  エラー処理
├── modules
│   ├── db_controller.py  ---  DBへのクエリ実行
│   └── meteorological_img.py  ---  気象庁から地図、雲画像の取得
├── static  ---  静的ファイル置き場（画像）
│   ├── cartopy  ---  Python作成地図
│   ├── cloud  ---  雲画像（気象庁）
│   ├── map  ---  地図画像（気象庁）
│   └── sye  ---  雲・地図画像の合成画像
│       └── zoom2  ---  縮尺レベル
│           ├── 202102190410.png
│           ├── ......
│           └── 202102190600.png
├── templates  ---  htmlファイル置き場
│   ├── common  ---  共通レイアウト
│   │   └── layout.html
│   ├── index.html
│   └── test.html
├── application.py  ---  設定ファイルの読み込み、DBへの接続
├── apscheduler_img.py  ---  定期的な実行処理
├── manager.py  ---  アプリ実行スクリプト
└── www.py  ---  アプリの登録