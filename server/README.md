# DiscordImageSync Server

## 概要

Discord BOTサーバー実装。WebSocketサーバーとして動作し、複数のクライアントからの接続を管理します。

## 主な機能

- Discord BOTとしてチャンネルを監視
- WebSocketサーバーとしてクライアントと双方向通信
- ISH-Hybrid形式のファイルをDiscordへアップロード
- 受信したファイルを各クライアントへ配信

## 技術スタック

- Python 3.x
- discord.py (Discord API)
- websockets (WebSocketサーバー)

## セットアップ

```bash
cd server
pip install -r requirements.txt
```

## 実行

```bash
python bot.py
```

## 環境変数

- `DISCORD_TOKEN`: Discord BOTのトークン
- `CHANNEL_ID`: 監視対象のチャンネルID
- `WS_PORT`: WebSocketサーバーのポート（デフォルト: 8765）
