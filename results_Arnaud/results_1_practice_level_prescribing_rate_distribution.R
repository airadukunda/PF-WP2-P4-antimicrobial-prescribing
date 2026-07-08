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
# Here we want try to  to pool practice-level ratios (avoids equal weight to small and large practices).
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
p_trends_uti <- ggplot(national_monthly|>
    filter(condition =="UTI",month>="2022-02-01"),
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
    title = "Antimicrobial prescribing rate for uncomplicated urinary infections",
    subtitle = "Dashed line = national Pharmacy First rollout (31 Jan 2024)",
    x = NULL, y = "Prescribing rate",
    colour = NULL
  ) +
  theme_minimal(base_size = 8) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "top")
#
p_trends_uti

latest_month <- max(df$month)
table(df$month)
p_jan_2026 <- df %>%
  filter(month == latest_month, denominator > 0) %>%
  ggplot(aes(x = condition, y = ratio, fill = service)) +
  geom_boxplot(outlier.alpha = 0.3, position = position_dodge(0.8)) +
  #scale_y_continuous(labels = percent_format(accuracy = 1)) +
  labs(
    title = paste("Practice-level prescribing rate distribution,", format(latest_month, "%b %Y")),
    x = NULL, y = "Rate", fill = NULL
  ) +
  theme_minimal(base_size = 11) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), legend.position = "top")
#
p_jan_2026

ggsave(
  plot = p_jan_2026,
  filename = "results_1_practice_level_prescribing_rate_distribution.png", path = here::here("results_Arnaud"),
)
