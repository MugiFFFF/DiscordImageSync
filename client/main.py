"""
DiscordImageSync クライアント
メインエントリポイント
"""
import sys
from config_loader import load_config, ConfigValidationError


def display_config(config):
    """設定内容をCLIに表示"""
    print("=" * 70)
    print("DiscordImageSync クライアント - 設定情報")
    print("=" * 70)
    print()
    
    # 設定ファイルパス
    print(f"📄 設定ファイル: {config.config_path}")
    print()
    
    # サーバー設定
    print("🌐 [Server] WebSocket接続")
    print(f"   URL: {config.websocket_url}")
    print()
    
    # 同期サーバー設定
    print("🔄 [Sync] サーバー設定")
    enabled_count = sum(1 for s in config.sync_servers.values() if s.enabled)
    print(f"   登録サーバー数: {len(config.sync_servers)} (有効: {enabled_count})")
    print()
    
    for name, sync in config.sync_servers.items():
        status = "✅ 有効" if sync.enabled else "❌ 無効"
        print(f"   [{sync.name}] {status}")
        if sync.enabled:
            print(f"      Server ID:  {sync.server_id}")
            print(f"      Channel ID: {sync.channel_id}")
            print(f"      Local Path: {sync.local_path}")
        print()
    
    # 転送設定
    print("📤 [Transfer] 転送設定")
    print(f"   最大ファイルサイズ:     {config.max_file_size_mb} MB")
    print(f"   送信インターバル:       {config.send_interval_sec} 秒")
    print(f"   アディッショナルタイム: {config.additional_time_sec} 秒")
    print(f"   パケットタイムアウト:   {config.packet_timeout_sec} 秒")
    print()
    
    # ファイル設定
    print("📁 [Files] ファイル設定")
    print(f"   対応拡張子:       {', '.join(config.supported_extensions)}")
    print(f"   転送データ拡張子: {config.data_file_extension}")
    print()
    
    # シャドウディレクトリ設定
    print("👻 [Shadow] シャドウディレクトリ設定")
    print(f"   シャドウディレクトリ: {config.shadow_dir_name}")
    print(f"   テンポラリディレクトリ: {config.temp_dir_name}")
    print(f"   ハッシュディレクトリ: {config.hash_dir_name}")
    print()
    
    print("=" * 70)


def main():
    """メイン処理"""
    try:
        # 設定ファイルの読み込み
        print("設定ファイルを読み込んでいます...")
        config = load_config()
        print("✅ 設定ファイルの読み込みに成功しました")
        print()
        
        # 設定内容の表示
        display_config(config)
        
        # TODO: ここに実際の同期処理を追加
        print("ℹ️  現在はテストモードです。同期処理は未実装です。")
        
    except ConfigValidationError as e:
        print("❌ 設定エラー:", str(e), file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print("❌ ファイルが見つかりません:", str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("❌ 予期しないエラーが発生しました:", str(e), file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
