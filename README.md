# blog_slack_reminder

GitHub の「未執筆」ラベルが付いた Issue を毎週 Slack に通知する Python 製 Bot です。

## 機能概要

- 指定リポジトリの「未執筆」ラベル付き Issue 一覧を取得
- 各 Issue のタイトル・URL・冒頭 3 行を整形して Slack に投稿
- Issue がなければ「未執筆なし」と通知
- GitHub Actions で指定した時間に Slack へ通知されます

## Slack App設定方法

このBotを使うには、Slack Appを作成し適切な権限を設定する必要があります。

1. [Slack API](https://api.slack.com/apps) にアクセスし、「Create New App」をクリック
   - 「From scratch」を選択
   - App名を入力（例: 「Blog Reminder Bot」）
   - 使用するワークスペースを選択

2. 作成したアプリの「OAuth & Permissions」セクションへ移動

3. 「Scopes」セクションで以下のBot Token Scopesを追加:
   - `chat:write` (メッセージ送信用)

4. ページ上部の「Install to Workspace」ボタンをクリックしてアプリをインストール

5. インストール後に表示される「Bot User OAuth Token」をコピーし、環境変数 `SLACK_BOT_TOKEN` に設定

6. アプリを投稿先チャンネルに招待:
   ```
   /invite @あなたのアプリ名
   ```

7. チャンネルIDの取得:
   - Slackでチャンネルを開き、URLの最後の部分がチャンネルID
   - 取得したIDを環境変数 `SLACK_CHANNEL_ID` に設定
  
## GitHubの設定

Githubと連携するために、AccessTokenを設定する必要があります。

1. トークン作成ページにアクセス([GitHub Setting](https://github.com/settings/tokens))

  - Fine-grained tokens」または「Personal access tokens (classic)」のどちらかを選択できます。

    一般的には classic で問題ありません（必要なスコープに応じて選択してください）

2. トークンを作成

    トークンの名前（例: blog_slack_reminder token）を設定します。

    有効期限を設定（例: 30 days）。

    必要なスコープを選択します：

        ✅ repo（リポジトリの読み書き）

     プライベートリポジトリを読み込む場合は repo スコープが必要です。

3. Tokenの設定
  - 取得したTokenを、`PERSONAL_GITHUB_TOKEN`に設定してください

## 必要な環境変数

ローカルで確かめる場合は`.env`で必要な環境変数を設定してください

```sh
cp .env.sample .env
```

本番環境で動かす場合は、GitHub Actions の Secrets に以下を設定してください。

- `PERSONAL_GITHUB_TOKEN` : Issue 取得用 GitHub トークン
- `SLACK_BOT_TOKEN` : Slack Bot トークン
- `SLACK_CHANNEL_ID` : 通知先 Slack チャンネル ID
- `REPO` : 対象 GitHub リポジトリ（例: `user/repo`）

## 使い方

### ローカル実行

1. 必要なパッケージをインストール

   ```sh
   pip install -r requirements.txt
   ```

2. `.env` ファイルを用意し、環境変数を設定

3. スクリプトを実行

   ```sh
   python slack_reminder.py
   ```

### Docker で実行

```sh
docker compose up --build # 初回のみ --buildオプション付与します

docker compose up slack_reminder # スクリプト実行

docker compose up test # test実行
```

### GitHub Actions による自動実行

[.github/workflows/weekly_slack_reminder.yml](.github/workflows/weekly_slack_reminder.yml) で毎週月曜に自動実行されます。

## ファイル構成

- [slack_reminder.py](slack_reminder.py) : メインスクリプト
- [requirements.txt](requirements.txt) : 依存パッケージ
- [compose.yml](compose.yml) : Docker Compose 設定
- [Dockerfile](Dockerfile) : Docker イメージ定義
- [.github/workflows/weekly_slack_reminder.yml](.github/workflows/weekly_slack_reminder.yml) : GitHub Actions ワークフロー

## ライセンス

MIT
