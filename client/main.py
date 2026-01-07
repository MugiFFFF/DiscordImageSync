"""
DiscordImageSync クライアント
メインエントリポイント
"""
import sys
import os
from config_loader import load_config, ConfigValidationError
from hybrid_converter import convert_to_hybrid
from logger import get_logger


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


def process_images(config):
    """
    client/images内の画像ファイルをHybrid形式に変換してclient/images/outに出力
    
    Args:
        config: 設定オブジェクト
    
    Returns:
        dict: 処理結果の統計情報
    """
    logger = get_logger()
    
    # ディレクトリパス設定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")
    output_dir = os.path.join(images_dir, "out")
    
    # 統計情報
    stats = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # imagesディレクトリが存在しない場合
    if not os.path.exists(images_dir):
        print(f"⚠️  {images_dir} が存在しません")
        return stats
    
    # 画像ファイルを検索
    for root, dirs, files in os.walk(images_dir):
        # outディレクトリは除外
        if "out" in dirs:
            dirs.remove("out")
        
        for filename in files:
            # 拡張子チェック
            _, ext = os.path.splitext(filename)
            if ext.lower() not in config.supported_extensions:
                continue
            
            stats["total"] += 1
            
            # 入力ファイルパス
            input_file = os.path.join(root, filename)
            
            # 出力ファイルパス（相対パス構造を維持）
            rel_path = os.path.relpath(input_file, images_dir)
            output_basename = os.path.splitext(rel_path)[0] + config.data_file_extension
            output_file = os.path.join(output_dir, output_basename)
            
            # 変換処理
            print(f"🔄 変換中: {rel_path}")
            success = convert_to_hybrid(input_file, output_file, images_dir)
            
            if success:
                stats["success"] += 1
                print(f"   ✅ 成功: {output_basename}")
            else:
                stats["failed"] += 1
                print(f"   ❌ 失敗: {rel_path}")
    
    return stats


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
        
        # 画像ファイル変換処理
        print("\n" + "=" * 70)
        print("🖼️  画像ファイル変換処理を開始します")
        print("=" * 70)
        print()
        
        stats = process_images(config)
        
        # 処理結果サマリー
        print()
        print("=" * 70)
        print("📊 処理結果サマリー")
        print("=" * 70)
        print(f"   総ファイル数: {stats['total']}")
        print(f"   成功: {stats['success']}")
        print(f"   失敗: {stats['failed']}")
        print(f"   スキップ: {stats['skipped']}")
        print("=" * 70)
        
        if stats['failed'] > 0:
            print("\n⚠️  エラーの詳細は error.log を確認してください")
        
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
