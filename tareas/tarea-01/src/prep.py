# src/prep.py
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build weekly store-item dataset from raw Kaggle files.")
    p.add_argument("--raw_dir", type=str, default="data/raw", help="Input dir with raw CSVs")
    p.add_argument("--prep_dir", type=str, default="data/prep", help="Output dir for prepared datasets")
    return p.parse_args()


def load_raw(raw_dir: Path) -> dict[str, pd.DataFrame]:
    files = {
        "sales": raw_dir / "sales_train.csv",
        "test": raw_dir / "test.csv",
        "items": raw_dir / "items_en.csv",
        "shops": raw_dir / "shops_en.csv",
        "cats": raw_dir / "item_categories_en.csv",
        "sample": raw_dir / "sample_submission.csv",
    }
    missing = [k for k, f in files.items() if not f.exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing raw files in {raw_dir.resolve()}: {missing}. "
            "Expected Kaggle Predict Future Sales raw CSVs."
        )

    return {
        "sales": pd.read_csv(files["sales"]),
        "test": pd.read_csv(files["test"]),
        "items": pd.read_csv(files["items"]),
        "shops": pd.read_csv(files["shops"]),
        "cats": pd.read_csv(files["cats"]),
        "sample": pd.read_csv(files["sample"]),
    }


def build_weekly_item_shop(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    sales = data["sales"].copy()
    items = data["items"].copy()
    shops = data["shops"].copy()
    cats = data["cats"].copy()

    # Tu notebook: merge sales + items + shops + cats
    df = (
        sales.merge(items, on="item_id", how="left")
        .merge(shops, on="shop_id", how="left")
        .merge(cats, on="item_category_id", how="left")
    )

    # Tipos / limpieza (igual que notebook)
    df["item_price"] = df["item_price"].astype(float)
    df["item_cnt_day"] = pd.to_numeric(df["item_cnt_day"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y", errors="coerce")
    df = df.dropna(subset=["date", "shop_id", "item_id", "item_cnt_day", "item_price"])

    # Sales = unidades * precio
    df["sales"] = (df["item_cnt_day"] * df["item_price"]).astype(float)

    # Agregación semanal por shop-item
    # Para "week_start" estable, usamos inicio de semana (lunes)
    df["week_start"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)

    weekly = (
        df.groupby(["week_start", "shop_id", "item_id"], as_index=False)
        .agg(
            y_units=("item_cnt_day", "sum"),
            sales=("sales", "sum"),
            avg_price=("item_price", "mean"),
            active_days=("date", lambda s: s.dt.date.nunique()),
        )
        .sort_values(["shop_id", "item_id", "week_start"])
        .reset_index(drop=True)
    )

    # Clip
    weekly["y_units"] = weekly["y_units"].clip(lower=0)

    return weekly


def main() -> None:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    prep_dir = Path(args.prep_dir)
    prep_dir.mkdir(parents=True, exist_ok=True)

    data = load_raw(raw_dir)
    weekly = build_weekly_item_shop(data)

    out_parquet = prep_dir / "weekly_item_shop.parquet"
    out_csv = prep_dir / "weekly_item_shop.csv"

    weekly.to_parquet(out_parquet, index=False)
    weekly.to_csv(out_csv, index=False)

    print(f"[OK] weekly dataset saved:\n- {out_parquet}\n- {out_csv}")
    print(f"[INFO] rows={len(weekly):,} cols={weekly.shape[1]} range={weekly['week_start'].min()} -> {weekly['week_start'].max()}")


if __name__ == "__main__":
    main()
