import pandas as pd

input_file = "output/practice_measures.csv"
df = pd.read_csv(input_file)

print(df.groupby("interval_start")["practice"].nunique())

df["interval_start"] = pd.to_datetime(df["interval_start"])

pop = (
    df[df["measure"] == "appointments_scheduled"]
    .rename(columns={"denominator": "population"})
    [["practice", "stp", "region", "interval_start", "population"]]
)

appt_scheduled = (
    df[df["measure"] == "appointments_scheduled"]
    .rename(columns={"numerator": "appointments_scheduled"})
    [["practice", "stp", "region", "interval_start", "appointments_scheduled"]]
)

appt_seen = (
    df[df["measure"] == "appointments_seen"]
    .rename(columns={"numerator": "appointments_seen"})
    [["practice", "stp", "region", "interval_start", "appointments_seen"]]
)

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
    df[df["measure"] == "pf_consultation_uti"]
    .rename(columns={"denominator": "populationeligible_uuti"})
    [["practice", "stp", "region", "interval_start", "populationeligible_uuti"]]
)

# NEW: Extract medication measure (nitrofurantoin)
pf_nitrofurantoin = (
    df[df["measure"] == "pf_medication_nitrofurantoin"]
    .rename(columns={"numerator": "pf_nitrofurantoin"})
    [["practice", "stp", "region", "interval_start", "pf_nitrofurantoin"]]
)


df_wide = pop.merge(appt_scheduled,on=["practice", "stp", "region", "interval_start"],how="left")
df_wide = df_wide.merge(appt_seen,on=["practice", "stp", "region", "interval_start"],how="left")
df_wide = df_wide.merge(pf, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_uti_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_uti_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
# NEW: Merge medication measure
df_wide = df_wide.merge(pf_nitrofurantoin,on=["practice", "stp", "region", "interval_start"],how="left")
for col in [
    "appointments_scheduled",
    "appointments_seen",
    "pf_consultation_general",
    "pf_consultation_uti",
    "populationeligible_uuti",
    "pf_nitrofurantoin",     # NEW: Fill missing medication values
]:
    df_wide[col] = df_wide[col].fillna(0)

# NEW: Proportion of PF UTI consultations resulting in nitrofurantoin
df_wide["nitrofurantoin_prescribing_proportion"] = (df_wide["pf_nitrofurantoin"]/ df_wide["pf_consultation_uti"])
# NEW: Here , we will replace undefined values when no PF UTI consultations occurred
df_wide["nitrofurantoin_prescribing_proportion"] = (df_wide["nitrofurantoin_prescribing_proportion"].fillna(0))

df_wide.to_csv("output/practice_level_data.csv", index=False)

# print(df_wide.head())
# print(df_wide["interval_start"].unique())
# print(df_wide.groupby("interval_start")["practice"].nunique())