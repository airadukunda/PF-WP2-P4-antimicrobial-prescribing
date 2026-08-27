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
# P4: 
# I.Extraction of consultation measures and  eligible populations
pf = (
    df[df["measure"] == "pf_consultation_general"]
    .rename(columns={"numerator": "pf_consultation_general"})
    [["practice", "stp", "region", "interval_start", "pf_consultation_general"]]
)
# I.A.Consultation measures and  eligible populations for the 7 conditions 
#uncomplicated urinary infections
pf_uti_consultation = (
    df[df["measure"] == "pf_consultation_uti"]
    .rename(columns={"numerator": "pf_consultation_uti"})
    [["practice", "stp", "region", "interval_start", "pf_consultation_uti"]]
)

gp_uti_consultation = (
    df[df["measure"] == "gp_consultation_uti"]
    .rename(columns={"numerator": "gp_consultation_uti"})
    [["practice", "stp", "region", "interval_start", "gp_consultation_uti"]]
)

pf_uti_eligible = (
    df[df["measure"] == "pf_consultation_uti"]
    .rename(columns={"denominator": "populationeligible_uuti"})
    [["practice", "stp", "region", "interval_start", "populationeligible_uuti"]]
)
# Sinusitis consultations

pf_sinusitis_consultation = (
    df[df["measure"] == "pf_consultation_sinusitis"]
    .rename(columns={"numerator": "pf_consultation_sinusitis"})
    [["practice", "stp", "region", "interval_start",
      "pf_consultation_sinusitis"]]
)

gp_sinusitis_consultation = (
    df[df["measure"] == "gp_consultation_sinusitis"]
    .rename(columns={"numerator": "gp_consultation_sinusitis"})
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_sinusitis"]]
)

pf_sinusitis_eligible = (
    df[df["measure"] == "pf_consultation_sinusitis"]
    .rename(columns={"denominator": "populationeligible_sinusitis"})
    [["practice", "stp", "region", "interval_start",
      "populationeligible_sinusitis"]]
)

# Infected insect bite consultations 

pf_insectbite_consultation = (
    df[df["measure"] == "pf_consultation_insectbite"]
    .rename(columns={"numerator": "pf_consultation_insectbite"})
    [["practice", "stp", "region", "interval_start",
      "pf_consultation_insectbite"]]
)

gp_insectbite_consultation = (
    df[df["measure"] == "gp_consultation_insectbite"]
    .rename(columns={"numerator": "gp_consultation_insectbite"})
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_insectbite"]]
)

pf_insectbite_eligible = (
    df[df["measure"] == "pf_consultation_insectbite"]
    .rename(columns={"denominator": "populationeligible_insectbite"})
    [["practice", "stp", "region", "interval_start",
      "populationeligible_insectbite"]]
)

# Otitis media consultations
 
pf_otitismedia_consultation = (
    df[df["measure"] == "pf_consultation_otitismedia"]
    .rename(columns={"numerator": "pf_consultation_otitismedia"})
    [["practice", "stp", "region", "interval_start",
      "pf_consultation_otitismedia"]]
)

gp_otitismedia_consultation = (
    df[df["measure"] == "gp_consultation_otitismedia"]
    .rename(columns={"numerator": "gp_consultation_otitismedia"})
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_otitismedia"]]
)

pf_otitismedia_eligible = (
    df[df["measure"] == "pf_consultation_otitismedia"]
    .rename(columns={"denominator": "populationeligible_otitismedia"})
    [["practice", "stp", "region", "interval_start",
      "populationeligible_otitismedia"]]
)
# Sore throat consultations
pf_sorethroat_consultation = (
    df[df["measure"] == "pf_consultation_sorethroat"]
    .rename(columns={"numerator": "pf_consultation_sorethroat"})
    [["practice", "stp", "region", "interval_start",
      "pf_consultation_sorethroat"]]
)

gp_sorethroat_consultation = (
    df[df["measure"] == "gp_consultation_sorethroat"]
    .rename(columns={"numerator": "gp_consultation_sorethroat"})
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_sorethroat"]]
)

pf_sorethroat_eligible = (
    df[df["measure"] == "pf_consultation_sorethroat"]
    .rename(columns={"denominator": "populationeligible_sorethroat"})
    [["practice", "stp", "region", "interval_start",
      "populationeligible_sorethroat"]]
)

# Shingles consultations

pf_shingles_consultation = (
    df[df["measure"] == "pf_consultation_shingles"]
    .rename(columns={"numerator": "pf_consultation_shingles"})
    [["practice", "stp", "region", "interval_start",
      "pf_consultation_shingles"]]
)

gp_shingles_consultation = (
    df[df["measure"] == "gp_consultation_shingles"]
    .rename(columns={"numerator": "gp_consultation_shingles"})
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_shingles"]]
)

