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

heatmap <- ggplot(
   national_monthly %>%
     filter(!is.na(condition),
       month  > as.Date("2025-10-01")),
   aes(x = month,
     y = condition,
     fill = rate)
 ) +
   geom_tile() +
   facet_wrap(~service) +
   scale_fill_gradient(low = "white", high = "darkblue") +
   scale_x_date(
     date_breaks = "1 month",
     date_labels = "%Y-%m"
   ) +
   labs(
     x = "Month",
     y = "Condition",
     fill = "rate"
   ) +
   theme_minimal() +
   theme(
     axis.text.x = element_text(angle = 60, hjust = 1)
  )
#
heatmap
ggsave(
  plot = heatmap,
  filename = "results_1_practice_level_prescribing_rate_heatmap.png", path = here::here("results_Arnaud"),
)
