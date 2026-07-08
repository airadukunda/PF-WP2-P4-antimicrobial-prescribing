library("tidyverse")
library(readr)
library(dplyr)
#library(table1)
library(ggplot2)
library(lubridate)

df_input <- read_csv(
  here::here("output", "dataset_patients_combined.csv.gz"),
  col_types = cols(patient_id = col_integer(), age = col_double())
)

dataset_patients <- df_input %>%
  mutate(
    Period = case_when(
      .data$start_date < as.Date("2024-02-01") ~ "Pre-PF",
      TRUE ~ "Post-PF"
    )
  )
#Prescribing visualization

df <- dataset_patients %>%
  mutate(index_date = mdy(index_date))

cutoff <- as.Date("2024-02-01")

cutoff <- as.Date("2024-02-01")
plot_uti_pf <- ggplot(df, aes(index_date, numerator_pf_medication_uti)) +
  annotate("rect",
    xmin = min(df$index_date),
    xmax = cutoff,
    ymin = -Inf,
    ymax = Inf,
    fill = "lightblue",
    alpha = 0.2) +
  
  annotate("rect",
    xmin = cutoff,
    xmax = max(df$index_date),
    ymin = -Inf,
    ymax = Inf,
    fill = "lightgreen",
    alpha = 0.2) +
  
  geom_line(linewidth=0.6) +
  geom_point(size =2) +
  geom_vline(xintercept = cutoff,
    linetype = "dashed",
    color = "red") +
  scale_x_date(date_labels = "%Y %b", date_breaks = "1 month") +
  theme_minimal(base_size = 8)+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))+
  labs(
    x = "Year-Month",
    y = "Prescriptions",
    title = "Volume of antimicrobials prescribed  for uti in PF settings"
  ) 

#uti in GP 
plot_uti_gp <- ggplot(df, aes(index_date, numerator_gp_medication_uti)) +
  
  annotate("rect",
    xmin = min(df$index_date),
    xmax = cutoff,
    ymin = -Inf,
    ymax = Inf,
    fill = "lightblue",
    alpha = 0.2) +
  
  annotate("rect",
    xmin = cutoff,
    xmax = max(df$index_date),
    ymin = -Inf,
    ymax = Inf,
    fill = "lightgreen",
    alpha = 0.2) +
  
  geom_line(linewidth=0.6) +
  geom_point(size =2) +
  geom_vline(xintercept = cutoff,
    linetype = "dashed",
    color = "red") +
  scale_x_date(date_labels = "%Y %b", date_breaks = "1 month") +
  theme_minimal(base_size = 8)+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))+
  labs(
    x = "Year-Month",
    y = "Prescriptions",
    title = "Volume of antimicrobials prescribed  for uti in General practice settings"
  ) 

ggsave(
  plot = plot_uti_gp,
  filename = "1_results_volume_prescribed_uti.png", path = here::here("results_Arnaud"),
)
