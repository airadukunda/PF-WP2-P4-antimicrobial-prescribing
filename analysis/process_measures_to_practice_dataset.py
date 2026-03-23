import pandas as pd

input_file = "output/practice_measures.csv"
df = pd.read_csv(input_file)

print(df.groupby("interval_start")["practice"].nunique())
print(df[df["measure"] == "population"].groupby("interval_start")["numerator"].sum())

df["interval_start"] = pd.to_datetime(df["interval_start"])
df["count"] = df["numerator"]

base = df[["practice", "stp", "region", "interval_start"]].drop_duplicates()

pop_df = (
    df[df["measure"] == "population"]
    .groupby(["practice", "stp", "region", "interval_start"], as_index=False)["numerator"]
    .sum()
    .rename(columns={"numerator": "population"})
)

df_measures = df[df["measure"] != "population"]

df_wide = (
    df_measures
    .groupby(["practice", "stp", "region", "interval_start", "measure"], as_index=False)["count"]
    .sum()
    .pivot(
        index=["practice", "stp", "region", "interval_start"],
        columns="measure",
        values="count"
    )
    .reset_index()
)

df_wide.columns.name = None

df_wide = base.merge(
    df_wide,
    on=["practice", "stp", "region", "interval_start"],
    how="left"
)

df_wide = df_wide.merge(
    pop_df,
    on=["practice", "stp", "region", "interval_start"],
    how="left"
)

id_cols = ["practice", "stp", "region", "interval_start", "population"]
measure_cols = [c for c in df_wide.columns if c not in id_cols]
df_wide[measure_cols] = df_wide[measure_cols].fillna(0)

pf_cols = [
    "pf_uti", "pf_sinusitis", "pf_insectbite",
    "pf_otitismedia", "pf_sorethroat",
    "pf_shingles", "pf_impetigo"
]

for col in pf_cols:
    if col not in df_wide.columns:
        df_wide[col] = 0

df_wide["pf_total"] = df_wide[pf_cols].sum(axis=1)

df_wide.to_csv("output/practice_level_data.csv", index=False)

print(df_wide.head())
print(df_wide["interval_start"].unique())
print(df_wide.groupby("interval_start")["practice"].nunique())
print(df_wide.groupby("interval_start")["population"].sum())