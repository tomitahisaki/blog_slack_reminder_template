# blog_slack_reminder

GitHub の「未執筆」ラベルが付いた Issue を毎週 Slack に通知する Python 製 Bot です。

## 機能概要

- 指定リポジトリの「未執筆」ラベル付き Issue 一覧を取得
- 各 Issue のタイトル・URL・冒頭 3 行を整形して Slack に投稿
- Issue がなければ「未執筆なし」と通知
- GitHub Actions で指定した時間に Slack へ通知されます

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
