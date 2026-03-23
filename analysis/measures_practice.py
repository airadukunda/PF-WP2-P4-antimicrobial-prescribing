from ehrql import create_measures, months
from analysis.dataset_definition_patients_measures import dataset
# opensafely exec ehrql:v1 generate-measures analysis/measures_practice.py --output output/measures_practice.csv

from ehrql import claim_permissions
claim_permissions("appointments")

# Create measures object
measures = create_measures()
measures.configure_disclosure_control(enabled=False)

group = {
    "practice": dataset.practice,
    "stp": dataset.stp,
    "region": dataset.region,
    "start_date": dataset.start_date,
}
measures.define_defaults(
    # intervals=months(1).starting_on("2024-02-01"),
    intervals=months(2).starting_on("2024-02-01")
)

# population
measures.define_measure(
    name="population",
    numerator=dataset.registered_index,
    denominator=dataset.registered_index.is_not_null(),
    group_by=group,
)

# appointments
measures.define_measure(
    name="appointments_total",
    numerator=dataset.appointment_count,
    denominator=dataset.registered_index.is_not_null(),
    group_by=group,
)

# PF count by condition
conditions = ["uti","sinusitis","insectbite","otitismedia","sorethroat","shingles","impetigo"]
for cond in conditions:
    measures.define_measure(
        name=f"pf_{cond}",
        numerator=getattr(dataset, f"numerator_pf_consultation_{cond}"),
        denominator=dataset.registered_index.is_not_null(),
        group_by=group,
        )
