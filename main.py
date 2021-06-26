# Main script for Resting State fMRI preprocessing
from bandpassfilter_recoverbrain import bpft
from compute_regressors_for_seed_based import compute_globalmean, compute_timecourse

#  The following files must already be in "YourFolder" :
# "sraRSYourName.nii"          # Resting State preprocessed with slice timing, reealignement smoothing. 
# "meanaRSYourName_mask.nii"   # Brain mask
# "meanaRSYourName.nii"        # Mean Resting State image

# Define your working folder
datapath = "YourFolder/YourData.nii"
# Examle : "../DATA/RestingState/RS_Frida3Mois"

# Define the the Nifti ROI you want to use in Seed Based analysis
# It should be placed in YourFolder/ROI
roi_path = "ROI/YourRoi.nii"

folder = datapath[:datapath.rfind("/") + 1]
name = datapath[datapath.rfind("/") + 1 : datapath.find(".nii")]

# Band pass filter fMRI data
bpft(folder, name)

# Compute mean global signal (to use as confound in GLM)
dRS, dRS_normglobmean, global_mean_course, folder_res = compute_globalmean(folder, name)
# Compute mean timecourse of selected ROI
compute_timecourse(roi_path, dRS, dRS_normglobmean, global_mean_course, folder_res)


