from pathlib import Path
import json


def test_model_exists():
    model_path = Path("artifacts/models/model.pkl")
    assert model_path.exists(), "El modelo no fue generado por el entrenamiento"
    

def test_model_metadata():
    metadata_path = Path("artifacts/models/model_info.json")

    assert metadata_path.exists(), "No existe metadata del modelo"

    with open(metadata_path) as f:
        data = json.load(f)

    assert "metrics" in data
    assert "mae" in data["metrics"]
    assert "rmse" in data["metrics"]