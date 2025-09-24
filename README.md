# otree-econ-exp-team1

経済実験用のoTreeのソースコードを管理するリポジトリ


## 📘 はじめに：GitHubとは？

GitHubは、ソースコードをオンラインで管理・共有するためのサービスです。  
複数人での開発や、ソースコードの変更履歴の管理を行うことができます。

---

## 🔐 1. GitHub アカウントの登録方法

1. 下記URLにアクセス：  
   👉 https://github.com/
2. 右上の「Sign up」ボタンをクリック
3. メールアドレス、ユーザー名、パスワードを入力
4. 届いたメールで認証
5. GitHubにログインできればOKです！

---

## 💻 2. Git のインストール（ローカル(自分のPC上)で使うツール）

Gitを使ってソースコードのバージョン管理を行います。
（Gitを使うことで正常に動いていたバージョンに戻せたり、機能を追加したり修正した時に、いつ誰がどの部分を治したのか把握できるようになる。）

### ◉ Windowsの場合：

1. 下記URLからGitをダウンロード：  
   👉 https://git-scm.com/download/win
2. [Git for Windows/x64 Setup.]をクリックする　（インストールするツールをダウンロードできる）
3. インストーラーを実行し、基本的に「Next」で進めてOKです。


◉ インストール確認
Power shell または　コマンドプロンプト　で以下のコマンドを実行してgit version x.x.x と表示されればInstall成功です。

`git --version`


## 📥 3. リポジトリのクローン方法

◉ クローンとは？

GitHub上にあるプロジェクトを、自分のPCにまるごとコピーする操作です。
これにより、ローカル（自分のPC）でソースコードを編集できるようになります。


◉ 手順
1.	ターミナルやコマンドプロンプトを開く
2.	oTreeのファイルをを配置したい場所で以下のコマンドを実行：

`git clone https://github.com/nakajinbee/otree-econ-exp-team1.git`

3.	フォルダ otree-econ-exp-team1 が作成され、中にソースコードが入っています。


## ✏️ 4. ソースコードを修正してGitHubに反映する手順

以下のコマンドは、ターミナルまたはコマンドプロンプトで、
otree-econ-exp-team1 フォルダ内で実行してください。

```
# 1. フォルダに移動
cd otree-econ-exp-team1

# 2. 変更されたファイルを確認
git status

# 3. 変更をステージに追加
git add .

# 4. 変更内容にコメントを付けてコミット
git commit -m "〇〇を修正しました"

# 5. GitHubに反映（push）
git push origin main
```

上記の後、GitHubを見ると、自分が修正したソースコードを確認できる。

otree-econ-exp-team1　を開き、 `otree devserver` コマンドを実行することで、oTreeを起動することができる。


⭐️ 5. ソースコードを最新化する方法

otree-econ-exp-team1 フォルダ内で以下のコマンドを実行する
`git pull`

上記を実行することでGitHub上の最新のソースコードを取得することができる。
