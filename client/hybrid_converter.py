"""
Hybrid形式変換モジュール
画像ファイルを200バイト固定長ヘッダーとバイナリ部に分割し、
Discord上での画像プレビューを抑制する.dat形式に変換する
"""
import os
import hashlib
from datetime import datetime
from logger import get_logger


# 定数
HYBRID_HEADER_SIZE = 200  # 固定長ヘッダーサイズ（バイト）
MAX_FILE_SIZE_MB = 10  # 最大ファイルサイズ（MB）
SIZE_MARGIN = 1.02  # サイズマージン（2%）
MIN_FILE_SIZE = HYBRID_HEADER_SIZE  # 最小ファイルサイズ（200バイト）


def calculate_sha256(file_path):
    """
    ファイルのSHA-256ハッシュを計算
    
    Args:
        file_path (str): ハッシュを計算するファイルのパス
    
    Returns:
        str: 64文字の16進数ハッシュ値
    
    Raises:
        Exception: ファイル読み込みエラー
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            # 4KBずつ読み込んでハッシュを更新
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        raise Exception(f"SHA-256計算エラー: {e}")


def validate_file_size(file_path):
    """
    ファイルサイズの妥当性を検証
    - 200バイト未満のファイルを除外
    - 元サイズ × 1.02 が 10MB を超えるファイルを除外
    
    Args:
        file_path (str): 検証するファイルのパス
    
    Returns:
        tuple: (bool, str) - (検証結果, エラーメッセージ)
    """
    try:
        file_size = os.path.getsize(file_path)
        
        # 最小サイズチェック
        if file_size < MIN_FILE_SIZE:
            return False, "規定サイズ以下のファイルは共有されません"
        
        # 最大サイズチェック（2%マージン込み）
        max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size * SIZE_MARGIN > max_size_bytes:
            return False, f"ファイルサイズが上限（{MAX_FILE_SIZE_MB}MB + 2%マージン）を超えています"
        
        return True, ""
    except Exception as e:
        return False, f"ファイルサイズ取得エラー: {e}"


def create_hybrid_header(sha256_hash, relative_path, original_size):
    """
    200バイト固定長のHybridヘッダーを生成
    
    Args:
        sha256_hash (str): SHA-256ハッシュ（64文字）
        relative_path (str): ルートディレクトリからの相対パス
        original_size (int): 元ファイルのサイズ（バイト）
    
    Returns:
        bytes: 200バイト固定長のヘッダー（UTF-8エンコード済み）
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # ヘッダー内容を構築
    header_lines = [
        "HYBRID-HEADER-V1",
        f"SHA256:{sha256_hash}",
        f"Path:{relative_path}",
        f"Size:{original_size}",
        f"Time:{timestamp}",
        f"Offset:{HYBRID_HEADER_SIZE}"
    ]
    
    header_text = "\n".join(header_lines)
    header_bytes = header_text.encode('utf-8')
    
    # 200バイトを超える場合はエラー
    if len(header_bytes) >= HYBRID_HEADER_SIZE:
        raise ValueError(f"ヘッダーサイズが{HYBRID_HEADER_SIZE}バイトを超えました: {len(header_bytes)}バイト")
    
    # 200バイトに満たない場合は null文字でパディング
    # （実際には200バイト未満になることはほぼないが、安全のため）
    padding_size = HYBRID_HEADER_SIZE - len(header_bytes)
    header_bytes += b'\x00' * padding_size
    
    return header_bytes


