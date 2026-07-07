from ehrql import create_measures, months, years
#from analysis.dataset_definition_patients_measures_Arnaud import dataset  # measures arnaud insetad measures 
from analysis.dataset_definition_patients_Arnaud import dataset  # as i haven't yet called all variables at patients level in patients measures.py, i will be calling it dataset ( inorder to use some variables. normally there are quite similar)
# opensafely exec ehrql:v1 generate-measures analysis/practice_variables/measures_practice_Arnaud.py --output output/measures_practice.csv

from ehrql import claim_permissions
claim_permissions("appointments")

# Create measures object
measures = create_measures()
measures.configure_disclosure_control(enabled=False)
measures.define_defaults(
    intervals=months(48).starting_on("2022-02-01"), # Here we start the 2 years before PF.
    # intervals=years(2).starting_on("2024-02-01")
)

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

group = {
    "practice": dataset.practice,
    "stp": dataset.stp,
    "region": dataset.region,
}

# appointments
measures.define_measure(
    name="appointments_scheduled",
    numerator=dataset.appointment_scheduled,
    denominator=measure_base_population,
    group_by=group,
)

measures.define_measure(
    name="appointments_seen",
    numerator=dataset.appointment_seen,
    denominator=measure_base_population,
    group_by=group,
)

# PF consultations
measures.define_measure(
    name="pf_consultation_general",
    numerator=dataset.pf_consultation_general,
    denominator=pf_eligible_population,
    group_by=group,
)

measures.define_measure(
    name="pf_consultation_uti",
    numerator=dataset.numerator_pf_consultation_uti,
    denominator=measure_base_population & dataset.include_patient_uuti,
    group_by=group,
)
"""
#------------P4----------------------------------
measures.define_measure(
    name="pf_medication_uti",
    numerator= dataset.numerator_pf_medication_uti,
    denominator=measure_base_population & dataset.include_patient_uuti,
    group_by=group,
)

measures.define_measure(
    name="gp_medication_uti",
    numerator= dataset.numerator_gp_medication_uti,
    denominator=measure_base_population & dataset.include_patient_uuti,
    group_by=group,
)
"""