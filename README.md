# sample_flask_database

Flask とデータベースを連携するためのテスト用レポジトリ

## 機能

- タスクの新規登録
- タスクの削除
- タスクの取得
- タスクの情報変更

タスクは以下のパラメータを持つ

- id
- name
- description
- created_at
- updated_at

## 使用技術

- Flask
- SQLite
- Flask-SQLAlchemy
- flask-restx
- Flask-Migrate
- gunicorn

## 使用ライブラリのメリット

### Flask-SQLAlchemy

- SQLAlchemy の機能を Flask で簡単に使える
- モデル定義が直感的で、Python のクラスとして書ける
- データベース操作が Python のオブジェクト操作として書ける

### flask-restx

- Swagger UI による API ドキュメントの自動生成

### Flask-Migrate

- データベーススキーマのバージョン管理が可能
- 既存データを保持したままスキーマ変更が可能
- チーム開発でのスキーマ変更の共有が容易
- ロールバック機能で安全なスキーマ変更が可能

### gunicorn

- 複数のワーカープロセスで並列処理が可能
- ワーカープロセスがクラッシュしても自動的に再起動
- メモリリークを防ぐ（定期的な再起動）
- 本番環境での安定した運用が可能

## 動作手順

### 開発環境

```bash
# 環境構築
python -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# データベースの初期化
flask db init  # migrationsファイルを作成
flask db migrate -m "initial migration"  # database.dbを作成
flask db upgrade  # テーブルを作成

# アプリケーションの起動
python app.py
```

### 本番環境

```bash
# 環境構築
python -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# データベースの初期化
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# アプリケーションの起動（4プロセス）
gunicorn -w 4 -b 0.0.0.0:8000 \
  --log-file - \
  --access-logfile - \
  --error-logfile - \
  app:app
```

## マイグレーションコマンド

```bash
# マイグレーションファイルの作成
flask db migrate -m "変更内容の説明"

# マイグレーションの適用
flask db upgrade

# マイグレーションのロールバック
flask db downgrade
```
