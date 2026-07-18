library("tidyverse")
library(readr)
library(dplyr)
#library(table1)
library(ggplot2)
library(lubridate)

data <- read_csv(
  here::here("output", "data_patients_measures_Arnaud.csv"),
  col_types = cols(patient_id = col_integer(), age = col_double())
)

df <- data %>%
  mutate(
    month = ymd(month),
    interval_start = ymd(interval_start),
    interval_end = ymd(interval_end)
  ) %>%
  extract(
    measure,
    into = c("service", "condition"),
    regex = "^(pf|gp)_medication_(.+)$",
    remove = FALSE
  ) %>%
  mutate(
    service = factor(
      service,
      levels = c("gp", "pf"),
      labels = c("GP", "PF")
    ),
    condition = factor(
      condition,
      levels = c(
        "uti",
        "sinusitis",
        "insectbite",
        "otitismedia",
        "sorethroat",
        "shingles",
        "impetigo",
        "acutebronchitis_control",
        "conjunctivitisallergic_control",
        "vulvovaginalcandidiasis_control",
        "all_conditions"
      ),
      labels = c(
        "UTI",
        "Sinusitis",
        "Insect bite",
        "Otitis media",
        "Sore throat",
        "Shingles",
        "Impetigo",
        "Acute bronchitis (Control)",
        "Allergic conjunctivitis (Control)",
        "Vulvovaginal candidiasis (Control)",
        "All conditions"
      )
    ),
    group = case_when(
      condition %in% c(
        "Acute bronchitis (Control)",
        "Allergic conjunctivitis (Control)",
        "Vulvovaginal candidiasis (Control)"
      ) ~ "Control",
      
      condition == "All conditions" ~ "Overall",
      
      TRUE ~ "Pharmacy First"
    ),
    group = factor(
      group,
      levels = c("Pharmacy First", "Control", "Overall")
    )
 )
#PF start
pf_launch <- ymd("2024-02-01")
#------2.National monthly metrics (denominator-weighted) --------
national_monthly <- df %>%
  group_by(month, service, condition) %>%
  summarise(
    numerator   = sum(numerator, na.rm = TRUE),
    denominator = sum(denominator, na.rm = TRUE),
    n_practices = n_distinct(practice),
    .groups = "drop"
  ) %>%
  mutate(rate = numerator / denominator)
#
latest_month <- max(national_monthly$month)
table(national_monthly$month)
p_jan_2026 <- national_monthly %>%
  filter(month == latest_month, denominator > 0) %>%
  ggplot(aes(x = condition, y = rate, fill = service)) +
  geom_boxplot(outlier.alpha = 0.3, position = position_dodge(0.8)) +
  #scale_y_continuous(labels = percent_format(accuracy = 1)) +
  labs(
    title = paste("Practice-level prescribing rate distribution,", format(latest_month, "%b %Y")),
    x = NULL, y = "Rate", fill = NULL
  ) +
  theme_minimal(base_size = 11) +
  theme(axis.text.x = element_text(angle = 30, hjust = 1), legend.position = "top")
#
p_jan_2026

ggsave(
  plot = p_jan_2026,
  filename = "results_1_practice_level_prescribing_rate_distribution.png", path = here::here("results_Arnaud"),
)
