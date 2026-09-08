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
#
p_trends_all_pf_conditions <- ggplot(national_monthly|>
    filter(condition =="All conditions",month>="2022-02-01"),
  aes(x = month, y = numerator, colour = service,shape=service)) +
  geom_line(linewidth = 0.5) +
  geom_point(size = 1.2) +
  geom_vline(xintercept = as.numeric(pf_launch),
    linetype = "dashed", colour = "grey40") +
  facet_wrap(~ condition, scales = "free_y", ncol = 4) +
  scale_x_date(
    limits = range(national_monthly$month),
    date_breaks = "1 month",
    date_labels = "%Y-%m",
    expand = expansion(mult = 0.01)
  )+
  #scale_y_continuous(labels = percent_format(accuracy = 0.1)) +
  labs(
    title = "Antimicrobial prescribing rate for all PF conditions",
    subtitle = "Dashed line = national Pharmacy First rollout (31 Jan 2024)",
    x = NULL, y = "Prescribing rate",
    colour = NULL
  ) +
  theme_minimal(base_size = 8) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "top")
#
p_trends_all_pf_conditions

ggsave(
  plot = p_trends_all_pf_conditions,
  filename = "results_1_volume_prescribed_all_pf_conditions.png", path = here::here("results_Arnaud"),
)
