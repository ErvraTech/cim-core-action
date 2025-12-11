import sys
import json
import requests
import pandas as pd

def main():
    api_key = sys.argv[1]
    data_path = sys.argv[2]
    config_path = sys.argv[3] if len(sys.argv) > 3 else None
    endpoint = sys.argv[4] if len(sys.argv) > 4 else None

    # Load dataset
    try:
        df = pd.read_csv(data_path)
    except:
        with open(data_path, "r") as f:
            df = f.read()

    payload = {
        "api_key": api_key,
        "data": df if isinstance(df, dict) else df.to_dict(),
    }

    if config_path:
        with open(config_path, "r") as f:
            payload["config"] = f.read()

    response = requests.post(endpoint, json=payload)

    if response.status_code != 200:
        print("❌ CIM-Core API Error:", response.text)
        sys.exit(1)

    report = response.json()

    # Save output report
    with open("cim_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("✅ CIM-Core analysis complete.")
    print("Report saved to cim_report.json")

if __name__ == "__main__":
    main()
