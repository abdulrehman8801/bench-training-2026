import os
import sys
import urllib.request
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

def ensure_dataset(csv_path: str) -> None:
    if os.path.exists(csv_path):
        return

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    try:
        with urllib.request.urlopen(DATA_URL, timeout=30) as resp:
            data = resp.read()
        with open(csv_path, "wb") as f:
            f.write(data)
    except Exception as exc:
        raise RuntimeError(f"Failed to download titanic.csv: {exc}") from exc

def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "titanic.csv")

    try:
        ensure_dataset(csv_path)
        df = pd.read_csv(csv_path)
    except Exception as exc:
        print(f"Error: could not load Titanic dataset: {exc}", file=sys.stderr)
        sys.exit(1)

    required_columns = {"Survived", "Pclass", "Age", "Embarked", "Name", "Sex", "Cabin"}
    missing = required_columns - set(df.columns)
    if missing:
        print(f"Error: dataset is missing required columns: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded Titanic dataset from {csv_path} (rows={len(df)}).")
    print()

    # 01. How many passengers survived vs. didn't? (counts + percentages)
    print("01. Survived vs. didn't (counts + percentages)")
    survived_count = int((df["Survived"] == 1).sum())
    didnt_count = int((df["Survived"] == 0).sum())
    survived_pct = survived_count / len(df) * 100
    didnt_pct = didnt_count / len(df) * 100
    print(f"Survived: {survived_count} ({survived_pct:.2f}%)")
    print(f"Didn't:   {didnt_count} ({didnt_pct:.2f}%)")
    print()

    # 02. Survival rate by passenger class (1st, 2nd, 3rd)
    print("02. Survival rate by passenger class")
    class_rates = (df.groupby("Pclass")["Survived"].mean() * 100).round(2)
    for cls in [1, 2, 3]:
        suffix = {1: "st", 2: "nd", 3: "rd"}[cls]
        print(f"{cls}{suffix}: {class_rates.get(cls, float('nan'))}%")
    print()

    # 03. Average age of survivors vs. non-survivors
    print("03. Average age of survivors vs. non-survivors")
    avg_age_survived = df.loc[df["Survived"] == 1, "Age"].mean()
    avg_age_didnt = df.loc[df["Survived"] == 0, "Age"].mean()
    print(f"Survived: {avg_age_survived:.2f} years")
    print(f"Didn't:   {avg_age_didnt:.2f} years")
    print()

    # 04. Which embarkation port had the highest survival rate?
    print("04. Embarkation port with highest survival rate")
    embarked_rates = (
        df.dropna(subset=["Embarked"])
        .groupby("Embarked")["Survived"]
        .mean()
        .mul(100)
        .round(2)
    )
    best_port = embarked_rates.idxmax()
    print(f"Port: {best_port} ({embarked_rates.loc[best_port]}% survival rate)")
    print()

    # 05. Missing ages: count + fill with median age for that passenger class
    print("05. Missing Age values + fill with per-class median")
    missing_age_count = int(df["Age"].isna().sum())
    print(f"Missing Age values: {missing_age_count}")
    df["Age"] = df.groupby("Pclass")["Age"].transform(lambda s: s.fillna(s.median()))
    print("Filled missing Age values using median Age within each Pclass.")
    print()

    # 06. Oldest surviving passenger: print their name, age, class
    print("06. Oldest surviving passenger")
    surviving = df[df["Survived"] == 1]
    oldest_idx = surviving["Age"].idxmax()
    oldest = surviving.loc[oldest_idx, ["Name", "Age", "Pclass"]]
    print(f"Name: {oldest['Name']}")
    print(f"Age: {oldest['Age']:.2f}")
    print(f"Class: {int(oldest['Pclass'])}")
    print()

    # 07. % women survived vs. % men
    print("07. Survival rate by sex (women vs. men)")
    sex_rates = (df.groupby("Sex")["Survived"].mean() * 100).round(2)
    for sex in ["female", "male"]:
        if sex in sex_rates.index:
            print(f"{sex.capitalize()}: {sex_rates.loc[sex]}% survived")
    print()

    # 08. Add AgeGroup and show survival rate per group
    print("08. Survival rate per AgeGroup (Child/Adult/Senior)")
    df["AgeGroup"] = pd.Series(index=df.index, dtype="object")
    df.loc[df["Age"] < 18, "AgeGroup"] = "Child"
    df.loc[(df["Age"] >= 18) & (df["Age"] <= 60), "AgeGroup"] = "Adult"
    df.loc[df["Age"] > 60, "AgeGroup"] = "Senior"
    agegroup_rates = (df.groupby("AgeGroup")["Survived"].mean() * 100).round(2)
    for group in ["Child", "Adult", "Senior"]:
        if group in agegroup_rates.index:
            print(f"{group}: {agegroup_rates.loc[group]}% survived")
    print()

    # 09. Among 3rd class passengers, survival rate for men vs. women
    print("09. 3rd class survival rate by sex")
    third = df[df["Pclass"] == 3]
    third_rates = (third.groupby("Sex")["Survived"].mean() * 100).round(2)
    for sex in ["female", "male"]:
        if sex in third_rates.index:
            print(f"{sex.capitalize()}: {third_rates.loc[sex]}% survived")
    print()

    # 10. Drop rows with missing Cabin data; how many remain and what % kept?
    print("10. Drop missing Cabin rows + retention percentage")
    original_rows = len(df)
    df_cabin = df.dropna(subset=["Cabin"])
    remaining_rows = len(df_cabin)
    kept_pct = remaining_rows / original_rows * 100
    print(f"Rows remaining: {remaining_rows}")
    print(f"Percent of original data kept: {kept_pct:.2f}%")
    print()


if __name__ == "__main__":
    main()