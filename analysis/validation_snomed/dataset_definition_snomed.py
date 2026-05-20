# analysis/dataset_definition_snomed_validation.py
# gunzip -c output/dataset_patients_snomed.csv.gz > output/dataset_patients_snomed.csv

from ehrql import create_dataset, get_parameter, INTERVAL, days, months, show
from ehrql.tables.tpp import (patients, practice_registrations, clinical_events)

import analysis.codelists as codelists

dataset = create_dataset()
dataset.configure_dummy_data(population_size=500)

start_date = get_parameter("start_date", default="2024-02-01")
index_date = start_date + months(1) - days(1)

#----------------------------------------
# Patient identifiers: alive_status, registration_status
alive = patients.is_alive_on(index_date) # alive at the end of month
# Only include the patient if they were registered for the whole month, 
# so registered before the month starts and not deregistered or died during the month
registered_start = practice_registrations.for_patient_on(start_date).exists_for_patient()
registered_index = practice_registrations.for_patient_on(index_date).exists_for_patient()

# Demographics: sex, age, patient_imd
sex = patients.sex
age = patients.age_on(index_date)

# Define population
# base_population = patients.exists_for_patient()
age_valid = (patients.age_on(index_date) <= 120) # "Exclude any patients over 120 years old as the date of birth is most likely to be missing"
base_population = alive & registered_start & registered_index & age_valid 
dataset.define_population(base_population) # include all patients or those alive and registered

#----------------------------------------
# condition = get_parameter("condition")
condition = "sorethroat"

pf_gp_codelists = {
    "uti": codelists.gp_snomed_codelist_uti,
    "sinusitis": codelists.gp_snomed_codelist_sinusitis,
    "insectbite": codelists.gp_snomed_codelist_insect_bites,
    "otitismedia": codelists.gp_snomed_codelist_otitis_media,
    "sorethroat": codelists.gp_snomed_codelist_sore_throat,
    "shingles": codelists.gp_snomed_codelist_shingles,
    "impetigo": codelists.gp_snomed_codelist_impetigo,
}

codes = pf_gp_codelists[condition]

for code in codes:

    code_events = clinical_events.where(
        clinical_events.date.is_on_or_between(start_date, index_date)
        & (clinical_events.snomedct_code == code)
    )

    dataset.add_column(
        f"count_{code}",
        code_events.count_for_patient(),
    )


show(dataset)