"""
Python Automation - Advanced Utilities
Extended automation functions for common tasks
"""

import os
import json
import yaml
import logging
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)


class FileWatcher:
    """Monitor files for changes"""
    
    def __init__(self, watch_paths: List[str], callback):
        self.watch_paths = watch_paths
        self.callback = callback
        self.file_hashes = {}
        self._scan_files()
    
    def _scan_files(self):
        """Initial file scan"""
        for path in self.watch_paths:
            path_obj = Path(path)
            if path_obj.is_file():
                self.file_hashes[str(path_obj)] = self._get_file_hash(path)
            elif path_obj.is_dir():
                for file in path_obj.rglob('*'):
                    if file.is_file():
                        self.file_hashes[str(file)] = self._get_file_hash(str(file))
    
    def _get_file_hash(self, filepath: str) -> str:
        """Calculate file hash"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    
    def check_changes(self) -> List[str]:
        """Check for file changes"""
        changed_files = []
        
        current_files = {}
        
        for path in self.watch_paths:
            path_obj = Path(path)
            if path_obj.is_file():
                current_files[str(path_obj)] = self._get_file_hash(path)
            elif path_obj.is_dir():
                for file in path_obj.rglob('*'):
                    if file.is_file():
                        current_files[str(file)] = self._get_file_hash(str(file))
        
        # Check for new or modified files
        for filepath, hash_value in current_files.items():
            if filepath not in self.file_hashes:
                changed_files.append(f"NEW: {filepath}")
            elif self.file_hashes[filepath] != hash_value:
                changed_files.append(f"MODIFIED: {filepath}")
        
        # Check for deleted files
        for filepath in self.file_hashes:
            if filepath not in current_files:
                changed_files.append(f"DELETED: {filepath}")
        
        self.file_hashes = current_files
        
        return changed_files
    
    def watch(self, interval: int = 60):
        """Start watching for changes"""
        while True:
            changes = self.check_changes()
            if changes:
                for change in changes:
                    logger.info(f"File change detected: {change}")
                    self.callback(changes)
            
            time.sleep(interval)


class TaskScheduler:
    """Advanced task scheduling"""
    
    def __init__(self):
        self.tasks = []
    
    def add_task(self, func, schedule_info: str, task_name: Optional[str] = None):
        """Add a scheduled task"""
        task = {
            'name': task_name or func.__name__,
            'func': func,
            'schedule': schedule_info
        }
        self.tasks.append(task)
        
        # Register with schedule library
        if schedule_info == 'daily':
            schedule.every().day.do(func)
        elif schedule_info == 'hourly':
            schedule.every().hour.do(func)
        elif schedule_info == 'minutes':
            schedule.every(10).minutes.do(func)
        elif schedule_info.startswith('every '):
            # Parse "every X minutes/hours"
            parts = schedule_info.split()
            if len(parts) >= 3:
                amount = int(parts[1])
                unit = parts[2]
                
                if 'minute' in unit:
                    schedule.every(amount).minutes.do(func)
                elif 'hour' in unit:
                    schedule.every(amount).hours.do(func)
                elif 'day' in unit:
                    schedule.every(amount).days.do(func)
        
        logger.info(f"Task scheduled: {task['name']} ({schedule_info})")
    
    def run_pending(self):
        """Run pending tasks"""
        schedule.run_pending()
    
    def run_continuously(self, interval: int = 60):
        """Run scheduler continuously"""
        logger.info("Scheduler started")
        while True:
            self.run_pending()
            time.sleep(interval)


class DataProcessor:
    """Data processing utilities"""
    
    @staticmethod
    def batch_process(items: List[Any], batch_size: int = 100):
        """Process items in batches"""
        for i in range(0, len(items), batch_size):
            yield items[i:i + batch_size]
    
    @staticmethod
    def deduplicate(items: List[Any], key=None) -> List[Any]:
        """Remove duplicates while preserving order"""
        seen = set()
        result = []
        
        for item in items:
            lookup_key = key(item) if key else item
            
            if lookup_key not in seen:
                seen.add(lookup_key)
                result.append(item)
        
        return result
    
    @staticmethod
    def filter_by_date(items: List[Dict], date_field: str, 
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> List[Dict]:
        """Filter items by date range"""
        result = []
        
        for item in items:
            if date_field not in item:
                continue
            
            item_date = item[date_field]
            
            if isinstance(item_date, str):
                item_date = datetime.fromisoformat(item_date.replace('Z', '+00:00'))
            
            if start_date and item_date < start_date:
                continue
            
            if end_date and item_date > end_date:
                continue
            
            result.append(item)
        
        return result


class JSONLHandler:
    """Handle JSON Lines files"""
    
    @staticmethod
    def read(filepath: str) -> List[Dict]:
        """Read JSONL file"""
        items = []
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
        
        return items
    
    @staticmethod
    def write(filepath: str, items: List[Dict]):
        """Write to JSONL file"""
        with open(filepath, 'w') as f:
            for item in items:
                f.write(json.dumps(item) + '\n')
    
    @staticmethod
    def append(filepath: str, item: Dict):
        """Append single item to JSONL file"""
        with open(filepath, 'a') as f:
            f.write(json.dumps(item) + '\n')


# Export commonly used functions
__all__ = [
    'ConfigManager',
    'FileWatcher',
    'TaskScheduler',
    'DataProcessor',
    'JSONLHandler'
]
