from pathlib import Path

def test_predictions_exist():
    pred_path = Path("artifacts/predictions/valid_predictions.parquet")
    assert pred_path.exists(), "No existen predicciones generadas"