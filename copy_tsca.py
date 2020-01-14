import os
from datetime import datetime

# Global variables
from config import archive_directory_cluster
from config import results_directory_cluster
from config import results_directory_l_drive

# Temp variables
run_id = "191220_NB551415_0052_AHVVJVAFXY"


def parse_variables():
    variables = {}
    # Load variables files for all samples on the run
    for s in next(os.walk(os.path.join(results_directory_cluster, run_id, "IlluminaTruSightCancer")))[1]:
        current_variables = {}
        with open(os.path.join(results_directory_cluster, run_id, "IlluminaTruSightCancer", s,
                               f"{s}.variables")) as vf:
            for line in vf:
                split_line = line.rstrip().split("=")
                try:
                    current_variables[split_line[0]] = split_line[1]
                except IndexError:
                    pass
        variables[s] = current_variables
    return variables


def main():
    # Obtain current year
    yr = datetime.now().year

    # Check existence of results directory on L: and if not there, create it
    if not os.path.exists(os.path.join(results_directory_l_drive, f"{yr} Runs")):
        os.makedirs(os.path.join(results_directory_l_drive, f"{yr} Runs"))

    # Obtain worksheet id
    # Load variables files
    all_variables = parse_variables()

    # Extract worksheet id from variables files
    worksheets = []
    for s, d in all_variables.items():
        worksheets.append(d.get('worklistId'))
    worksheet_ids = list(set(worksheets))

    if len(worksheet_ids) != 1:
        raise Exception(f"Unable to identify the worksheet id for run {run_id}. Program Exiting.")

    worksheet_id = worksheet_ids[0]
    print(worksheet_id)


if __name__ == '__main__':
    main()