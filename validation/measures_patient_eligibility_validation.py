from ehrql import case, create_measures, months, when
from analysis.dataset_definition_patients_measures import dataset

measures = create_measures()
measures.configure_disclosure_control(enabled=False)

# =====================================================
# Base population
# =====================================================
base = (
    dataset.alive
    & dataset.registered_start
    & dataset.registered_index
    & (dataset.age <= 120)
)

# =====================================================
# Age group (for validation)
# =====================================================
age_group = case(
    when(dataset.age < 5).then("0-4"),
    when(dataset.age < 16).then("5-15"),
    when(dataset.age < 20).then("16-19"),
    when(dataset.age < 45).then("20-44"),
    when(dataset.age < 65).then("45-64"),
    when(dataset.age < 80).then("65-79"),
    when(dataset.age >= 80).then("80+"),
    when(dataset.age.is_null()).then("Missing"),
)

group = {
    "sex": dataset.sex,
    "age_group": age_group,
}

# =====================================================
# Time intervals
# =====================================================
measures.define_defaults(
    intervals=months(1).starting_on("2024-02-01")
)

# =====================================================
# 1️⃣ RAW CLINICAL FLAGS (most important)
# =====================================================

measures.define_measure(
    name="pregnant_this_month",
    numerator=dataset.pregnant_this_month,
    denominator=base,
    group_by=group,
)

measures.define_measure(
    name="bullous_impetigo_this_month",
    numerator=dataset.bullous_impetigo_this_month,
    denominator=base,
    group_by=group,
)

measures.define_measure(
    name="recurrent_impetigo_this_year",
    numerator=dataset.recurrent_impetigo_this_year,
    denominator=base,
    group_by=group,
)

measures.define_measure(
    name="catheter_status",
    numerator=dataset.catheter_status,
    denominator=base,
    group_by=group,
)

measures.define_measure(
    name="recurrent_uti_6m",
    numerator=dataset.recurrent_uti_6m,
    denominator=base,
    group_by=group,
)

measures.define_measure(
    name="recurrent_uti_12m",
    numerator=dataset.recurrent_uti_12m,
    denominator=base,
    group_by=group,
)

measures.define_measure(
    name="recurrent_uti",
    numerator=dataset.recurrent_uti,
    denominator=base,
    group_by=group,
)

# =====================================================
# 2️⃣ ELIGIBILITY COMPONENTS (inclusion / exclusion)
# ⚠️ requires these to be added to dataset_definition first:
# dataset.uuti_eligible, dataset.uuti_exclusion, etc.
# =====================================================

# --- UUTI components ---
measures.define_measure(
    name="uuti_eligible",
    numerator=dataset.uuti_eligible,
    denominator=base,
    group_by=group,
)

measures.define_measure(
    name="uuti_exclusion",
    numerator=dataset.uuti_exclusion,
    denominator=base,
    group_by=group,
)

# --- Impetigo components ---
measures.define_measure(
    name="impetigo_exclusion",
    numerator=dataset.impetigo_exclusion,
    denominator=base,
    group_by=group,
)

# --- Sore throat / insect bite exclusions ---
measures.define_measure(
    name="sore_throat_exclusion",
    numerator=dataset.exclusion_sore_throat,
    denominator=base,
    group_by=group,
)

measures.define_measure(
    name="insect_bite_exclusion",
    numerator=dataset.exclusion_insect_bites,
    denominator=base,
    group_by=group,
)

# =====================================================
# 3️⃣ FINAL ELIGIBILITY FLAGS
# =====================================================

conditions = [
    "otitis_media",
    "sinusitis",
    "sore_throat",
    "insect_bites",
    "shingles",
    "impetigo",
    "uuti",
]

for cond in conditions:
    measures.define_measure(
        name=f"eligible_{cond}",
        numerator=getattr(dataset, f"include_patient_{cond}"),
        denominator=base,
        group_by=group,
    )

# Overall eligibility
measures.define_measure(
    name="eligible_overall",
    numerator=dataset.include_patient_overall_eligible,
    denominator=base,
    group_by=group,
)

"""
=====================================================
Expected patterns for eligibility validation
=====================================================
These expectations are approximate and intended for validation, not strict thresholds.
-----------------------------------------------------
1. RAW CLINICAL FLAGS
-----------------------------------------------------

pregnant_this_month:
- Should be ~0 for males
- Concentrated in ages ~16–45
- Very low (<1–2%) outside reproductive age groups

catheter_status:
- Generally low prevalence (few % at most)
- Higher in older age groups (65+)

recurrent_uti_6m / recurrent_uti_12m:
- Should be relatively low (typically <5–10%)
- Higher in females than males
- Increasing with age

recurrent_uti:
- Should be >= recurrent_uti_6m
- Should be >= recurrent_uti_12m (combined logic)
- Should not exceed plausible clinical prevalence

bullous_impetigo_this_month:
- Very rare
- Likely close to 0 in most strata

recurrent_impetigo_this_year:
- Low prevalence
- Higher in children than adults

-----------------------------------------------------
2. ELIGIBILITY COMPONENTS
-----------------------------------------------------

uuti_eligible:
- Restricted to females only
- Age range strictly 16–64
- Should be 0 outside this range

uuti_exclusion:
- Subset of uuti_eligible population
- Driven by pregnancy, catheter, or recurrent UTI
- Should not exceed uuti_eligible

impetigo_exclusion:
- Small proportion of population
- Driven by:
    - bullous_impetigo_this_month
    - recurrent_impetigo_this_year
    - pregnancy in <16

sore_throat_exclusion / insect_bite_exclusion:
- Very small proportion overall
- Only applies to pregnant individuals <16

-----------------------------------------------------
3. FINAL ELIGIBILITY FLAGS
-----------------------------------------------------

eligible_uuti:
- Only females aged 16–64
- Should be <= uuti_eligible
- Reduction from uuti_eligible explained by exclusions

eligible_impetigo:
- Broad age range (>=1)
- Reduced by exclusion criteria
- Should not be extremely low

eligible_shingles:
- Only age >=18
- Slightly reduced by pregnancy exclusion

eligible_otitis_media:
- Only ages 1–17

eligible_sinusitis:
- Only age >=12

eligible_sore_throat:
- Age >=5
- Slight reduction in pregnant <16

eligible_insect_bites:
- Age >=1
- Slight reduction in pregnant <16

eligible_overall:
- Should be reasonably high (since union of conditions)
- But not close to 100%
- Should vary by age group

-----------------------------------------------------
4. GENERAL SANITY CHECKS
-----------------------------------------------------

- No unexpected values in males for female-specific conditions
- No eligibility outside defined age ranges
- No exclusion variable exceeding its eligible population
- Patterns should be smooth across age groups (no sharp discontinuities unless rule-based)

Any major deviation from these patterns should be investigated.
"""