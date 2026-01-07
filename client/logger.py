"""
エラーログモジュール
永続的なエラーログ（error.log）への記録機能を提供
"""
import os
import configparser
from datetime import datetime
from error_def import ERROR_MESSAGES, DEFAULT_LANGUAGE


def _get_language_from_config():
    """
    config.iniから言語設定を取得
    
    Returns:
        str: 言語コード ("ja" または "en")
    """
    try:
        config_path = os.path.join(os.path.dirname(__file__), "config.ini")
        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path, encoding='utf-8')
            if 'General' in config and 'language' in config['General']:
                lang = config['General']['language'].lower()
                # jaまたはenのみ許可、それ以外はデフォルト
                return lang if lang in ['ja', 'en'] else DEFAULT_LANGUAGE
    except Exception:
        # 設定ファイル読み込みエラーの場合はデフォルト言語を使用
        pass
    
    return DEFAULT_LANGUAGE


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
    
    def log_error(self, error_id, target_file=None, additional_info=None):
        """
        エラーログをファイルに記録
        
        Args:
            error_id (int): エラーID（error_def.pyで定義）
            target_file (str, optional): エラーが発生した対象ファイル
            additional_info (str, optional): 追加情報
        """
        # config.iniから言語設定を取得
        language = _get_language_from_config()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # エラーIDからメッセージを取得
        error_def = ERROR_MESSAGES.get(error_id)
        if error_def:
            # 指定言語のメッセージを取得（存在しない場合はデフォルト言語）
            error_message = error_def.get(language) or error_def.get(DEFAULT_LANGUAGE)
        else:
            # 未定義のエラーID
            if language == "en":
                error_message = f"Undefined error (ID: {error_id})"
            else:
                error_message = f"未定義のエラー (ID: {error_id})"
        
        # ログエントリを構築
        log_parts = [f"[{timestamp}]", f"[ID:{error_id}]", error_message]
        
        if target_file:
            if language == "en":
                log_parts.append(f"- Target: {target_file}")
            else:
                log_parts.append(f"- 対象: {target_file}")
        
        if additional_info:
            if language == "en":
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
        # config.iniから言語設定を取得
        language = _get_language_from_config()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 例外情報を構築
        exception_info = f"{type(exception).__name__}: {str(exception)}"
        
        # ログエントリを構築
        log_parts = [f"[{timestamp}]", "[EXCEPTION]"]
        
        if context:
            log_parts.append(f"{context} -")
        
        log_parts.append(exception_info)
        
        if target_file:
            if language == "en":
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

