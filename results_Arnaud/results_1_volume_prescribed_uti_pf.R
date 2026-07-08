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

df_input<- df_input %>%
  mutate(
    Period = case_when(
      .data$start_date < as.Date("2024-02-01") ~ "Pre-PF",
      TRUE ~ "Post-PF"
    )
  )
#Prescribing visualization

df <- df_input %>%
  mutate(index_date = mdy(index_date))

pf_start <- as.Date("2024-02-01")

pf_start <- as.Date("2024-02-01")
plot_uti_pf <- ggplot(df, aes(index_date, numerator_pf_medication_uti)) +
  annotate("rect",
    xmin = min(df$index_date),
    xmax = pf_start,
    ymin = -Inf,
    ymax = Inf,
    fill = "lightblue",
    alpha = 0.2) +
  
  annotate("rect",
    xmin = pf_start,
    xmax = max(df$index_date),
    ymin = -Inf,
    ymax = Inf,
    fill = "lightgreen",
    alpha = 0.2) +
  
  geom_line(linewidth=0.6) +
  geom_point(size =2) +
  geom_vline(xintercept = pf_start,
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

#Save
plot_uti_pf <- ggplot(df, aes(x = index_date, y = numerator_pf_medication_uti)) +

  geom_line(linewidth = 0.7, colour = "black") +
  geom_point(size = 2) +

  geom_vline(
    xintercept = pf_start,
    linetype = "dashed",
    colour = "red",
    linewidth = 0.8
  ) +

  annotate(
    "text",
    x = pf_start,
    y = max(df$numerator_pf_medication_uti) * 1.02,
    label = "Pharmacy First",
    colour = "red",
    angle = 90,
    vjust = -0.4,
    size = 3
  ) +

  scale_x_date(
    date_labels = "%Y\n%b",
    date_breaks = "2 months",
    expand = expansion(mult = c(0.01, 0.02))
  ) +

  labs(
    title = "Volume of antimicrobial prescriptions for UTI in Pharmacy First settings",
    x = "Year-Month",
    y = "Number of prescriptions"
  ) +

  theme_minimal(base_size = 10) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    plot.title = element_text(face = "bold", hjust = 0.5),
    panel.grid.minor = element_blank()
  )
ggsave(
  plot = plot_uti_pf,
  filename = "results_1_volume_prescribed_uti_gp.png", path = here::here("results_Arnaud"),
)
