"""
エラー定義モジュール
エラーID（数値）とエラーメッセージ（日本語/英語）の対応を定義
"""

# エラーID : {"ja": 日本語メッセージ, "en": 英語メッセージ} の辞書
ERROR_MESSAGES = {
    1: {
        "ja": "ファイルが見つかりませんでした",
        "en": "File not found"
    },
    2: {
        "ja": "ファイルの読み込みに失敗しました",
        "en": "Failed to read file"
    },
    3: {
        "ja": "ファイルの書き込みができませんでした",
        "en": "Failed to write file"
    },
    4: {
        "ja": "20MBを超えるファイルは共有できません",
        "en": "Files larger than 20MB cannot be shared"
    },
    5: {
        "ja": "1KB以下のファイルは共有できません",
        "en": "Files smaller than 1KB cannot be shared"
    },
    6: {
        "ja": "不正なファイル形式です",
        "en": "Invalid file format"
    },
    7: {
        "ja": "ヘッダー解析に失敗しました",
        "en": "Failed to parse header"
    },
    8: {
        "ja": "SHA-256ハッシュの計算に失敗しました",
        "en": "Failed to calculate SHA-256 hash"
    },
    9: {
        "ja": "バイナリ抽出に失敗しました",
        "en": "Failed to extract binary data"
    },
    10: {
        "ja": "不明なエラーが発生しました",
        "en": "Unknown error occurred"
    },
    11: {
        "ja": "ネットワーク接続に失敗しました",
        "en": "Network connection failed"
    },
    12: {
        "ja": "タイムアウトが発生しました",
        "en": "Timeout occurred"
    },
    13: {
        "ja": "認証に失敗しました",
        "en": "Authentication failed"
    },
    14: {
        "ja": "権限が拒否されました",
        "en": "Permission denied"
    },
    15: {
        "ja": "ディスク容量が不足しています",
        "en": "Insufficient disk space"
    },
    16: {
        "ja": "メモリ不足エラーが発生しました",
        "en": "Out of memory error"
    },
    17: {
        "ja": "無効なパラメータが指定されました",
        "en": "Invalid parameter specified"
    },
    18: {
        "ja": "操作がキャンセルされました",
        "en": "Operation cancelled"
    },
}

# デフォルト言語
DEFAULT_LANGUAGE = "ja"
