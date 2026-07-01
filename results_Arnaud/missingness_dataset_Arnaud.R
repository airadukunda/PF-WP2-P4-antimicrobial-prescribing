library("tidyverse")
library("gridExtra")
library("readr")
#install.packages("DataExplorer") # Not sure if the packages is available/supported in OpenSafely

install.packages("DataExplorer", dependencies = TRUE)
library("DataExplorer")
df_input <- read_csv(
  here::here("results_Arnaud", "dataset_Arnaud.csv.gz"),
  col_types = cols(patient_id = col_integer(),age = col_double())
)
data <-data.frame(df_input)
names(data)
analytic.miss <- as.data.frame(data)
# DataExploreration
plot_1<-plot_missing(analytic.miss)
analytic.miss_1 <- analytic.miss[, colSums(is.na(analytic.miss)) > 0]
plot_2<-plot_missing(analytic.miss_1)
#
figure<-grid.arrange(
  plot_1, plot_2,
  ncol = 2
)
ggsave(
  filename = "results_Arnaud/missingness_dataset_Arnaud.png",
  plot = figure,
  width = 14,
  height = 10,
  dpi = 300
)
