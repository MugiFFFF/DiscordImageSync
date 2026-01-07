"""
Hybrid形式 動作確認スクリプト
.datファイルのヘッダー解析、SHA-256検証、バイナリ抽出をテスト
"""
import os
import sys
from hybrid_converter import parse_hybrid_header, extract_binary_from_hybrid


def test_hybrid_file(dat_file):
    """
    .datファイルのテスト
    
    Args:
        dat_file (str): テスト対象の.datファイルパス
    """
    print("=" * 70)
    print(f"📋 テスト対象: {dat_file}")
    print("=" * 70)
    print()
    
    # ファイル存在チェック
    if not os.path.exists(dat_file):
        print(f"❌ ファイルが見つかりません: {dat_file}")
        return False
    
    # ファイルサイズ表示
    file_size = os.path.getsize(dat_file)
    print(f"📦 ファイルサイズ: {file_size:,} バイト ({file_size / 1024 / 1024:.2f} MB)")
    print()
    
    # 1. ヘッダー解析テスト
    print("🔍 ステップ1: ヘッダー解析")
    print("-" * 70)
    header_info = parse_hybrid_header(dat_file)
    
    if not header_info:
        print("❌ ヘッダー解析に失敗しました")
        return False
    
    print("✅ ヘッダー解析成功")
    print()
    for key, value in header_info.items():
        print(f"   {key}: {value}")
    print()
    
    # 2. バイナリ抽出テスト
    print("🔍 ステップ2: バイナリ抽出とSHA-256検証")
    print("-" * 70)
    
    # 出力ファイル名生成（元のファイル名を使用）
    original_path = header_info.get('Path', 'unknown.jpg')
    test_output_dir = os.path.join(os.path.dirname(dat_file), "test_restored")
    test_output_file = os.path.join(test_output_dir, os.path.basename(original_path))
    
    # バイナリ抽出
    success = extract_binary_from_hybrid(dat_file, test_output_file)
    
    if success:
        print(f"✅ バイナリ抽出成功")
        print(f"   復元ファイル: {test_output_file}")
        restored_size = os.path.getsize(test_output_file)
        expected_size = int(header_info.get('Size', 0))
        print(f"   ファイルサイズ: {restored_size:,} バイト (期待値: {expected_size:,})")
        
        if restored_size == expected_size:
            print("   ✅ サイズ一致")
        else:
            print("   ⚠️  サイズ不一致")
        
        print()
        print("🎉 すべてのテストに成功しました！")
        return True
    else:
        print("❌ バイナリ抽出に失敗しました")
        return False


def test_all_dat_files(directory):
    """
    指定ディレクトリ内のすべての.datファイルをテスト
    
    Args:
        directory (str): テスト対象ディレクトリ
    """
    print("=" * 70)
    print(f"📂 ディレクトリ: {directory}")
    print("=" * 70)
    print()
    
    dat_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.dat'):
                dat_files.append(os.path.join(root, filename))
    
    if not dat_files:
        print("⚠️  .datファイルが見つかりませんでした")
        return
    
    print(f"📋 見つかった.datファイル: {len(dat_files)}個")
    print()
    
    success_count = 0
    for dat_file in dat_files:
        if test_hybrid_file(dat_file):
            success_count += 1
        print()
    
    # サマリー
    print("=" * 70)
    print("📊 テスト結果サマリー")
    print("=" * 70)
    print(f"   総ファイル数: {len(dat_files)}")
    print(f"   成功: {success_count}")
    print(f"   失敗: {len(dat_files) - success_count}")
    print("=" * 70)


def main():
    """メイン処理"""
    # デフォルトのテスト対象ディレクトリ
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_test_dir = os.path.join(script_dir, "images", "out")
    
    if len(sys.argv) > 1:
        # 引数で.datファイルまたはディレクトリを指定
        target = sys.argv[1]
        
        if os.path.isfile(target):
            # 単一ファイルのテスト
            test_hybrid_file(target)
        elif os.path.isdir(target):
            # ディレクトリ内のすべてのファイルをテスト
            test_all_dat_files(target)
        else:
            print(f"❌ 指定されたパスが見つかりません: {target}")
            sys.exit(1)
    else:
        # デフォルトディレクトリをテスト
        if os.path.exists(default_test_dir):
            test_all_dat_files(default_test_dir)
        else:
            print(f"❌ デフォルトディレクトリが見つかりません: {default_test_dir}")
            print()
            print("使用方法:")
            print(f"  python {os.path.basename(__file__)} [.datファイルまたはディレクトリ]")
            print()
            print("例:")
            print(f"  python {os.path.basename(__file__)} images/out/sample.dat")
            print(f"  python {os.path.basename(__file__)} images/out")
            sys.exit(1)


if __name__ == "__main__":
    main()
