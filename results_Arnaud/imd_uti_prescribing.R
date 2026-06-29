library(tidyverse)

df_input <- read_csv(
  here::here("results_Arnaud", "dataset_Arnaud.csv.gz"),
  col_types = cols(
    patient_id = col_integer(),
    age = col_double()
  )
)
# Assuming you have a column for UTI prescription (e.g., uti_prescription, antibiotic_uti, or similar)
# Replace "uti_prescription" with your actual column name
plot_uti_imd <- df_input %>%
  filter(factor(imd)!= "Missing")%>%
  group_by(imd) %>%
  summarise(
    total_patients = n(),
    uti_prescriptions = sum(numerator_gp_medication_uti, na.rm = TRUE),  # Replace with your column name
    prescription_rate = uti_prescriptions / total_patients * 100
  ) %>%
  ggplot(aes(x = factor(imd), y = prescription_rate)) +
  geom_col(fill = "steelblue") +
  labs(
    title = "UTI Prescription Rate by IMD Quintile",
    x = "IMD Quintile (1 = most deprived)",
    y = "UTI Prescription Rate (%)"
  ) +
  theme_minimal(base_size = 14) +
  geom_text(aes(label = paste0(round(prescription_rate, 1), "%")), 
    vjust = -0.5, 
    size = 4)

ggsave(
  plot = plot_uti_imd,
  filename = "imd_uti_prescribing.png",
  path = here::here("results_Arnaud"),
  width = 7,
  height = 5,
  dpi = 300
)