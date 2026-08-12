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

# P4: Extract medication measure (nitrofurantoin)
pf_nitrofurantoin = (
    df[df["measure"] == "pf_medication_nitrofurantoin"]
    .rename(columns={"numerator": "pf_nitrofurantoin"})
    [["practice", "stp", "region", "interval_start", "pf_nitrofurantoin"]]
)

# P4: Extraction of medication measures

pf_medication_uti = (
    df[df["measure"] == "pf_medication_uti"]
    .rename(columns={"numerator": "pf_medication_uti"})
    [["practice", "stp", "region", "interval_start", "pf_medication_uti"]]
)

pf_medication_sinusitis = (
    df[df["measure"] == "pf_medication_sinusitis"]
    .rename(columns={"numerator": "pf_medication_sinusitis"})
    [["practice", "stp", "region", "interval_start", "pf_medication_sinusitis"]]
)

pf_medication_insectbite = (
    df[df["measure"] == "pf_medication_insectbite"]
    .rename(columns={"numerator": "pf_medication_insectbite"})
    [["practice", "stp", "region", "interval_start", "pf_medication_insectbite"]]
)

pf_medication_otitismedia = (
    df[df["measure"] == "pf_medication_otitismedia"]
    .rename(columns={"numerator": "pf_medication_otitismedia"})
    [["practice", "stp", "region", "interval_start", "pf_medication_otitismedia"]]
)

pf_medication_sorethroat = (
    df[df["measure"] == "pf_medication_sorethroat"]
    .rename(columns={"numerator": "pf_medication_sorethroat"})
    [["practice", "stp", "region", "interval_start", "pf_medication_sorethroat"]]
)

pf_medication_shingles = (
    df[df["measure"] == "pf_medication_shingles"]
    .rename(columns={"numerator": "pf_medication_shingles"})
    [["practice", "stp", "region", "interval_start", "pf_medication_shingles"]]
)

pf_medication_impetigo = (
    df[df["measure"] == "pf_medication_impetigo"]
    .rename(columns={"numerator": "pf_medication_impetigo"})
    [["practice", "stp", "region", "interval_start", "pf_medication_impetigo"]]
)

pf_medication_all_conditions = (
    df[df["measure"] == "pf_medication_all_conditions"]
    .rename(columns={"numerator": "pf_medication_all_conditions"})
    [["practice", "stp", "region", "interval_start", "pf_medication_all_conditions"]]
)

#General practice level
# P4: GP medication measures
gp_medication_uti = (
    df[df["measure"] == "gp_medication_uti"]
    .rename(columns={"numerator": "gp_medication_uti"})
    [["practice", "stp", "region", "interval_start", "gp_medication_uti"]]
)

gp_medication_sinusitis = (
    df[df["measure"] == "gp_medication_sinusitis"]
    .rename(columns={"numerator": "gp_medication_sinusitis"})
    [["practice", "stp", "region", "interval_start", "gp_medication_sinusitis"]]
)

gp_medication_insectbite = (
    df[df["measure"] == "gp_medication_insectbite"]
    .rename(columns={"numerator": "gp_medication_insectbite"})
    [["practice", "stp", "region", "interval_start", "gp_medication_insectbite"]]
)

gp_medication_otitismedia = (
    df[df["measure"] == "gp_medication_otitismedia"]
    .rename(columns={"numerator": "gp_medication_otitismedia"})
    [["practice", "stp", "region", "interval_start", "gp_medication_otitismedia"]]
)

gp_medication_sorethroat = (
    df[df["measure"] == "gp_medication_sorethroat"]
    .rename(columns={"numerator": "gp_medication_sorethroat"})
    [["practice", "stp", "region", "interval_start", "gp_medication_sorethroat"]]
)

gp_medication_shingles = (
    df[df["measure"] == "gp_medication_shingles"]
    .rename(columns={"numerator": "gp_medication_shingles"})
    [["practice", "stp", "region", "interval_start", "gp_medication_shingles"]]
)

gp_medication_impetigo = (
    df[df["measure"] == "gp_medication_impetigo"]
    .rename(columns={"numerator": "gp_medication_impetigo"})
    [["practice", "stp", "region", "interval_start", "gp_medication_impetigo"]]
)

gp_medication_all_conditions = (
    df[df["measure"] == "gp_medication_all_conditions"]
    .rename(columns={"numerator": "gp_medication_all_conditions"})
    [["practice", "stp", "region", "interval_start", "gp_medication_all_conditions"]]
)

