
pacman::p_load(tidyverse,here)
# Read measures
data <- read_csv(
  here("results_Arnaud", "measures_Arnaud.csv.gz")
)
#Prescribing rate
uti <- data %>%
  mutate(
    prescribing_rate = 100 * pf_uti_medication_count /
      pf_uti_consultation_count
  )

# plot
plot_uti <- ggplot(
  data = uti,
  aes(x = interval_start, y = prescribing_rate)
) +
  geom_line(linewidth = 1.2, colour = "#0072B2") +
  geom_point(size = 2, colour = "#0072B2") +
  scale_y_continuous(
    limits = c(0, 100),
    labels = scales::label_percent(scale = 1)
  ) +
  labs(
    title = "Monthly antibiotic prescribing rate for UTI",
    subtitle = "Pharmacy First consultations",
    x = "Month",
    y = "Prescribing rate (%)"
  ) +
  theme_minimal(base_size = 14)

# Display the plot
print(plot_uti)

# Save the plot
ggsave(
  plot = plot_uti, 
  filename = "uti_prescribing_rate.png",
  path = here("results_Arnaud"),
  width = 8,
  height = 5,
  dpi = 300
)