pf_shingles_eligible = (
    df[df["measure"] == "pf_consultation_shingles"]
    .rename(columns={"denominator": "populationeligible_shingles"})
    [["practice", "stp", "region", "interval_start",
      "populationeligible_shingles"]]
)

# Impetigo consultations

pf_impetigo_consultation = (
    df[df["measure"] == "pf_consultation_impetigo"]
    .rename(columns={"numerator": "pf_consultation_impetigo"})
    [["practice", "stp", "region", "interval_start",
      "pf_consultation_impetigo"]]
)

gp_impetigo_consultation = (
    df[df["measure"] == "gp_consultation_impetigo"]
    .rename(columns={"numerator": "gp_consultation_impetigo"})
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_impetigo"]]
)

pf_impetigo_eligible = (
    df[df["measure"] == "pf_consultation_impetigo"]
    .rename(columns={"denominator": "populationeligible_impetigo"})
    [["practice", "stp", "region", "interval_start",
      "populationeligible_impetigo"]]
)
# ------------------------------------------------------------------------------
# I.B.Consultation measures and  eligible populations for PF conditions combined 
# ------------------------------------------------------------------------------
pf_all_conditions_consultation = (
    df[df["measure"] == "pf_consultation_all_conditions"]
    .rename(columns={"numerator": "pf_consultation_all_conditions"})
    [["practice", "stp", "region", "interval_start",
      "pf_consultation_all_conditions"]]
)

gp_all_conditions_consultation = (
    df[df["measure"] == "gp_consultation_all_conditions"]
    .rename(columns={"numerator": "gp_consultation_all_conditions"})
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_all_conditions"]]
)

pf_all_conditions_eligible = (
    df[df["measure"] == "pf_consultation_all_conditions"]
    .rename(columns={
        "denominator": "populationeligible_all_conditions"
    })
    [["practice", "stp", "region", "interval_start",
      "populationeligible_all_conditions"]]
)
# ---------------------------------------------------------------------------------------------------------
# I.C.Consultation measures and  eligible populations for Control conditions (In General practices  only)
#----------------------------------------------------------------------------------------------------------
# Control 1: Acute bronchitis
# Denominator = include_patient_sore_throat
gp_acutebronchitis_consultation = (
    df[df["measure"] == "gp_consultation_acutebronchitis_control"]
    .rename(columns={
        "numerator": "gp_consultation_acutebronchitis_control"
    })
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_acutebronchitis_control"]]
)

gp_acutebronchitis_eligible = (
    df[df["measure"] == "gp_consultation_acutebronchitis_control"]
    .rename(columns={
        "denominator": "populationeligible_acutebronchitis_control"
    })
    [["practice", "stp", "region", "interval_start",
      "populationeligible_acutebronchitis_control"]]
)


# Control 2: Allergic conjunctivitis 
gp_conjunctivitisallergic_consultation = (
    df[df["measure"] == "gp_consultation_conjunctivitisallergic_control"]
    .rename(columns={
        "numerator": "gp_consultation_conjunctivitisallergic_control"
    })
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_conjunctivitisallergic_control"]]
)
gp_conjunctivitisallergic_eligible = (
    df[df["measure"] == "gp_consultation_conjunctivitisallergic_control"]
    .rename(columns={
        "denominator": "populationeligible_conjunctivitisallergic_control"
    })
    [["practice", "stp", "region", "interval_start",
      "populationeligible_conjunctivitisallergic_control"]]
)
# Control 3: Vulvovaginal candidiasis
gp_vulvovaginalcandidiasis_consultation = (
    df[df["measure"] == "gp_consultation_vulvovaginalcandidiasis_control"]
    .rename(columns={
        "numerator": "gp_consultation_vulvovaginalcandidiasis_control"
    })
    [["practice", "stp", "region", "interval_start",
      "gp_consultation_vulvovaginalcandidiasis_control"]]
)

gp_vulvovaginalcandidiasis_eligible = (
    df[df["measure"] == "gp_consultation_vulvovaginalcandidiasis_control"]
    .rename(columns={
        "denominator": "populationeligible_vulvovaginalcandidiasis_control"
    })
    [["practice", "stp", "region", "interval_start",
      "populationeligible_vulvovaginalcandidiasis_control"]]
)



# P4: II.Extract medication measure (nitrofurantoin)
"""
pf_nitrofurantoin = (
    df[df["measure"] == "pf_medication_nitrofurantoin"]
    .rename(columns={"numerator": "pf_nitrofurantoin"})
    [["practice", "stp", "region", "interval_start", "pf_nitrofurantoin"]]
)
"""
# P4:
# II. Medication measures
# II.A. Extraction of medication measures for the 7 conditions 
# II.A.1.CP level  

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