# NEW: GP control medication measures

gp_medication_acutebronchitis_control = (
    df[df["measure"] == "gp_medication_acutebronchitis_control"]
    .rename(columns={"numerator": "gp_medication_acutebronchitis_control"})
    [["practice", "stp", "region", "interval_start", "gp_medication_acutebronchitis_control"]]
)

gp_medication_conjunctivitisallergic_control = (
    df[df["measure"] == "gp_medication_conjunctivitisallergic_control"]
    .rename(columns={"numerator": "gp_medication_conjunctivitisallergic_control"})
    [["practice", "stp", "region", "interval_start", "gp_medication_conjunctivitisallergic_control"]]
)

gp_medication_vulvovaginalcandidiasis_control = (
    df[df["measure"] == "gp_medication_vulvovaginalcandidiasis_control"]
    .rename(columns={"numerator": "gp_medication_vulvovaginalcandidiasis_control"})
    [["practice", "stp", "region", "interval_start", "gp_medication_vulvovaginalcandidiasis_control"]]
)

df_wide = pop.merge(appt_scheduled,on=["practice", "stp", "region", "interval_start"],how="left")
df_wide = df_wide.merge(appt_seen,on=["practice", "stp", "region", "interval_start"],how="left")
df_wide = df_wide.merge(pf, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_uti_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_uti_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
# P4 : PF medication measures
df_wide = df_wide.merge(pf_nitrofurantoin,on=["practice", "stp", "region", "interval_start"],how="left")
df_wide = df_wide.merge(pf_medication_uti,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(pf_medication_sinusitis,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(pf_medication_insectbite,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(pf_medication_otitismedia,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(pf_medication_sorethroat,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(pf_medication_shingles,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(pf_medication_impetigo,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(pf_medication_all_conditions,on=["practice", "stp", "region", "interval_start"],how="left",)
# P4 : GP medication measures
df_wide = df_wide.merge(gp_medication_uti,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(gp_medication_sinusitis,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(gp_medication_insectbite,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(gp_medication_otitismedia,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(gp_medication_sorethroat,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(gp_medication_shingles,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(gp_medication_impetigo,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(gp_medication_all_conditions,on=["practice", "stp", "region", "interval_start"],how="left",)
# P4 : GP control medication measures
df_wide = df_wide.merge(gp_medication_acutebronchitis_control,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(gp_medication_conjunctivitisallergic_control,on=["practice", "stp", "region", "interval_start"],how="left",)
df_wide = df_wide.merge(gp_medication_vulvovaginalcandidiasis_control,on=["practice", "stp", "region", "interval_start"],how="left",)
for col in [
    "appointments_scheduled",
    "appointments_seen",
    "pf_consultation_general",
    "pf_consultation_uti",
    "populationeligible_uuti",
    # P4 : PF medication measures
    "pf_nitrofurantoin",  
    "pf_medication_uti",
    "pf_medication_sinusitis",
    "pf_medication_insectbite",
    "pf_medication_otitismedia",
    "pf_medication_sorethroat",
    "pf_medication_shingles",
    "pf_medication_impetigo",
    "pf_medication_all_conditions",
    # P4 : GP medication measures
    "gp_medication_uti",
    "gp_medication_sinusitis",
    "gp_medication_insectbite",
    "gp_medication_otitismedia",
    "gp_medication_sorethroat",
    "gp_medication_shingles",
    "gp_medication_impetigo",
    "gp_medication_all_conditions",
    # P4 : GP control medication measures
    "gp_medication_acutebronchitis_control",
    "gp_medication_conjunctivitisallergic_control",
    "gp_medication_vulvovaginalcandidiasis_control",
]:
    df_wide[col] = df_wide[col].fillna(0)

# P4 : Proportion of PF UTI consultations resulting in nitrofurantoin
df_wide["nitrofurantoin_prescribing_proportion"] = (df_wide["pf_nitrofurantoin"]/ df_wide["pf_consultation_uti"])
# P4 : Here , we will replace undefined values when no PF UTI consultations occurred
df_wide["nitrofurantoin_prescribing_proportion"] = (df_wide["nitrofurantoin_prescribing_proportion"].fillna(0))

df_wide.to_csv("output/practice_level_data.csv", index=False)

# print(df_wide.head())
# print(df_wide["interval_start"].unique())
# print(df_wide.groupby("interval_start")["practice"].nunique())