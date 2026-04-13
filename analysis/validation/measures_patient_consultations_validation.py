# PF consultations, GP consultations, A&E, appointment: total and by condition

'''
Appointment: 
- Appointment_scheduled: count the number of appointments that were scheduled within this month based on the appointment start_date, include statues such as Arrived, Visit etc - reflect overall appointment demand regardless of whether the patient was actually seen
- Appointment_seen: count the number of appointments that were recorded as seen … use the same set of statues -- indicate appointment was actually processed or attended
? is appointment_scheduled == appointment_seen? 
- - > Expect this to be slightly different - some appointments may be rescheduled to a date that is in another month.
'''


'''
PF consultation count:
? is numerator_pf_event_{condition} == numerator_pf_consultation_{condition} >= numerator_pf_episode_{condition}?
- - > for validating which method to use for counting number of consultations

- pf_consultation_general: the total number of PF consultations per patient
- pf_consultation_general_butno_condition: PF consultations that have no associated PF condition code
? is (pf_consultation_general - pf_consultation_general_butno_condition) 
        == 
        sum(numerator_pf_consultation_{condition})?
- - > may not be. sanity check - to decide on which metric to use as total PF consultation count


- For PF consultations, assigned each consultation to a single type (face-to-face, online, or telephone) using a priority rule (face-to-face > online > telephone), and grouped the remaining as unknown. This ensures that consultation types form a complete partition of PF consultations.
? is pf_consultation_general == pf_consultation_f2f + pf_consultation_online + pf_consultation_telephone + pf_consultation_unknowntype? 
- - > This should be equal.
'''


'''
GP consultation count:
- is sum(numerator_gp_consultation_{condition}) >= 
     (gp_pf_consultation_f2f + gp_pf_consultation_online + gp_pf_consultation_telephone + gp_pf_consultation_unknowntype)?
- - > may be more than - one consultation may include many conditions
'''