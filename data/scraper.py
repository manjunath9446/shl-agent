import json
import pandas as pd


INPUT_JSON = "data/shl_product_catalog.json"
OUTPUT_CSV = "data/shl_assessments.csv"


def safe_get(obj, key, default=""):

    value = obj.get(key, default)

    if value is None:
        return default

    return value


def normalize_list(value):

    if isinstance(value, list):

        cleaned = []

        for item in value:

            if isinstance(item, dict):

                if "name" in item:
                    cleaned.append(str(item["name"]))

                elif "value" in item:
                    cleaned.append(str(item["value"]))

                else:
                    cleaned.append(str(item))

            else:
                cleaned.append(str(item))

        return ", ".join(cleaned)

    return str(value)


def extract_test_type(text):

    text = text.lower()

    mapping = {
        "personality": "P",
        "behavior": "P",
        "knowledge": "K",
        "skills": "K",
        "ability": "A",
        "aptitude": "A",
        "simulation": "S",
        "competency": "C"
    }

    for keyword, label in mapping.items():

        if keyword in text:
            return label

    return "Unknown"


def build_row(item):

    name = safe_get(item, "name")

    # IMPORTANT FIX
    url = safe_get(item, "link")

    description = safe_get(
        item,
        "description"
    )

    duration = safe_get(
        item,
        "duration"
    )

    skills = normalize_list(
        item.get("keys", [])
    )

    job_levels = normalize_list(
        item.get("job_levels", [])
    )

    languages = normalize_list(
        item.get("languages", [])
    )

    remote_testing = safe_get(
        item,
        "remote"
    )

    adaptive_irt = safe_get(
        item,
        "adaptive"
    )

    # BETTER TEST TYPE EXTRACTION
    keys_text = skills.lower()

    if "personality" in keys_text:
        test_type = "P"

    elif "knowledge" in keys_text or "skills" in keys_text:
        test_type = "K"

    elif "ability" in keys_text or "aptitude" in keys_text:
        test_type = "A"

    elif "simulation" in keys_text:
        test_type = "S"

    elif "competencies" in keys_text:
        test_type = "C"

    else:
        test_type = "Unknown"

    return {
        "name": name,
        "url": url,
        "description": description,
        "skills": skills,
        "duration": duration,
        "job_levels": job_levels,
        "languages": languages,
        "remote_testing": remote_testing,
        "adaptive_irt": adaptive_irt,
        "test_type": test_type
    }

def scrape_shl():

    print("Loading JSON catalog...")

    with open(INPUT_JSON, "r", encoding="utf-8") as f:

        data = json.load(f)

    # handle multiple possible schemas
    if isinstance(data, dict):

        if "data" in data:
            assessments = data["data"]

        elif "assessments" in data:
            assessments = data["assessments"]

        elif "products" in data:
            assessments = data["products"]

        else:
            assessments = list(data.values())

    else:
        assessments = data

    rows = []
    seen_urls = set()

    print(f"Found {len(assessments)} raw assessments")
    print("\nFIRST ITEM SAMPLE:\n")
    print(json.dumps(assessments[0], indent=2)[:5000])

    for item in assessments:

        try:

            row = build_row(item)

            if not row["url"]:
                continue

            if row["url"] in seen_urls:
                continue

            seen_urls.add(row["url"])

            rows.append(row)

        except Exception as e:

            print(f"Skipping item: {e}")

    df = pd.DataFrame(rows)

    df = df.fillna("")

    df.to_csv(
        OUTPUT_CSV,
        index=False
    )

    print(
        f"Saved {len(df)} assessments to CSV"
    )

    print("\nColumns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    scrape_shl()