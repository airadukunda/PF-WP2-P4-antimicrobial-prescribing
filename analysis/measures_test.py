from ehrql import create_measures, months
from analysis.dataset_definition_patients import dataset

measures = create_measures()
measures.configure_disclosure_control(enabled=False)

# Population denominator
# population = dataset.exists_for_patient()
# measures.configure_dummy_data(population_size=500)
measures.define_defaults(
    denominator=dataset.population,
    intervals=months(1).starting_on("2024-02-01"),
)

# Demographics
measures.define_measure(
    name="female_proportion",
    numerator=(dataset.sex == "female"),
    # denominator=dataset.exists_for_patient(),
    group_by={"region": dataset.region},
    intervals=months(1).starting_on("2024-02-01"),
)

measures.define_measure(
    name="imd_most_deprived_proportion",
    numerator=(dataset.imd == "1 (Most Deprived)"),
    # denominator=dataset.exists_for_patient(),
    group_by={"region": dataset.region},
    intervals=months(1).starting_on("2024-02-01"),
)

measures.define_measure(
    name="ethnicity_missing_proportion",
    numerator=(dataset.ethnicity == "Missing"),
    # denominator=dataset.exists_for_patient(),
    group_by={"region": dataset.region},
    intervals=months(1).starting_on("2024-02-01"),
)

measures.define_measure(
    name="pf_eligible_population_proportion",
    numerator=dataset.include_patient_overall_eligible,
    # denominator=dataset.exists_for_patient(),
    group_by={"region": dataset.region},
    intervals=months(1).starting_on("2024-02-01"),
)

measures.define_measure(
    name="children_proportion",
    numerator=(dataset.age < 18),
    # denominator=dataset.exists_for_patient(),
    group_by={"region": dataset.region},
    intervals=months(1).starting_on("2024-02-01"),
)

# PF consultation rate

measures.define_measure(
    name="pf_consultation_rate",
    numerator=dataset.has_pf_consultation,
    # denominator=population,
    group_by={"region": dataset.region},
)

# PF sore throat consultation rate

measures.define_measure(
    name="pf_eligible_sorethroat_rate",
    numerator=dataset.include_patient_sore_throat,
    # denominator=population,
    group_by={"region": dataset.region},
)

measures.define_measure(
    name="pf_eligible_otitismedia_rate",
    numerator=dataset.include_patient_otitis_media,
    # denominator=population,
    group_by={"region": dataset.region},
)