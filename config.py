import os

# Paths
'''
archive_directory_cluster = os.path.join(os.sep, "A:", os.sep, "nextseq")
results_directory_cluster = os.path.join(os.sep, "W:", os.sep)
results_directory_l_drive = os.path.join(os.sep, "L:", os.sep, "NGS ANALYSIS", "TruSightCancer")
'''
archive_directory_cluster = os.path.join(os.sep, "Users", "sararey", "Documents", "tsca", "raw")
results_directory_cluster = os.path.join(os.sep, "Users", "sararey", "Documents", "tsca")
results_directory_l_drive = os.path.join(os.sep, "Users", "sararey", "Documents", "tsca", "results")


ntc_names = ["NTC"]
ntc_directories = ["InterOp"]
ntc_files = ["RunInfo.xml", "RunParameters.xml"]
sample_directories = []
sample_files = ["customClinicalCoverageTargetCoverage.txt", "customGaps.bed"]
cnv_files = ["cnvReport.csv"]