def convert_to_hybrid(input_file, output_file, root_dir=None):
    """
    画像ファイルをHybrid形式(.dat)に変換
    
    Args:
        input_file (str): 入力画像ファイルのパス
        output_file (str): 出力.datファイルのパス
        root_dir (str, optional): 相対パス計算のルートディレクトリ
    
    Returns:
        bool: 変換成功時True、失敗時False
    """
    logger = get_logger()
    
    try:
        # ファイルサイズ検証
        is_valid, error_msg = validate_file_size(input_file)
        if not is_valid:
            logger.log_error(error_msg, input_file)
            return False
        
        # SHA-256計算
        try:
            sha256_hash = calculate_sha256(input_file)
        except Exception as e:
            logger.log_exception(e, input_file, "SHA-256計算失敗")
            return False
        
        # 相対パス計算
        if root_dir:
            try:
                relative_path = os.path.relpath(input_file, root_dir)
            except Exception as e:
                logger.log_exception(e, input_file, "相対パス計算失敗")
                return False
        else:
            relative_path = os.path.basename(input_file)
        
        # ファイルサイズ取得
        original_size = os.path.getsize(input_file)
        
        # Hybridヘッダー生成
        try:
            header_bytes = create_hybrid_header(sha256_hash, relative_path, original_size)
        except Exception as e:
            logger.log_exception(e, input_file, "Hybridヘッダー生成失敗")
            return False
        
        # バイナリデータ読み込み
        try:
            with open(input_file, 'rb') as f:
                binary_data = f.read()
        except Exception as e:
            logger.log_exception(e, input_file, "ファイル読み込み失敗")
            return False
        
        # Hybrid形式で書き込み（ヘッダー + バイナリ）
        try:
            # 出力ディレクトリが存在しない場合は作成
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            with open(output_file, 'wb') as f:
                f.write(header_bytes)
                f.write(binary_data)
        except Exception as e:
            logger.log_exception(e, output_file, "ファイル書き込み失敗")
            return False
        
        return True
        
    except Exception as e:
        logger.log_exception(e, input_file, "Hybrid変換中の予期しないエラー")
        return False


def parse_hybrid_header(dat_file):
    """
    .datファイルからHybridヘッダーを解析
    
    Args:
        dat_file (str): .datファイルのパス
    
    Returns:
        dict: ヘッダー情報の辞書、エラー時はNone
    """
    logger = get_logger()
    
    try:
        with open(dat_file, 'rb') as f:
            # 200バイトのヘッダー部を読み込み
            header_bytes = f.read(HYBRID_HEADER_SIZE)
            
            if len(header_bytes) < HYBRID_HEADER_SIZE:
                logger.log_error("ヘッダーサイズが不正です", dat_file)
                return None
            
            # null文字を除去してデコード
            header_text = header_bytes.rstrip(b'\x00').decode('utf-8')
            
            # ヘッダー情報をパース
            header_info = {}
            for line in header_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    header_info[key.strip()] = value.strip()
            
            return header_info
            
    except Exception as e:
        logger.log_exception(e, dat_file, "Hybridヘッダー解析失敗")
        return None


def extract_binary_from_hybrid(dat_file, output_file):
    """
    .datファイルからバイナリ部を抽出して元の画像ファイルに復元
    
    Args:
        dat_file (str): .datファイルのパス
        output_file (str): 復元する画像ファイルのパス
    
    Returns:
        bool: 復元成功時True、失敗時False
    """
    logger = get_logger()
    
    try:
        # ヘッダー解析
        header_info = parse_hybrid_header(dat_file)
        if not header_info:
            return False
        
        # バイナリ部を読み込み
        with open(dat_file, 'rb') as f:
            # ヘッダー部をスキップ
            f.seek(HYBRID_HEADER_SIZE)
            binary_data = f.read()
        
        # SHA-256検証
        sha256_hash = hashlib.sha256(binary_data).hexdigest()
        expected_hash = header_info.get('SHA256', '')
        
        if sha256_hash != expected_hash:
            logger.log_error(
                f"SHA-256ハッシュ不一致: 期待値={expected_hash}, 実際={sha256_hash}",
                dat_file
            )
            return False
        
        # 出力ディレクトリが存在しない場合は作成
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # バイナリデータを書き込み
        with open(output_file, 'wb') as f:
            f.write(binary_data)
        
        return True
        
    except Exception as e:
        logger.log_exception(e, dat_file, "バイナリ抽出失敗")
        return False
