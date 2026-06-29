library('tidyverse')

df_input <- read_csv(
  here::here("results_Arnaud", "dataset_Arnaud.csv.gz"),
  col_types = cols(patient_id = col_integer(),age = col_double())
)

plot_age<-df_input %>% 
 filter(!is.na(age)) %>%
  mutate(
    age_band = cut(
      age,
      breaks = seq(0, 120, 5),
      right = FALSE
    )
  ) %>%
  count(age_band) %>%
  ggplot(aes(age_band, n)) +
  geom_col(fill = "green") +
  #coord_flip() +
  labs(
    x = "Age band",
    y = "Patients",
    title = "Patients by age band"
  ) +
  theme_minimal()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) # Angled labels

ggsave(
  plot= plot_age,
  filename="age.png", path=here::here("results_Arnaud"),
)
