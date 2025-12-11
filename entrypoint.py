import sys
import json
import requests
import pandas as pd
from pathlib import Path


def load_dataset(path: str):
    """Charge le dataset. Tente CSV avec pandas, sinon envoie le texte brut."""
    p = Path(path)
    if not p.exists():
        print(f"❌ Data file not found: {p}")
        sys.exit(1)

    try:
        df = pd.read_csv(p)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"ℹ️ Could not parse with pandas ({e}), sending raw text instead.")
        return p.read_text(encoding="utf-8")


def load_config(path: str | None):
    """Charge un fichier de config JSON optionnel."""
    if not path or path.strip() == "":
        return None

    p = Path(path)
    if not p.exists():
        print(f"⚠️ Config file not found: {p}, ignoring.")
        return None

    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to parse config JSON ({e}), ignoring.")
        return None


def main():
    if len(sys.argv) < 3:
        print("Usage: entrypoint.py <api_key> <data_path> [config_path] [endpoint]")
        sys.exit(1)

    api_key = sys.argv[1]
    data_path = sys.argv[2]
    config_path = sys.argv[3] if len(sys.argv) > 3 else ""
    # Si endpoint vide -> on met la valeur par défaut de l'action
    endpoint = (
        sys.argv[4]
        if len(sys.argv) > 4 and sys.argv[4].strip() != ""
        else "https://api.cim-core.com/analyze"
    )

    print("🚀 Starting CIM-Core Action")
    print(f"  • Data path : {data_path}")
    print(f"  • Endpoint  : {endpoint}")

    data = load_dataset(data_path)
    config = load_config(config_path)

    payload: dict[str, object] = {
        "api_key": api_key,
        "data": data,
    }
    if config is not None:
        payload["config"] = config

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    except Exception as e:
        print(f"❌ HTTP request failed: {e}")
        sys.exit(1)

    if response.status_code != 200:
        print(f"❌ CIM-Core API error ({response.status_code}): {response.text}")
        sys.exit(1)

    # On essaie de parser en JSON
    try:
        report = response.json()
    except Exception:
        print("⚠️ Response is not JSON, raw text below:")
        print(response.text)
        sys.exit(0)

    out_path = Path("cim_report.json")
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"✅ CIM-Core analysis complete. Report saved to {out_path.resolve()}")


if __name__ == "__main__":
    main()
