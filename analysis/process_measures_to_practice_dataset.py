import pandas as pd

input_file = "output/practice_measures.csv"
df = pd.read_csv(input_file)

print(df.groupby("interval_start")["practice"].nunique())
print(df[df["measure"] == "population"].groupby("interval_start")["numerator"].sum())

df["interval_start"] = pd.to_datetime(df["interval_start"])

# base = df[["practice", "stp", "region", "interval_start"]].drop_duplicates()

# pop_df = (
#     df[df["measure"] == "population"]
#     .groupby(["practice", "stp", "region", "interval_start"], as_index=False)["numerator"]
#     .sum()
#     .rename(columns={"numerator": "population"})
# )

# df_measures = df[df["measure"] != "population"]

# df_wide = (
#     df_measures
#     .groupby(["practice", "stp", "region", "interval_start", "measure"], as_index=False)["numerator"]
#     .sum()
#     .pivot(
#         index=["practice", "stp", "region", "interval_start"],
#         columns="measure",
#         values="numerator"
#     )
#     .reset_index()
# )

# df_wide.columns.name = None

# df_wide = base.merge(
#     df_wide,
#     on=["practice", "stp", "region", "interval_start"],
#     how="left"
# )

# df_wide = df_wide.merge(
#     pop_df,
#     on=["practice", "stp", "region", "interval_start"],
#     how="left"
# )

# id_cols = ["practice", "stp", "region", "interval_start", "population"]
# measure_cols = [c for c in df_wide.columns if c not in id_cols]
# df_wide[measure_cols] = df_wide[measure_cols].fillna(0)

# pf_cols = [
#     "pf_uti", "pf_sinusitis", "pf_insectbite",
#     "pf_otitismedia", "pf_sorethroat",
#     "pf_shingles", "pf_impetigo"
# ]

# for col in pf_cols:
#     if col not in df_wide.columns:
#         df_wide[col] = 0

# df_wide["pf_total"] = df_wide[pf_cols].sum(axis=1)

pop = (
    df[df["measure"] == "population"]
    .rename(columns={"numerator": "population"})
    [["practice", "stp", "region", "interval_start", "population"]]
)

appt = (
    df[df["measure"] == "appointments_total"]
    .rename(columns={"numerator": "appointments_total"})
    [["practice", "stp", "region", "interval_start", "appointments_total"]]
)

df_wide = pop.merge(
    appt,
    on=["practice", "stp", "region", "interval_start"],
    how="left"
)

df_wide["appointments_total"] = df_wide["appointments_total"].fillna(0)


pf = (
    df[df["measure"] == "pf_consultation_general"]
    .rename(columns={"numerator": "pf_consultation_general"})
    [["practice", "stp", "region", "interval_start", "pf_consultation_general"]]
)
pf_uti_consultation = (
    df[df["measure"] == "pf_consultation_uti"]
    .rename(columns={"numerator": "pf_consultation_uti"})
    [["practice", "stp", "region", "interval_start", "pf_consultation_uti"]]
)
pf_uti_eligible = (
    df[df["measure"] == "populationeligible_uuti"]
    .rename(columns={"numerator": "populationeligible_uuti"})
    [["practice", "stp", "region", "interval_start", "populationeligible_uuti"]]
)

df_wide = df_wide.merge(pf, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_uti_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_uti_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide["pf_consultation_general"] = df_wide["pf_consultation_general"].fillna(0)
df_wide["pf_consultation_uti"] = df_wide["pf_consultation_uti"].fillna(0)
df_wide["populationeligible_uuti"] = df_wide["populationeligible_uuti"].fillna(0)

df_wide.to_csv("output/practice_level_data.csv", index=False)

print(df_wide.head())
print(df_wide["interval_start"].unique())
print(df_wide.groupby("interval_start")["practice"].nunique())
print(df_wide.groupby("interval_start")["population"].sum())