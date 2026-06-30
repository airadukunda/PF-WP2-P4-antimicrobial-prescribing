library(tidyverse)

df <- read_csv(
  here::here("results_Arnaud", "dataset_Arnaud.csv.gz"),
  col_types = cols(
    patient_id = col_integer(),
    age = col_double()
  )
)
df<-as.data.frame(df)

df <- df %>%
  filter(numerator_gp_medication_uti > 0) %>%
  group_by(index_date, sex, age_band) %>%
  summarise(
    count = n(),
    .groups = "drop"
  )

ggplot(df,
  aes(x = index_date,
    y = numerator_gp_medication_uti,
    colour = sex)) +
  geom_line(linewidth = 1) +
  facet_wrap(~age_band) +
  labs(
    title = "GP UTI medication prescribing over time",
    x = NULL,
    y = "Number of prescriptions"
  ) +
  theme_minimal()
#
plot_uti <- df %>%
  ggplot() +
  geom_area(
    aes(
      x = index_date,
      y = numerator_gp_medication_uti,
      fill = age_band
    ),
    stat = "identity"
  ) +
  facet_wrap(~imd) +
  scale_fill_viridis_d() +
  labs(
    title = "GP UTI medication prescriptions",
    x = NULL,
    y = "Count"
  ) +
  theme_minimal()

  # Save the plot
ggsave(
  filename = "results_Arnaud/medications_vol_uti.png",
  plot = plot_uti,
  width = 10,
  height = 6
)
