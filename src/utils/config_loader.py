import yaml
from pathlib import Path


def load_yaml(path: str) -> dict:
    """
    Load a YAML file and return contents as dict.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_all_configs():
    """
    Load settings.yaml and model_config.yaml together.
    """
    base_dir = Path(__file__).resolve().parents[2]

    settings_path = base_dir / "config" / "settings.yaml"
    model_config_path = base_dir / "config" / "model_config.yaml"

    settings = load_yaml(settings_path)
    model_config = load_yaml(model_config_path)

    return settings, model_config
