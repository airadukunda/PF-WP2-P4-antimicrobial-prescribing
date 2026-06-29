library(tidyverse)
library(lubridate)
library(here)
# 1. Read the data
df_input <- read_csv(
  here::here("results_Arnaud", "measures_Arnaud.csv"))
  
df <- as.data.frame(df_input) 

df_uti <- df %>%
  filter(
    str_detect(measure, "gp_prescribing_rate_uti|pf_prescribing_rate_uti")
  )

# Clean labels for plotting
df_plot <- df_uti %>%
  mutate(
    setting = case_when(
      str_detect(measure, "^gp_") ~ "GP",
      str_detect(measure, "^pf_") ~ "Community Pharmacy",
      TRUE ~ "Other"
    ),
    interval_start = as.Date(interval_start)
  ) %>%
  group_by(setting, interval_start) %>%
  summarise(
    prescription_rate = mean(ratio, na.rm = TRUE),
    .groups = "drop"
  )

# Plot
p <- ggplot(df_plot, aes(x = interval_start, y = prescription_rate, color = setting)) +
  geom_line(linewidth = 1) +
  geom_point() +
  labs(
    title = "UTI prescribing rate: GP vs Community Pharmacy",
    x = "Time (2-month intervals)",
    y = "Prescribing rate"
  ) +
  theme_minimal()

ggsave("results_Arnaud/gp_prescribing_rate_uti.png", p, width = 10, height = 6)