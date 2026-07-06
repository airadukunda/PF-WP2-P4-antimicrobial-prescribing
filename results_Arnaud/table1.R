
library(table1)
library(dplyr)
library(readr)
library(knitr)
library(tidyverse)
library(here)
library(rmarkdown)
df_input <- read_csv(
  here::here("output", "dataset_patients_combined.csv.gz"),
  col_types = cols(patient_id = col_integer(), age = col_double())
)
data <-data.frame(df_input)
names(data)
library(dplyr)

data <- data %>%
  mutate(
    Period = case_when(
      .data$start_date < as.Date("2024-02-01") ~ "Pre-PF",
      TRUE ~ "Post-PF"
    )
  )



table_1<-table1(
  ~ age + sex + ethnicity + region |
    imd,
  data = data
)
rmarkdown::render(
  input = "analysis/table_1.R",
  output_file = "table_1.html",
  output_dir = "output"
)

