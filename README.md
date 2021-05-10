# Screen Captor SAKURA
SAKURAは手順書作成等の、スクリーンショットを行うためのツールです.  
オペレーションを行いながら、最小限の操作でスクリーンショットをExcelへ記録することができます.

![image](https://user-images.githubusercontent.com/50811989/110207576-ceea8600-7ec7-11eb-8b63-829d5514343c.png)

![image](https://user-images.githubusercontent.com/50811989/110207624-17a23f00-7ec8-11eb-9f18-d2a3124f1227.png)

# Documentation
## 動作環境
- OS : Windows 8.1/10
- Microsoft Excel : 2019/Office365

## 環境構築
### Pythonで実行する場合
#### 前提条件
pythonがインストールされていること
> - [pythonのインストール](https://www.python.org/downloads/)

#### 導入手順
1. 資産をローカルPCへダウンロードする
    - Gitからクローンする、または、zipファイルをダウンロード
    > - Gitからクローンする場合のコマンド
    > `git clone https://github.com/Trend-Research-and-Trial/Screen-Captor-Sakura.git`
    > - [zipファイルのダウンロード](https://github.com/Trend-Research-and-Trial/Screen-Captor-Sakura/archive/refs/heads/master.zip)

2. pythonライブラリ各種インストール
    - 下記コマンドで必要ライブラリをインストール  
    `pip install -r requirements.txt` 
    (`requirements.txt` ファイルがあるディレクトリで実行すること)

3. コマンドプロンプトからアプリ実行
    - ダウンロード先のディレクトリで下記コマンドを実行  
    `python main.py` 

### 「.exe」で使用する場合 (非推奨)

1. 下記より「scs.zip」をダウンロード
    - https://github.com/Trend-Research-and-Trial/Screen-Captor-Sakura/releases

2. ダウンロードフォルダにある「.exe」を実行 

※「.exe」は最新バージョンでない可能性があります.  
※ 動作環境によっては、「.exe」の実行が制限されている場合があります.  


## 操作方法
1. 作成したいファイル名を入力
![image](https://user-images.githubusercontent.com/50811989/110207603-f3def900-7ec7-11eb-9665-5beb828fe2e5.png)



2. 画面キャプチャを行いたい画面でPrintScreenキーを押下する

3. 強調したい部分をドラッグアンドドロップで赤枠で囲み、説明を記載する
![image](https://user-images.githubusercontent.com/50811989/110207836-479e1200-7ec9-11eb-9d94-a397f514011c.png)

4. 次へを押下する (F12)

5. 2~4 を繰り返す

6. 手順作成を終了する場合はESCキーを押下

### Excelの出力先
- 実行したファイルと同一ディレクトリの`output`ディレクトリ配下


## 制約事項
- 複数のディスプレイで使用しているときも、スクリーンショットが取れるのはメインディスプレイのみ
- 赤枠は画像に埋め込むため、複数の枠をつけたい場合はツール操作完了後にExcelで赤枠を追加する

# Request & Bug report
- [githubのissueを発行する](https://github.com/Trend-Research-and-Trial/Screen-Captor-Sakura/issues/new)
- 以下へメールを送る
  - wakate2019@gmail.com
