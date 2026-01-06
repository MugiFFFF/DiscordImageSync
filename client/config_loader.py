"""
設定ファイル（INI形式）の読み込みと検証を行うモジュール
"""
import configparser
import os
from pathlib import Path
from typing import Dict, List, Optional


class ConfigValidationError(Exception):
    """設定ファイルの検証エラー"""
    pass


class SyncServerConfig:
    """個別サーバーの同期設定"""
    
    def __init__(self, name: str, section: configparser.SectionProxy):
        self.name = name
        self.enabled = section.getboolean('enabled', fallback=False)
        self.server_id = section.get('server_id', '')
        self.channel_id = section.get('channel_id', '')
        self.local_path = section.get('local_path', '')
        
        # 検証
        if self.enabled:
            if not self.server_id:
                raise ConfigValidationError(f"[{name}]: server_id が設定されていません")
            if not self.channel_id:
                raise ConfigValidationError(f"[{name}]: channel_id が設定されていません")
            if not self.local_path:
                raise ConfigValidationError(f"[{name}]: local_path が設定されていません")


class Config:
    """アプリケーション設定を保持するクラス"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        
        # 設定ファイルの読み込み
        if not os.path.exists(config_path):
            raise ConfigValidationError(f"設定ファイルが見つかりません: {config_path}")
        
        self.config.read(config_path, encoding='utf-8')
        
        # 各セクションの読み込みと検証
        self._load_server_config()
        self._load_sync_configs()
        self._load_transfer_config()
        self._load_files_config()
        self._load_shadow_config()
        
        # 有効なサーバー設定が1つ以上あるか確認
        if not any(sync.enabled for sync in self.sync_servers.values()):
            raise ConfigValidationError("有効なサーバー設定が1つもありません")
    
    def _load_server_config(self):
        """[Server] セクションの読み込み"""
        if 'Server' not in self.config:
            raise ConfigValidationError("[Server] セクションが見つかりません")
        
        self.websocket_url = self.config['Server'].get('websocket_url', '')
        if not self.websocket_url:
            raise ConfigValidationError("[Server]: websocket_url が設定されていません")
    
    def _load_sync_configs(self):
        """[Sync.*] セクションの読み込み"""
        self.sync_servers: Dict[str, SyncServerConfig] = {}
        
        for section_name in self.config.sections():
            if section_name.startswith('Sync.'):
                server_name = section_name[5:]  # "Sync." を除去
                self.sync_servers[server_name] = SyncServerConfig(
                    section_name, self.config[section_name]
                )
        
        if not self.sync_servers:
            raise ConfigValidationError("[Sync.*] セクションが1つも見つかりません")
    
    def _load_transfer_config(self):
        """[Transfer] セクションの読み込み"""
        if 'Transfer' not in self.config:
            raise ConfigValidationError("[Transfer] セクションが見つかりません")
        
        transfer = self.config['Transfer']
        self.max_file_size_mb = transfer.getint('max_file_size_mb', fallback=10)
        self.send_interval_sec = transfer.getint('send_interval_sec', fallback=30)
        self.additional_time_sec = transfer.getint('additional_time_sec', fallback=15)
        self.packet_timeout_sec = transfer.getint('packet_timeout_sec', fallback=300)
        
        # 妥当性チェック
        if self.max_file_size_mb <= 0:
            raise ConfigValidationError("[Transfer]: max_file_size_mb は正の整数である必要があります")
        if self.send_interval_sec < 0:
            raise ConfigValidationError("[Transfer]: send_interval_sec は0以上である必要があります")
        if self.additional_time_sec < 0:
            raise ConfigValidationError("[Transfer]: additional_time_sec は0以上である必要があります")
        if self.packet_timeout_sec <= 0:
            raise ConfigValidationError("[Transfer]: packet_timeout_sec は正の整数である必要があります")
    
    def _load_files_config(self):
        """[Files] セクションの読み込み"""
        if 'Files' not in self.config:
            raise ConfigValidationError("[Files] セクションが見つかりません")
        
        files = self.config['Files']
        extensions_str = files.get('supported_extensions', '.jpg,.jpeg,.png,.webp')
        self.supported_extensions: List[str] = [
            ext.strip() for ext in extensions_str.split(',')
        ]
        self.data_file_extension = files.get('data_file_extension', '.dat')
        
        if not self.supported_extensions:
            raise ConfigValidationError("[Files]: supported_extensions が空です")
        if not self.data_file_extension:
            raise ConfigValidationError("[Files]: data_file_extension が設定されていません")
    
    def _load_shadow_config(self):
        """[Shadow] セクションの読み込み"""
        if 'Shadow' not in self.config:
            raise ConfigValidationError("[Shadow] セクションが見つかりません")
        
        shadow = self.config['Shadow']
        self.shadow_dir_name = shadow.get('shadow_dir_name', '.shadow')
        self.temp_dir_name = shadow.get('temp_dir_name', 'temp')
        self.hash_dir_name = shadow.get('hash_dir_name', 'hashes')
        
        if not self.shadow_dir_name:
            raise ConfigValidationError("[Shadow]: shadow_dir_name が空です")
        if not self.temp_dir_name:
            raise ConfigValidationError("[Shadow]: temp_dir_name が空です")
        if not self.hash_dir_name:
            raise ConfigValidationError("[Shadow]: hash_dir_name が空です")
    
    def get_enabled_servers(self) -> Dict[str, SyncServerConfig]:
        """有効なサーバー設定のみを返す"""
        return {
            name: config for name, config in self.sync_servers.items()
            if config.enabled
        }


def find_config_file() -> str:
    """
    設定ファイルのパスを特定する
    
    1. path.ini が存在する場合、そこに記載されたパスを使用
    2. 存在しない場合、デフォルトの config.ini を使用
    
    Returns:
        設定ファイルの絶対パス
    """
    client_dir = Path(__file__).parent
    path_ini = client_dir / 'path.ini'
    
    # path.ini が存在する場合
    if path_ini.exists():
        path_config = configparser.ConfigParser()
        path_config.read(path_ini, encoding='utf-8')
        
        if 'Path' not in path_config:
            raise ConfigValidationError("path.ini に [Path] セクションがありません")
        
        config_file = path_config['Path'].get('config_file', '')
        if not config_file:
            raise ConfigValidationError("path.ini の [Path] セクションに config_file が設定されていません")
        
        # 相対パスの場合は client ディレクトリからの相対パスとして解決
        config_path = Path(config_file)
        if not config_path.is_absolute():
            config_path = client_dir / config_path
        
        return str(config_path.resolve())
    
    # デフォルトの config.ini
    default_config = client_dir / 'config.ini'
    return str(default_config.resolve())


def load_config() -> Config:
    """
    設定ファイルを読み込む
    
    Returns:
        Config オブジェクト
    
    Raises:
        ConfigValidationError: 設定ファイルの読み込みまたは検証に失敗した場合
    """
    config_path = find_config_file()
    return Config(config_path)