## II.A.2.General practice level
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

# II.B. Control medication measures (in GP only)

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
df_wide = df_wide.merge(gp_uti_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_uti_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_medication_uti, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_uti, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(pf_sinusitis_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_sinusitis_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_sinusitis_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_medication_sinusitis, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_sinusitis, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(pf_insectbite_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_insectbite_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_insectbite_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_medication_insectbite, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_insectbite, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(pf_otitismedia_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_otitismedia_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_otitismedia_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_medication_otitismedia, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_otitismedia, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(pf_sorethroat_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_sorethroat_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_sorethroat_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_medication_sorethroat, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_sorethroat, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(pf_shingles_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_shingles_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_shingles_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_medication_shingles, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_shingles, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(pf_impetigo_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_impetigo_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_impetigo_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_medication_impetigo, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_impetigo, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(pf_all_conditions_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_all_conditions_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_all_conditions_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(pf_medication_all_conditions, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_all_conditions, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(gp_acutebronchitis_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_acutebronchitis_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_acutebronchitis_control, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(gp_conjunctivitisallergic_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_conjunctivitisallergic_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_conjunctivitisallergic_control, on=["practice", "stp", "region", "interval_start"], how="left")

df_wide = df_wide.merge(gp_vulvovaginalcandidiasis_consultation, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_vulvovaginalcandidiasis_eligible, on=["practice", "stp", "region", "interval_start"], how="left")
df_wide = df_wide.merge(gp_medication_vulvovaginalcandidiasis_control, on=["practice", "stp", "region", "interval_start"], how="left")
#
for col in [
    "appointments_scheduled",
    "appointments_seen",

    # P4: General PF consultation
    "pf_consultation_general",

    # P4: PF and GP consultation measures - 7 conditions
    "pf_consultation_uti",
    "gp_consultation_uti",
    "populationeligible_uuti",

    "pf_consultation_sinusitis",
    "gp_consultation_sinusitis",
    "populationeligible_sinusitis",

    "pf_insectbite_consultation",
    "gp_insectbite_consultation",
    "populationeligible_insectbite",

    "pf_otitismedia_consultation",
    "gp_otitismedia_consultation",
    "populationeligible_otitismedia",

    "pf_sorethroat_consultation",
    "gp_sorethroat_consultation",
    "populationeligible_sorethroat",

    "pf_shingles_consultation",
    "gp_shingles_consultation",
    "populationeligible_shingles",

    "pf_impetigo_consultation",
    "gp_impetigo_consultation",
    "populationeligible_impetigo",

    # P4: All PF conditions combined
    "pf_consultation_all_conditions",
    "gp_consultation_all_conditions",
    "populationeligible_all_conditions",

    # P4: PF medication measures
    "pf_medication_uti",
    "pf_medication_sinusitis",
    "pf_medication_insectbite",
    "pf_medication_otitismedia",
    "pf_medication_sorethroat",
    "pf_medication_shingles",
    "pf_medication_impetigo",
    "pf_medication_all_conditions",

    # P4: GP medication measures
    "gp_medication_uti",
    "gp_medication_sinusitis",
    "gp_medication_insectbite",
    "gp_medication_otitismedia",
    "gp_medication_sorethroat",
    "gp_medication_shingles",
    "gp_medication_impetigo",
    "gp_medication_all_conditions",

    # P4: GP control consultation measures
    "gp_consultation_acutebronchitis_control",
    "populationeligible_acutebronchitis_control",

    "gp_consultation_conjunctivitisallergic_control",
    "populationeligible_conjunctivitisallergic_control",

    "gp_consultation_vulvovaginalcandidiasis_control",
    "populationeligible_vulvovaginalcandidiasis_control",

    # P4: GP control medication measures
    "gp_medication_acutebronchitis_control",
    "gp_medication_conjunctivitisallergic_control",
    "gp_medication_vulvovaginalcandidiasis_control",
]:
    df_wide[col] = df_wide[col].fillna(0)
    
# P4 : Proportion of PF UTI consultations resulting in nitrofurantoin
# df_wide["nitrofurantoin_prescribing_proportion"] = (df_wide["pf_nitrofurantoin"]/ df_wide["pf_consultation_uti"])
# P4 : Here , we will replace undefined values when no PF UTI consultations occurred
# df_wide["nitrofurantoin_prescribing_proportion"] = (df_wide["nitrofurantoin_prescribing_proportion"].fillna(0))

df_wide.to_csv("output/practice_level_data.csv", index=False)

# print(df_wide.head())
# print(df_wide["interval_start"].unique())
# print(df_wide.groupby("interval_start")["practice"].nunique())