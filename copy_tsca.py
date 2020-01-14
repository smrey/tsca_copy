import os
from datetime import datetime
import shutil
import tkinter as tk
from tkinter import ttk

# Global variables
from config import archive_directory_cluster
from config import results_directory_cluster
from config import results_directory_l_drive
from config import ntc_name
from config import ntc_directories
from config import ntc_files
from config import sample_directories
from config import sample_files

# Temp variables
#run_id = "191220_NB551415_0052_AHVVJVAFXY"


def parse_variables(run_id):
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


def copy_sample(yr, run_id, worksheet_id, s):
    if sample_files:
        origin_path = os.path.join(results_directory_cluster, run_id, "IlluminaTruSightCancer", s)
        for f in sample_files:
            # Copy files from cluster to L: drive
            shutil.copy2(os.path.join(origin_path, f"{run_id}_{s}_{f}"),
                         os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, s))
    if sample_directories:
        for d in sample_directories:
            if not os.path.exists(os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, s, d)):
                os.makedirs(os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, s, d))
            # Copy directory files
            for f in os.listdir((os.path.join(archive_directory_cluster, run_id, d))):
                shutil.copy2(os.path.join(archive_directory_cluster, run_id, d, f),
                             os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, s, d))
    return "Copy successful"


def copy_ntc(yr, run_id, worksheet_id, s):
    if ntc_files:
        for f in ntc_files:
            shutil.copy2(os.path.join(archive_directory_cluster, run_id, f),
                         os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, s))
        for d in ntc_directories:
            # Make directory
            if not os.path.exists(os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, s, d)):
                os.makedirs(os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, s, d))
            # Copy directory files
            for f in os.listdir((os.path.join(archive_directory_cluster, run_id, d))):
                shutil.copy2(os.path.join(archive_directory_cluster, run_id, d, f),
                             os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, s, d))
    return "Copy successful"


def main():
    # Start pop-up
    '''
    root = tk.Tk()
    root.wm_title("TSCa file copy")
    root.label = ttk.Label(text="Software is working. Please wait.")
    root.label.grid(column=0,  row=0)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    from box import MyEntryWindow
    w = MyEntryWindow(root)
    try:
        run_id = w.run_id
    except AttributeError:
        raise AttributeError(f"Run id entry was not entered correctly. Please start again.")
    '''
    run_id = "191220_NB551415_0052_AHVVJVAFXY" #TODO temp
    # Obtain current year
    yr = datetime.now().year

    # Check existence of results directory on L: and if not there, create it
    if not os.path.exists(os.path.join(results_directory_l_drive, f"{yr} Runs")):
        os.makedirs(os.path.join(results_directory_l_drive, f"{yr} Runs"))

    # Obtain worksheet id
    # Load variables files
    all_variables = parse_variables(run_id)

    # Extract worksheet id from variables files
    worksheets = []
    for s, d in all_variables.items():
        worksheets.append(d.get('worklistId'))
    worksheet_ids = list(set(worksheets))

    if len(worksheet_ids) != 1:
        raise Exception(f"Unable to identify the worksheet id for run {run_id}. Program Exiting.")

    # Remove " from worksheet id for downstream use
    worksheet_id = worksheet_ids[0].split('"')[1]

    # Make directory named after worksheet on L:
    if not os.path.exists(os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id)):
        os.makedirs(os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id))

    # Copy data from cluster to L: drive
    try:
        for sample in next(os.walk(os.path.join(results_directory_cluster, run_id, "IlluminaTruSightCancer")))[1]:
            # Make directory named after sample on L: drive
            if not os.path.exists(os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, sample)):
                os.makedirs(os.path.join(results_directory_l_drive, f"{yr} Runs", worksheet_id, sample))
            if sample != ntc_name:
                copy_sample(yr, run_id, worksheet_id, sample)
            else:
                copy_ntc(yr, run_id, worksheet_id, sample)
    except:
        raise AttributeError(f"Invalid run ID. Please check and try again.")

    # Rename sample directories on L: drive with order
    


if __name__ == '__main__':
    main()