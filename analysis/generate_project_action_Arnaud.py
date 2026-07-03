from datetime import date
import yaml
import config
from config import month_range

# utilisation: python analysis/generate_project_action.py > project_test.yaml

# a.Montly datasets generation :
# Here we ill use :python analysis/generate_project_action_Arnaud.py > project_test_Arnaud.yaml
#Sepcifically, we will run "python analysis/generate_project_action_Arnaud.py > project_test_Arnaud.yaml" in  terminal 
#Where:
# 1.generate_project_action_Arnaud.py: use dataset definition_Arnaud designed for protocol 4 yaml actions needed to generate monthly datasets between dates specified in config.py
# 2.project_test_Arnaud.yaml : store the generated actions  in 1.These actions will be copied in project.yaml,which is the principal yml project for our analysis.
# For more details :Refer to weiyao monthly data generation and aggregation on my ORCiD .
# start_dates = ["2024-02-01", "2024-03-01"]
# b.Monthly datasets agggregation
#Run "python analysis/preprocess_combine_gz_Arnaud.py" in terminal :but make sure we use "start_dates = month_range(config.start, config.end)" in preprocess.
start_dates = month_range(config.start, config.end)

project = {
    "version": "5.0",    # 5.0 instead 4.0
    "actions": {
        "generate_dataset": {  #-->Here we used dataset definition specific for the protocol 4.
            "run": "ehrql:v1 generate-dataset analysis/dataset_definition_patients_Arnaud.py --output output/dataset_patients.csv.gz",
            "outputs": {"highly_sensitive": {"dataset": "output/dataset_patients.csv.gz"}}
        }
    }
}

for d in start_dates:
    d_str = d.isoformat()
    action_name = f"generate_patient_dataset_{d_str.replace('-', '_')}"
    project["actions"][action_name] = {
        "run": f"ehrql:v1 generate-dataset analysis/dataset_definition_patients_Arnaud.py --dummy-tables dummy_tables --output output/dataset_patients_{d_str}.csv.gz -- --start_date {d_str}",
        "outputs": {
            "highly_sensitive": {
                "dataset": f"output/dataset_patients_{d_str}.csv.gz"
            }
        }
    }

print(yaml.dump(project, sort_keys=False))