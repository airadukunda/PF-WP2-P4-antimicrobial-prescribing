from ehrql import create_dataset, weeks, show
from ehrql.tables.tpp import patients, practice_registrations, clinical_events
import codelists
dataset = create_dataset()

start_date = "2020-01-31"
index_date = "2025-11-30"

# registration is not important here as we want to capture pregnancy regardless
#registration_start = practice_registrations.for_patient_on(start_date)
#registration_end = practice_registrations.for_patient_on(index_date)

# find first end-of-pregnancy code
dataset.pregnancy_end_first = clinical_events.where(
    clinical_events.snomedct_code.is_in(codelists.end_pregnancy_codelist)).sort_by(clinical_events.date).first_for_patient().date

# get code for end of pregnancy
# might want to use this to check that short pregnancies are early losses 
# but would need to classify the codelist
#dataset.pregnancy_end_cod = clinical_events.where(
#    clinical_events.snomedct_code.is_in(codelists.end_pregnancy_codelist)).sort_by(clinical_events.date).first_for_patient().snomedct_code


# estimated date of delivery
# we can use this to estimate the known start of pregnancy ~8 months earlier
# Firstly select all events within a few weeks before / several months after the actual delivery date
# (Allow end of pregnancy up to 4 weeks "late" or 36 weeks "early")
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_between(dataset.pregnancy_end_first - weeks(4), dataset.pregnancy_end_first + weeks(36))
)
    
# now extract EDD within window of end of pregnancy
dataset.pregnancy_edd = selected_events.where(
    selected_events.snomedct_code.is_in(codelists.edd_codes)).sort_by(selected_events.date).last_for_patient().date


# calculate gestation at end of pregnancy
pregnancy_how_early = (dataset.pregnancy_edd - dataset.pregnancy_end_first).weeks
dataset.pregnancy_length_from_edd = 40 - pregnancy_how_early


# for start of pregnancy, assume pregnancy status known from 8 weeks
dataset.pregnancy_known_date = dataset.pregnancy_edd - weeks(32)

##### next
# do something when end of pregnancy is missing i.e ongoing pregnancies
# do something when EDD is missing

### pregnancy 2-10 ####
for n in range(2, 10):
    # find next end-of-pregnancy code
    preg_next_query = pregnancy_end_next = clinical_events.where(
        clinical_events.snomedct_code.is_in(codelists.end_pregnancy_codelist)
        &
        clinical_events.date.is_on_or_after(dataset.pregnancy_end_first + weeks(12))
        ).sort_by(clinical_events.date).first_for_patient().date
    
    dataset.add_column(f"pregnancy_end_{n}", preg_next_query)
    
    # now extract EDD within window of end of pregnancy
    preg_next_edd_query = clinical_events.where(
        clinical_events.snomedct_code.is_in(codelists.edd_codes)
        &
        clinical_events.date.is_on_or_between(preg_next_query - weeks(4), preg_next_query + weeks(36))
        ).sort_by(clinical_events.date).last_for_patient().date
    dataset.add_column(f"pregnancy_edd_{n}", preg_next_edd_query)


dataset.sex = patients.sex
dataset.age = patients.age_on(index_date)
dataset.define_population(
    (patients.sex == "female") & (dataset.age <=50) & (dataset.age >=11)
)

show(dataset)