library(tidyverse)
library(here)

# ----------------------------------------------------------------------
# 1. Read the data
# ----------------------------------------------------------------------
df_input <- read_csv(
  here::here("results_Arnaud", "dataset_Arnaud.csv.gz"),
  col_types = cols(
    prescribing    = col_character(),
    interval_start = col_date(format = "%Y-%m-%d"),
    interval_end   = col_date(format = "%Y-%m-%d"),
    ratio          = col_double(),
    numerator      = col_integer(),
    denominator    = col_integer(),
    practice       = col_integer(),
    month          = col_date(format = "%Y-%m-%d")
  )
)

# (Optional) convert to tibble – no need for as.data.frame()

# ----------------------------------------------------------------------
# 2. Average ratio per practice for the UTI measure only
# ----------------------------------------------------------------------
avg_ratio_uti <- df_input %>%
  filter(measure == "gp_prescribing_rate_uti") %>%   # exact column name? check
  group_by(practice) %>%
  summarise(mean_ratio = mean(ratio, na.rm = TRUE), .groups = "drop")

# ----------------------------------------------------------------------
# 3. Bar chart – now with correct x variable
# ----------------------------------------------------------------------
avg_ratio_uti <- avg_ratio_uti %>%
  ggplot(aes(x = reorder(practice, mean_ratio), y = mean_ratio)) +
  geom_col(fill = "steelblue") +
  coord_flip() +
  labs(
    title = "Average prescribing ratio for UTI (by practice)",
    x = "Practice ID",
    y = "Mean ratio"
  ) +
  theme_minimal(base_size = 12)

# Save
ggsave(
  plot = avg_ratio_uti,
  filename = "avg_ratio_uti.png",
  path = here::here("results_Arnaud"),
  width = 8,
  height = 6,
  dpi = 300
)
# ----------------------------------------------------------------------
# 4. Time series – for all prescribing measures (or filter to UTI)
# ----------------------------------------------------------------------
avg_ratio_month <- df_input %>%
  # filter(measure == "gp_prescribing_rate_uti") %>%
  group_by(month, measure) %>%
  summarise(mean_ratio = mean(ratio, na.rm = TRUE), .groups = "drop")

plot_time <- avg_ratio_month %>%
  ggplot(aes(x = month, y = mean_ratio, colour = measure)) +
  geom_line() +
  geom_point(size = 0.8) +
  labs(
    title = "Average prescribing ratio over time",
    x = "Month",
    y = "Mean ratio"
  ) +
  theme_minimal(base_size = 12) +
  theme(legend.position = "bottom")

ggsave(
  plot = plot_time,
  filename = "ratio_time_series.png",
  path = here::here("results_Arnaud"),
  width = 10,
  height = 6,
  dpi = 300
)