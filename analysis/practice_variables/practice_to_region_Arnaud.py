import pandas as pd

df = pd.read_csv("output/practice_level_data.csv")

df["interval_start"] = pd.to_datetime(df["interval_start"])

summary_region = (
    df.groupby(["interval_start", "region"])
    .agg(
        n_stp=("stp", "nunique"),
        n_practices=("practice", "nunique"),

        population_total=("population", "sum"),
        population_max_practice=("population", "max"),
        population_min_practice=("population", "min"),

        appointments_scheduled=("appointments_scheduled", "sum"),
        appointments_seen=("appointments_seen", "sum"),

        pf_consultation_general=("pf_consultation_general", "sum"),
        pf_consultation_uti=("pf_consultation_uti", "sum"),

        populationeligible_uuti=("populationeligible_uuti", "sum"),

        # P4: PF medication measures
        pf_medication_uti=("pf_medication_uti", "sum"),
        pf_medication_sinusitis=("pf_medication_sinusitis", "sum"),
        pf_medication_insectbite=("pf_medication_insectbite", "sum"),
        pf_medication_otitismedia=("pf_medication_otitismedia", "sum"),
        pf_medication_sorethroat=("pf_medication_sorethroat", "sum"),
        pf_medication_shingles=("pf_medication_shingles", "sum"),
        pf_medication_impetigo=("pf_medication_impetigo", "sum"),
        pf_medication_all_conditions=("pf_medication_all_conditions", "sum"),

        # P4: GP medication measures
        gp_medication_uti=("gp_medication_uti", "sum"),
        gp_medication_sinusitis=("gp_medication_sinusitis", "sum"),
        gp_medication_insectbite=("gp_medication_insectbite", "sum"),
        gp_medication_otitismedia=("gp_medication_otitismedia", "sum"),
        gp_medication_sorethroat=("gp_medication_sorethroat", "sum"),
        gp_medication_shingles=("gp_medication_shingles", "sum"),
        gp_medication_impetigo=("gp_medication_impetigo", "sum"),
        gp_medication_all_conditions=("gp_medication_all_conditions", "sum"),

        # P4: GP control medication measures
        gp_medication_acutebronchitis_control=(
            "gp_medication_acutebronchitis_control",
            "sum",
        ),
        gp_medication_conjunctivitisallergic_control=(
            "gp_medication_conjunctivitisallergic_control",
            "sum",
        ),
        gp_medication_vulvovaginalcandidiasis_control=(
            "gp_medication_vulvovaginalcandidiasis_control",
            "sum",
        ),
    )
    .reset_index()
)

summary_region.to_csv("output/practice_summary_by_region.csv",index=False,)