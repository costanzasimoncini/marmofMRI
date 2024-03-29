# Main script for Resting State fMRI preprocessing
from bandpassfilter_recoverbrain import bpft
from compute_regressors_for_seed_based import compute_globalmean, compute_timecourse

#  The following files must already be in "YourFolder" :
# "sraYourData.nii"          # Resting State preprocessed with slice timing, reealignement smoothing. 
# "meanaYourData_mask.nii"   # Brain mask
# "meanaYourData.nii"        # Mean Resting State image

# Define tha path of your fMRI data
# Example: 
datapath = "YourFolder/YourData.nii"

# Define the the Nifti ROI you want to use in Seed Based analysis
# It should be placed in YourFolder/ROI
# Examples: 
roi_path1 = "ROI/roi1.nii.gz"
roi_path2 = "ROI/roi2.nii.gz"


folder = datapath[:datapath.rfind("/") + 1]
name = datapath[datapath.rfind("/") + 1 : datapath.find(".nii")]

# Band pass filter fMRI data
bpft(folder, name)

# Compute mean global signal (to use as confound in GLM)
dRS, dRS_normglobmean, global_mean_course, folder_res = compute_globalmean(folder, name)
# Compute mean timecourse of selected ROI
compute_timecourse(roi_path1, dRS, dRS_normglobmean, global_mean_course, folder_res)
compute_timecourse(roi_path2, dRS, dRS_normglobmean, global_mean_course, folder_res)