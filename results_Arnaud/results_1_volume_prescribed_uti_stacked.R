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
# Plot

# Monthly breaks
month_breaks <- seq(
  from = as.Date("2022-02-01"),
  to = max(national_monthly$month),
  by = "1 month"
)

# Labels: show year only under January
month_labels <- ifelse(
  month(month_breaks) == 1,
  paste0(format(month_breaks, "%b"), "\n", format(month_breaks, "%Y")),
  format(month_breaks, "%b")
)
#
p_trends_uti_stack <- ggplot(
  national_monthly |>
    filter(
      condition == "UTI",
      month >= as.Date("2022-02-01")
    ),
  aes(
    x = month,
    y = rate,
    fill = service
  )
) +
  geom_area(
    position = "stack",
    alpha = 0.8,
    colour = "white",
    linewidth = 0.2
  ) +
  geom_vline(
    xintercept = pf_launch,
    linetype = "dashed",
    colour = "black",
    linewidth = 0.7
  ) +
  annotate(
    "text",
    x = pf_launch,
    y = Inf,
    label = "Pharmacy First",
    angle = 90,
    vjust = 1.3,
    hjust = 1.05,
    size = 3
  ) +
  scale_x_date(
    breaks = month_breaks,
    labels = month_labels,
    expand = expansion(mult = c(0.01, 0.01))
  ) +
  #scale_y_continuous(labels = percent_format(accuracy = 0.1),expand = expansion(mult = c(0, 0.05))) +
  labs(
    title = "Monthly antimicrobial prescribing rate for uncomplicated urinary tract infection",
    subtitle = "Prescribing rates in General Practices and Community Pharmacies",
    x = NULL,
    y = "Prescribing rate",
    fill = "Service"
  ) +
  theme_minimal(base_size = 11) +
  theme(
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_line(colour = "grey90"),
    axis.text.x = element_text(angle = 0, hjust = 0.5, size = 8),
    axis.title.y = element_text(face = "bold"),
    legend.position = "top",
    plot.title = element_text(face = "bold", size = 13),
    plot.subtitle = element_text(size = 10)
  )
p_trends_uti_stack

ggsave(
  plot = p_trends_uti_stack,
  filename = "results_1_volume_prescribed_uti_stacked.png", path = here::here("results_Arnaud"),
)
