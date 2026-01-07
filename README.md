# DiscordImageSync

注意：まだ動きません

Discordをシグナリングおよびデータストレージとして利用し、特定ユーザー間で画像ファイルを構造ごと同期するシステムです。

## [Server](./server/README.md)

Discord BOTサーバーの実装。WebSocketを介してクライアントと通信し、Discord APIを経由してファイル転送を仲介します。

## [Client](./client/README.md)

ユーザー側のクライアントアプリケーション。ローカルディレクトリを監視し、サーバーを介してファイルを同期します。

## 共有するファイル
画像ファイル(1ファイル200kbytes以上10MB以下を想定)