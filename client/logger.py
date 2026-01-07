"""
エラーログモジュール
永続的なエラーログ（error.log）への記録機能を提供
"""
import os
from datetime import datetime


class ErrorLogger:
    """エラーログ管理クラス"""
    
    def __init__(self, log_file="error.log"):
        """
        Args:
            log_file (str): ログファイルのパス（相対パスまたは絶対パス）
        """
        self.log_file = log_file
        # ログファイルのディレクトリが存在しない場合は作成
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    
    def log_error(self, error_message, target_file=None):
        """
        エラーログをファイルに記録
        
        Args:
            error_message (str): エラーメッセージ
            target_file (str, optional): エラーが発生した対象ファイル
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if target_file:
            log_entry = f"[{timestamp}] {error_message} - 対象: {target_file}\n"
        else:
            log_entry = f"[{timestamp}] {error_message}\n"
        
        try:
            # 追記モードでログファイルに書き込み
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            # ログ記録自体が失敗した場合はコンソールに出力
            print(f"エラーログの記録に失敗しました: {e}")
            print(f"元のエラー: {log_entry.strip()}")
    
    def log_exception(self, exception, target_file=None, context=""):
        """
        例外オブジェクトをログに記録
        
        Args:
            exception (Exception): 例外オブジェクト
            target_file (str, optional): エラーが発生した対象ファイル
            context (str, optional): エラーのコンテキスト情報
        """
        error_msg = f"{context}: {type(exception).__name__} - {str(exception)}" if context else f"{type(exception).__name__} - {str(exception)}"
        self.log_error(error_msg, target_file)


# グローバルインスタンス（シングルトンパターン）
_global_logger = None


def get_logger(log_file="error.log"):
    """
    グローバルなErrorLoggerインスタンスを取得
    
    Args:
        log_file (str): ログファイルのパス
    
    Returns:
        ErrorLogger: エラーロガーインスタンス
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = ErrorLogger(log_file)
    return _global_logger
