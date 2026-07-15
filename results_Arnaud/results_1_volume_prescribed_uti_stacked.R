library("tidyverse")
library(readr)
library(dplyr)
#library(table1)
library(ggplot2)
library(lubridate)

df <- read_csv(
  here::here("output", "data_patients_measures_Arnaud.csv"),
  col_types = cols(patient_id = col_integer(), age = col_double())
)

df <-df %>%
  mutate(
    month = ymd(month),
    interval_start = ymd(interval_start),
    interval_end   = ymd(interval_end)
  ) %>%
  extract(
    measure,
    into = c("service", "condition"),
    regex = "^(pf|gp)_medication_(.+)$",
    remove = FALSE
  ) %>%
  mutate(
    service   = factor(service, levels = c("gp", "pf"),
                        labels = c("GP", "PF")),
    condition = factor(condition,
                        levels = c("uti", "sinusitis", "insectbite",
                                   "otitismedia", "sorethroat",
                                   "shingles", "impetigo"),
                        labels = c("UTI", "Sinusitis", "Insect bite",
                                   "Otitis media", "Sore throat",
                                   "Shingles", "Impetigo"))
  )

## ---- 1b. Add "All conditions" as an extra condition level -----
condition_levels <- c("All conditions", "UTI", "Sinusitis", "Insect bite",
                       "Otitis media", "Sore throat", "Shingles", "Impetigo")

## Sums numerator/denominator across the 7 conditions, per practice x
## month x service, then re-derives the ratio. Binding this in here
## (rather than only at the national-aggregate stage) means it also
## flows through the practice-level spread plot and the ITS models.
df_all_conditions <- df %>%
  group_by(practice, month, service) %>%
  summarise(
    numerator      = sum(numerator, na.rm = TRUE),
    denominator    = sum(denominator, na.rm = TRUE),
    interval_start = first(interval_start),
    interval_end   = first(interval_end),
    .groups = "drop"
  ) %>%
  mutate(
    ratio     = numerator / denominator,
    condition = "All conditions",
    measure   = paste0(if_else(service == "Pharmacy First", "pf", "gp"),
                        "_medication_all")
  )

df <- df %>%
  mutate(condition = as.character(condition)) %>%
  bind_rows(df_all_conditions) %>%
  mutate(condition = factor(condition, levels = condition_levels))

## Pharmacy First national rollout date (England, 31 Jan 2024)
pf_launch <- ymd("2024-01-31")

## ---- 2. National monthly rates (denominator-weighted) --------
## Weighted mean across practices = sum(numerator)/sum(denominator)
## This is the correct way to pool practice-level ratios (avoids
## giving equal weight to small and large practices).
national_monthly <- df %>%
  group_by(month, service, condition) %>%
  summarise(
    numerator   = sum(numerator, na.rm = TRUE),
    denominator = sum(denominator, na.rm = TRUE),
    n_practices = n_distinct(practice),
    .groups = "drop"
  ) %>%
  mutate(rate = numerator / denominator)
#3. Time series plots: pf vs gp, per condition ------------
p_trends <- ggplot(national_monthly,
                    aes(x = month, y = rate, colour = service,shape=service)) +
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
    title = "Antimicrobial prescribing rate by condition in GP and   Pharmacy First settings",
    subtitle = "Dashed line = national Pharmacy First rollout (31 Jan 2024)",
    x = NULL, y = "Prescribing rate",
    colour = NULL
  ) +
  theme_minimal(base_size = 8) +
  theme(axis.text.x = element_text(angle = 80, hjust = 1),
        legend.position = "top")

p_trends
p_trends_all <- ggplot(national_monthly|>
    filter(condition =="All conditions"),
  aes(x = month, y = rate, colour = service,shape=service)) +
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
    title = "Antimicrobial prescribing rate for all the seven PF conditions ",
    subtitle = "Dashed line = national Pharmacy First rollout (31 Jan 2024)",
    x = NULL, y = "Prescribing rate",
    colour = NULL
  ) +
  theme_minimal(base_size = 8) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "top")
p_trends_all
#
# Pharmacy First launch date
pf_launch <- as.Date("2024-02-01")

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

# Plot

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
