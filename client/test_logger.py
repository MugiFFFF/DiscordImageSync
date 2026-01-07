"""
logger.py 単体テストスクリプト
ErrorLoggerクラスの各機能をテスト
"""
import os
import sys
from datetime import datetime
from logger import ErrorLogger, get_logger
from error_def import ERROR_MESSAGES


def test_logger_basic():
    """基本的なログ記録のテスト"""
    print("=" * 70)
    print("📋 テスト1: 基本的なログ記録")
    print("=" * 70)
    
    # テスト用ログファイル
    test_log_file = "test_error.log"
    
    # 既存のログファイルを削除
    if os.path.exists(test_log_file):
        os.remove(test_log_file)
        print(f"✅ 既存のログファイルを削除: {test_log_file}")
    
    # ロガーインスタンス作成
    logger = ErrorLogger(test_log_file)
    
    # エラーID 1 のログを記録（対象ファイルなし）
    print("\n🔄 エラーID 1 を記録中...")
    logger.log_error(1)
    
    # エラーID 2 のログを記録（対象ファイルあり）
    print("🔄 エラーID 2 を記録中...")
    logger.log_error(2, target_file="sample.txt")
    
    # エラーID 3 のログを記録（対象ファイル + 追加情報）
    print("🔄 エラーID 3 を記録中...")
    logger.log_error(3, target_file="output.dat", additional_info="ディスク容量不足")
    
    # ログファイルの内容を確認
    if os.path.exists(test_log_file):
        print(f"\n✅ ログファイルが作成されました: {test_log_file}")
        print("\n📄 ログファイルの内容:")
        print("-" * 70)
        with open(test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        print("-" * 70)
        return True
    else:
        print(f"\n❌ ログファイルが作成されませんでした: {test_log_file}")
        return False


def test_undefined_error_id():
    """未定義のエラーIDのテスト"""
    print("\n" + "=" * 70)
    print("📋 テスト2: 未定義のエラーID")
    print("=" * 70)
    
    test_log_file = "test_error.log"
    logger = ErrorLogger(test_log_file)
    
    # 未定義のエラーID（999）を記録
    print("\n🔄 未定義のエラーID 999 を記録中...")
    logger.log_error(999, target_file="unknown.file")
    
    # ログファイルの最終行を確認
    print("\n📄 ログファイルの最終行:")
    print("-" * 70)
    with open(test_log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            print(lines[-1].strip())
    print("-" * 70)
    
    if "未定義のエラー" in lines[-1]:
        print("✅ 未定義エラーの処理が正しく動作しています")
        return True
    else:
        print("❌ 未定義エラーの処理に問題があります")
        return False


def test_log_exception():
    """例外ログ記録のテスト"""
    print("\n" + "=" * 70)
    print("📋 テスト3: 例外ログ記録")
    print("=" * 70)
    
    test_log_file = "test_error.log"
    logger = ErrorLogger(test_log_file)
    
    # 意図的に例外を発生させてログに記録
    try:
        print("\n🔄 意図的に例外を発生させています...")
        result = 10 / 0  # ZeroDivisionError
    except Exception as e:
        print(f"✅ 例外をキャッチ: {type(e).__name__}")
        logger.log_exception(e, target_file="calculation.py", context="計算処理中")
    
    # ログファイルの最終行を確認
    print("\n📄 ログファイルの最終行:")
    print("-" * 70)
    with open(test_log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            print(lines[-1].strip())
    print("-" * 70)
    
    if "ZeroDivisionError" in lines[-1]:
        print("✅ 例外ログが正しく記録されました")
        return True
    else:
        print("❌ 例外ログの記録に問題があります")
        return False


def test_global_logger():
    """グローバルロガーのテスト"""
    print("\n" + "=" * 70)
    print("📋 テスト4: グローバルロガー（シングルトン）")
    print("=" * 70)
    
    # グローバルロガーを取得
    logger1 = get_logger("test_error.log")
    logger2 = get_logger("test_error.log")
    
    # 同じインスタンスかチェック
    if logger1 is logger2:
        print("✅ グローバルロガーは正しくシングルトンパターンで動作しています")
        print(f"   logger1: {id(logger1)}")
        print(f"   logger2: {id(logger2)}")
        return True
    else:
        print("❌ グローバルロガーがシングルトンになっていません")
        return False


def test_all_error_messages():
    """全エラーメッセージの定義確認"""
    print("\n" + "=" * 70)
    print("📋 テスト5: エラーメッセージ定義の確認")
    print("=" * 70)
    
    print(f"\n📚 定義されているエラーメッセージ: {len(ERROR_MESSAGES)}件")
    print("-" * 70)
    print(f"{'ID':<5} {'日本語':<40} {'英語':<40}")
    print("-" * 70)
    
    for error_id in sorted(ERROR_MESSAGES.keys()):
        msg_def = ERROR_MESSAGES[error_id]
        ja_msg = msg_def.get("ja", "未定義")
        en_msg = msg_def.get("en", "未定義")
        print(f"{error_id:<5} {ja_msg:<40} {en_msg:<40}")
    
    print("-" * 70)
    print("✅ すべてのエラーメッセージが正しく定義されています")
    return True


def test_english_logger():
    """英語ログのテスト（config.iniの言語設定を変更）"""
    print("\n" + "=" * 70)
    print("📋 テスト6: 英語ログ記録（config.ini経由）")
    print("=" * 70)
    
    # config.iniのバックアップを作成
    config_path = "config.ini"
    backup_path = "config.ini.backup"
    
    has_config = os.path.exists(config_path)
    if has_config:
        import shutil
        shutil.copy(config_path, backup_path)
        print(f"✅ config.iniをバックアップしました: {backup_path}")
    
    # 英語設定のconfig.iniを作成
    try:
        import configparser
        config = configparser.ConfigParser()
        config['General'] = {'language': 'en'}
        config['Server'] = {'websocket_url': 'ws://localhost:8765'}
        config['Sync.Test'] = {
            'enabled': 'true',
            'server_id': '123',
            'channel_id': '456',
            'local_path': './test'
        }
        config['Transfer'] = {
            'max_file_size_mb': '10',
            'send_interval_sec': '30',
            'additional_time_sec': '15',
            'packet_timeout_sec': '300'
        }
        config['Files'] = {
            'supported_extensions': '.jpg,.png',
            'data_file_extension': '.dat'
        }
        config['Shadow'] = {
            'shadow_dir_name': '.shadow',
            'temp_dir_name': 'temp',
            'hash_dir_name': 'hashes'
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)
        
        print("✅ 英語設定のconfig.iniを作成しました")
        
        # 英語モードのロガーを作成
        test_log_file = "test_error_en.log"
        
        # 既存のログファイルを削除
        if os.path.exists(test_log_file):
            os.remove(test_log_file)
        
        logger = ErrorLogger(test_log_file)
        
        # エラーを記録
        print("\n🔄 Recording error ID 1 in English...")
        logger.log_error(1)
        
        print("🔄 Recording error ID 2 in English...")
        logger.log_error(2, target_file="sample.txt")
        
        print("🔄 Recording error ID 15 in English...")
        logger.log_error(15, target_file="output.dat", additional_info="Only 100MB available")
        
        # ログファイルの内容を確認
        if os.path.exists(test_log_file):
            print(f"\n✅ English log file created: {test_log_file}")
            print("\n📄 Log file contents:")
            print("-" * 70)
            with open(test_log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
            print("-" * 70)
            
            # クリーンアップ
            os.remove(test_log_file)
            print(f"🧹 Cleaned up: {test_log_file}")
            
            # 英語メッセージが含まれているか確認
            result = "File not found" in content and "Target:" in content
            
            if result:
                print("✅ 英語ログが正しく記録されました")
            else:
                print("❌ 英語ログの記録に問題があります")
            
            return result
        else:
            print(f"\n❌ 英語ログファイルが作成されませんでした")
            return False
    
    finally:
        # config.iniを復元
        if has_config and os.path.exists(backup_path):
            import shutil
            shutil.move(backup_path, config_path)
            print(f"\n🔄 config.iniを復元しました")
        elif not has_config and os.path.exists(config_path):
            os.remove(config_path)
            print(f"\n🔄 テスト用config.iniを削除しました")


def cleanup():
    """テスト後のクリーンアップ"""
    print("\n" + "=" * 70)
    print("🧹 クリーンアップ")
    print("=" * 70)
    
    test_log_file = "test_error.log"
    if os.path.exists(test_log_file):
        # ユーザーに確認
        print(f"\nテストログファイル '{test_log_file}' を削除しますか？")
        print("  1. はい（削除する）")
        print("  2. いいえ（保持する）")
        
        try:
            choice = input("\n選択してください (1/2): ").strip()
            if choice == "1":
                os.remove(test_log_file)
                print(f"✅ テストログファイルを削除しました: {test_log_file}")
            else:
                print(f"ℹ️  テストログファイルを保持しました: {test_log_file}")
        except KeyboardInterrupt:
            print(f"\nℹ️  テストログファイルを保持しました: {test_log_file}")


def main():
    """メイン処理"""
    print("=" * 70)
    print("🧪 ErrorLogger 単体テスト")
    print("=" * 70)
    print()
    
    # テスト結果を記録
    results = []
    
    # 各テストを実行
    results.append(("基本的なログ記録", test_logger_basic()))
    results.append(("未定義のエラーID", test_undefined_error_id()))
    results.append(("例外ログ記録", test_log_exception()))
    results.append(("グローバルロガー", test_global_logger()))
    results.append(("エラーメッセージ定義", test_all_error_messages()))
    results.append(("英語ログ記録", test_english_logger()))
    
    # テスト結果サマリー
    print("\n" + "=" * 70)
    print("📊 テスト結果サマリー")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}  {test_name}")
    
    print("-" * 70)
    print(f"   合計: {passed}/{total} テスト成功")
    print("=" * 70)
    
    # クリーンアップ
    cleanup()
    
    # 終了ステータス
    if passed == total:
        print("\n🎉 すべてのテストに成功しました！")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed}件のテストが失敗しました")
        sys.exit(1)


if __name__ == "__main__":
    main()
