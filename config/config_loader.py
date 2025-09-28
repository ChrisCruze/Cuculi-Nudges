"""Universal configuration loader for the Cuculi AI Nudge Notification System."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml


class ConfigurationLoader:
    """Load YAML configuration files with environment-aware overrides."""

    def __init__(self, config_dir: str = "config") -> None:
        self.config_dir = Path(config_dir)
        self._cache: Dict[str, Dict[str, Any]] = {}

    def load_config(self, config_name: str, environment: str | None = None) -> Dict[str, Any]:
        """Load configuration with optional environment overrides."""
        cache_key = f"{config_name}_{environment}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        base_config = self._load_yaml_file(f"{config_name}.yaml")

        if environment:
            env_file = self.config_dir / "environments" / f"{environment}.yaml"
            if env_file.exists():
                env_overrides = self._load_yaml_file(str(env_file.relative_to(self.config_dir)))
                base_config = self._merge_configs(base_config, env_overrides)

        base_config = self._substitute_env_vars(base_config)

        self._cache[cache_key] = base_config
        return base_config

    def reload_config(self, config_name: str, environment: str | None = None) -> Dict[str, Any]:
        """Force reload configuration (useful for updates)."""
        cache_key = f"{config_name}_{environment}"
        if cache_key in self._cache:
            del self._cache[cache_key]
        return self.load_config(config_name, environment)

    def _load_yaml_file(self, filename: str) -> Dict[str, Any]:
        """Load YAML file with error handling."""
        file_path = self.config_dir / filename
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Configuration file not found: {file_path}") from exc
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML in {file_path}: {exc}") from exc

    def _substitute_env_vars(self, config: Any) -> Any:
        """Recursively substitute environment variables."""
        if isinstance(config, dict):
            return {key: self._substitute_env_vars(value) for key, value in config.items()}
        if isinstance(config, list):
            return [self._substitute_env_vars(item) for item in config]
        if isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            env_var = config[2:-1]
            return os.getenv(env_var, config)
        return config

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge configuration dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result


config_loader = ConfigurationLoader()
