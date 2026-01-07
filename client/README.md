# DiscordImageSync Client

## 概要

ユーザー側のクライアントアプリケーション。指定されたローカルディレクトリを監視し、サーバーを介して他のユーザーと画像ファイルを同期します。

## 主な機能

- ローカルディレクトリの監視（ファイル追加・変更検知）
- SHA-256によるファイル整合性管理
- Hybrid形式への変換（隠蔽化）
- WebSocketクライアントとしてサーバーと通信
- 受信ファイルの復元と配置

## 技術スタック

- Python 3.x
- watchdog (ファイル監視)
- websockets (WebSocketクライアント)

## セットアップ

```bash
cd client
pip install -r requirements.txt
```

## 実行

```bash
python main.py
```

## 設定

初回起動時に以下を設定：
- 同期対象のルートディレクトリ
- WebSocketサーバーのアドレス
- サーバーID（複数サーバー使用時）

## ディレクトリ構造

```
[指定ルート]/
├── [同期対象の画像ファイル]
└── .shadow/          # 管理用ディレクトリ（自動生成）
    ├── hashes/       # SHA-256管理
    └── temp/         # 受信ファイル一時保存
```
