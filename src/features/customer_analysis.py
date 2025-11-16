#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# Utilities
# =========================
def load_transactions(csv_path: Path) -> pd.DataFrame:
    """
    Load and normalize a transactions CSV.
    Required: 'amount'; Optional: 'date', 'type', 'customer_id'.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path.resolve()}")

    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]

    # Normalize date if present
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

    # Amount cleaning (handles $ and ,)
    if "amount" not in df.columns:
        raise ValueError("Expected an 'amount' column in the CSV.")
    if df["amount"].dtype == object:
        df["amount"] = (
            df["amount"].astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.strip()
        )
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    # Provide defaults if missing
    if "type" not in df.columns:
        df["type"] = "Unknown"
    return df


# =========================
# US-3 — Distribution by transaction type
# =========================
def distribution_by_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group totals and counts by transaction 'type'.
    Returns a sorted DataFrame by total amount (desc).
    """
    summary = (
        df.groupby("type")
          .agg(amount_sum=("amount", "sum"),
               transactions=("amount", "count"))
          .reset_index()
    )
    summary["amount_sum"] = summary["amount_sum"].astype(float).round(2)
    return summary.sort_values("amount_sum", ascending=False)


def plot_distribution_by_type(summary_df: pd.DataFrame,
                              png_path: Path | None = None,
                              show: bool = False) -> None:
    plt.figure(figsize=(10, 5))
    plt.bar(summary_df["type"].astype(str), summary_df["amount_sum"])
    plt.title("US-3: Distribution by Transaction Type")
    plt.xlabel("Transaction Type")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if png_path is not None:
        png_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(png_path, dpi=160)
    if show:
        plt.show()
    plt.close()


# =========================
# US-4 — Top clients by total amount
# =========================
def top_clients(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Top-N clients by total transaction amount.
    Requires a 'customer_id' column.
    """
    if "customer_id" not in df.columns:
        raise ValueError("Top clients requires a 'customer_id' column in the CSV.")

    grouped = (
        df.groupby("customer_id")
          .agg(total_amount=("amount", "sum"),
               transactions=("amount", "count"))
          .reset_index()
    )
    grouped["abs_total"] = grouped["total_amount"].abs()
    out = (
        grouped.sort_values(["abs_total", "total_amount"], ascending=[False, False])
               .head(n)
               .drop(columns=["abs_total"])
               .copy()
    )
    out["total_amount"] = out["total_amount"].astype(float).round(2)
    return out


def plot_top_clients(top_df: pd.DataFrame,
                     png_path: Path | None = None,
                     show: bool = False) -> None:
    plt.figure(figsize=(10, 5))
    plt.bar(top_df["customer_id"].astype(str), top_df["total_amount"])
    plt.title("US-4: Top Clients by Total Amount")
    plt.xlabel("Customer ID")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if png_path is not None:
        png_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(png_path, dpi=160)
    if show:
        plt.show()
    plt.close()


# =========================
# CLI (Notebook-safe)
# =========================
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="US-3/US-4 features: distribution by type & top clients"
    )
    parser.add_argument(
        "--input", "-i",
        default="data/financial_transactions.csv",
        help="Path to transactions CSV (default: ./data/financial_transactions.csv)",
    )
    parser.add_argument(
        "--outdir", "-o",
        default="outputs",
        help="Directory to write outputs (default: ./outputs)",
    )
    parser.add_argument(
        "--n", "-n", type=int, default=10,
        help="Number of top clients for US-4 (default: 10)",
    )
    parser.add_argument(
        "feature",
        nargs="?",
        choices=["type", "clients", "both"],
        default="both",
        help="Which feature to run: type (US-3), clients (US-4), or both (default).",
    )
    args, _ = parser.parse_known_args(argv)

    csv_path = Path(args.input)
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_transactions(csv_path)

    run_both = args.feature == "both"

    # ----- US-3 -----
    if run_both or args.feature == "type":
        us3_table = distribution_by_type(df)
        us3_csv = out_dir / "us3_distribution_by_type.csv"
        us3_png = out_dir / "us3_distribution_by_type.png"
        us3_table.to_csv(us3_csv, index=False)
        plot_distribution_by_type(us3_table, us3_png, show=("ipykernel" in sys.modules))
        print(f"[US-3] Saved table to: {us3_csv}")
        print(f"[US-3] Saved chart to: {us3_png}")

    # ----- US-4 -----
    if run_both or args.feature == "clients":
        us4_table = top_clients(df, n=args.n)
        us4_csv = out_dir / f"us4_top_{args.n}_clients.csv"
        us4_png = out_dir / f"us4_top_{args.n}_clients.png"
        us4_table.to_csv(us4_csv, index=False)
        plot_top_clients(us4_table, us4_png, show=("ipykernel" in sys.modules))
        print(f"[US-4] Saved table to: {us4_csv}")
        print(f"[US-4] Saved chart to: {us4_png}")


if __name__ == "__main__":
    main()
