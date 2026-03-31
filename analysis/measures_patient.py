from ehrql import create_measures, months
from analysis.dataset_definition_patients_measures import dataset
# opensafely exec ehrql:v1 generate-measures analysis/measures_patient.py --output output/measures_patient.csv

measures = create_measures()

measure_base_population = (
    dataset.alive
    & dataset.registered_start
    & dataset.registered_index
    & (dataset.age <= 120)
)

pf_eligible_population = (
    dataset.include_patient_overall_eligible
    & measure_base_population
)

pf_consultation_population_eligible = (
    (dataset.pf_consultation_general > 0)
    & pf_eligible_population
)

pf_consultation_population_all = (
    (dataset.pf_consultation_general > 0)
    & measure_base_population
)

measures.define_defaults(
    intervals=months(1).starting_on("2024-02-01")
)
measures.configure_disclosure_control(enabled=False)

# check base cohort size
measures.define_measure(
    name="population_by_sex",
    numerator=measure_base_population,
    denominator=measure_base_population,
    group_by = {"sex": dataset.sex},
)

measures.define_measure(
    name="population_by_region",
    numerator=measure_base_population,
    denominator=measure_base_population,
    group_by={"region": dataset.region},
)

measures.define_measure(
    name="population_by_imd",
    numerator=measure_base_population,
    denominator=measure_base_population,
    group_by={"imd": dataset.imd},
)

measures.define_measure(
    name="population_by_ethnicity",
    numerator=measure_base_population,
    denominator=measure_base_population,
    group_by={"ethnicity": dataset.ethnicity},
)

# # check practice size in base cohort
# # should be the same as population_base_eligible but grouped by practice instead of region, in case there are missing practice codes in the dataset
# # may be used to exclude practices with very small patient numbers from practice-level analyses
# measures.define_measure(
#     name="population_by_practice",
#     numerator=measure_base_population,
#     denominator=measure_base_population,
#     group_by={
#         "practice": dataset.practice
#     },
# )

# check PF eligible population size from base cohort
measures.define_measure(
    name="pf_eligible_population_by_sex",
    numerator=pf_eligible_population,
    denominator=measure_base_population,
    group_by={"sex": dataset.sex},
)

# among PF eligible population, check how many had a PF consultation
measures.define_measure(
    name="pf_eligible_population_with_consultation_by_sex",
    numerator=pf_consultation_population_eligible,
    denominator=pf_eligible_population,
    group_by={"sex": dataset.sex},
)

# among all population, check how many had a PF consultation
measures.define_measure(
    name="population_with_pf_consultation_by_sex",
    numerator=pf_consultation_population_all,
    denominator=measure_base_population,
    group_by={"sex": dataset.sex},
)

