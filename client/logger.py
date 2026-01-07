"""
エラーログモジュール
永続的なエラーログ（error.log）への記録機能を提供
"""
import os
from datetime import datetime
from error_def import ERROR_MESSAGES, DEFAULT_LANGUAGE


class ErrorLogger:
    """エラーログ管理クラス"""
    
    def __init__(self, log_file="error.log", language="ja"):
        """
        Args:
            log_file (str): ログファイルのパス（相対パスまたは絶対パス）
            language (str): ログメッセージの言語 ("ja" または "en")
        """
        self.log_file = log_file
        self.language = language
        # ログファイルのディレクトリが存在しない場合は作成
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    
    def log_error(self, error_id, target_file=None, additional_info=None):
        """
        エラーログをファイルに記録
        
        Args:
            error_id (int): エラーID（error_def.pyで定義）
            target_file (str, optional): エラーが発生した対象ファイル
            additional_info (str, optional): 追加情報
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # エラーIDからメッセージを取得
        error_def = ERROR_MESSAGES.get(error_id)
        if error_def:
            # 指定言語のメッセージを取得（存在しない場合はデフォルト言語）
            error_message = error_def.get(self.language) or error_def.get(DEFAULT_LANGUAGE)
        else:
            # 未定義のエラーID
            if self.language == "en":
                error_message = f"Undefined error (ID: {error_id})"
            else:
                error_message = f"未定義のエラー (ID: {error_id})"
        
        # ログエントリを構築
        log_parts = [f"[{timestamp}]", f"[ID:{error_id}]", error_message]
        
        if target_file:
            if self.language == "en":
                log_parts.append(f"- Target: {target_file}")
            else:
                log_parts.append(f"- 対象: {target_file}")
        
        if additional_info:
            if self.language == "en":
                log_parts.append(f"- Details: {additional_info}")
            else:
                log_parts.append(f"- 詳細: {additional_info}")
        
        log_entry = " ".join(log_parts) + "\n"
        
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 例外情報を構築
        exception_info = f"{type(exception).__name__}: {str(exception)}"
        
        # ログエントリを構築
        log_parts = [f"[{timestamp}]", "[EXCEPTION]"]
        
        if context:
            log_parts.append(f"{context} -")
        
        log_parts.append(exception_info)
        
        if target_file:
            if self.language == "en":
                log_parts.append(f"- Target: {target_file}")
            else:
                log_parts.append(f"- 対象: {target_file}")
        
        log_entry = " ".join(log_parts) + "\n"
        
        try:
            # 追記モードでログファイルに書き込み
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            # ログ記録自体が失敗した場合はコンソールに出力
            print(f"エラーログの記録に失敗しました: {e}")
            print(f"元のエラー: {log_entry.strip()}")


# グローバルインスタンス（シングルトンパターン）
_global_logger = None


def get_logger(log_file="error.log", language="ja"):
    """
    グローバルなErrorLoggerインスタンスを取得
    
    Args:
        log_file (str): ログファイルのパス
        language (str): ログメッセージの言語 ("ja" または "en")
    
    Returns:
        ErrorLogger: エラーロガーインスタンス
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = ErrorLogger(log_file, language)
    return _global_logger

