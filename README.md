# blog_slack_reminder

GitHub の Issue を活用したブログ執筆管理・通知システムです。

## 機能概要

このシステムでは、以下の機能を提供します：

### 1. ブログ候補通知機能

- 指定リポジトリの「未執筆」ラベル付き Issue 一覧を取得して Slack に通知
  - 各 Issue のタイトル・URL・冒頭 2 行を整形して投稿
  - Issue がなければ「未執筆なし」と通知

### 2. 週次執筆統計機能

- 過去 1 週間に「執筆済」ラベル付きでクローズされた Issue を集計
  - 今週執筆した記事の件数と一覧を通知
  - 執筆した記事がなければその旨を通知

この Bot を使うには、Slack App を作成し適切な権限を設定する必要があります。

1. [Slack API](https://api.slack.com/apps) にアクセスし、「Create New App」をクリック

   - 「From scratch」を選択
   - App 名を入力（例: 「Blog Reminder Bot」）
   - 使用するワークスペースを選択

2. 作成したアプリの「OAuth & Permissions」セクションへ移動

3. 「Scopes」セクションで以下の Bot Token Scopes を追加:

   - `chat:write` (メッセージ送信用)

4. ページ上部の「Install to Workspace」ボタンをクリックしてアプリをインストール

5. インストール後に表示される「Bot User OAuth Token」をコピーし、環境変数 `SLACK_BOT_TOKEN` に設定

6. アプリを投稿先チャンネルに招待:

   ```
   /invite @あなたのアプリ名
   ```

7. チャンネル ID の取得:
   - Slack でチャンネルを開き、URL の最後の部分がチャンネル ID
   - または API Testing で `conversations.list` を呼び出して確認
   - 取得した ID を環境変数 `SLACK_CHANNEL_ID` に設定

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

   **ブログ候補通知:**

   ```sh
   python slack_reminder.py
   ```

   **週次執筆統計通知:**

   ```sh
   python weekly_stats.py
   ```

   **テスト実行:**

   ```sh
   # 全てのテストを実行
   python -m unittest discover -p "test_*.py" -v

   # 特定のテストファイルのみ実行
   python -m unittest test_base_notification_service.py -v
   ```

### Docker で実行

```sh
docker compose up --build # 初回のみ --buildオプション付与します

# ブログ候補通知の実行
docker compose up slack_reminder

# 週次統計通知の実行
docker compose up weekly_stats

# テスト実行
docker compose up test
```

### GitHub Actions による自動実行

以下のワークフローが自動実行されます：

- **ブログ候補通知**: [.github/workflows/weekly_slack_reminder.yml](.github/workflows/weekly_slack_reminder.yml) で毎週月曜に実行
- **週次統計通知**: 毎週日曜に先週の執筆統計を集計・通知
- **テスト実行**: Pull Request 作成時やコード変更時に自動実行

## ファイル構成

### メインスクリプト

- [slack_reminder.py](slack_reminder.py) : ブログ候補通知スクリプト
- [weekly_stats.py](weekly_stats.py) : 週次統計通知スクリプト

### ライブラリモジュール

- [base_notification_service.py](base_notification_service.py) : 通知サービスの基底クラス
- [github_client.py](github_client.py) : GitHub API クライアント
- [issue_formatter.py](issue_formatter.py) : Issue フォーマッター
- [slack_notifier.py](slack_notifier.py) : Slack 通知クライアント

### テストファイル

- [test_base_notification_service.py](test_base_notification_service.py) : 基底クラスのテスト
- [test_github_client.py](test_github_client.py) : GitHub クライアントのテスト
- [test_issue_formatter.py](test_issue_formatter.py) : フォーマッターのテスト
- [test_slack_notifier.py](test_slack_notifier.py) : Slack 通知のテスト
- [test_slack_reminder.py](test_slack_reminder.py) : ブログ候補通知のテスト
- [test_weekly_stats.py](test_weekly_stats.py) : 週次統計のテスト

### 設定・デプロイファイル

- [requirements.txt](requirements.txt) : 依存パッケージ
- [compose.yml](compose.yml) : Docker Compose 設定
- [Dockerfile](Dockerfile) : Docker イメージ定義
- [.github/workflows/weekly_slack_reminder.yml](.github/workflows/weekly_slack_reminder.yml) : GitHub Actions ワークフロー

## ライセンス

MIT
