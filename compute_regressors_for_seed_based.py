import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

np.set_printoptions(precision=2, suppress=True)

def compute_globalmean(folder, name) :
    RS = nib.load(folder + "sra" + name + "_brain_bpft.nii.gz")

    dRS = RS.get_fdata()
    hRS = RS.header
    aRS = RS.affine


    # Compute mean global signal (to use as confound)
    global_mean_course = np.zeros([dRS.shape[3]])
    for i in np.arange(dRS.shape[3]):
        idx = dRS[..., i] != 0   # average on voxels != 0
        global_mean_course[i] = np.mean(dRS[idx, i])


    # Compute RS normalized by mean global signal
    dRS_normglobmean = np.zeros(dRS.shape)
    for i in np.arange(dRS.shape[3]):
        idx = dRS[..., i] != 0
        dRS_normglobmean[idx, i] = dRS[idx, i] - global_mean_course[i]

    dRS_normglobmean_nii = nib.Nifti1Image(dRS_normglobmean, aRS, hRS)
    nib.save(dRS_normglobmean_nii, folder + "sra" + name + "_normglobmean.nii.gz")

    if not os.path.isdir(folder + 'ROI'):
        os.mkdir(folder + 'ROI')
    np.savetxt(folder + 'ROI/global_mean_timecourse.txt', global_mean_course)


    # Create folder for regressors needed for Seed Based analysis in Feat FSL
    folder_res = folder + "Res_SeedBased"
    if not os.path.isdir(folder_res):
        os.mkdir(folder_res)
    
    return dRS, dRS_normglobmean, global_mean_course, folder_res


def compute_timecourse(roi_path, dRS, dRS_normglobmean, global_mean_course, folder_res):

    folder = folder_res[:folder_res.rfind("/") + 1]
    roi_name = roi_path[roi_path.rfind("/") + 1 : roi_path.find(".nii")]

    roi = nib.load(folder + roi_path)
    droi = roi.get_fdata()

    # Compute ROI timecourse
    roi_course = dRS[droi == 1]
    roi_mean_course = np.mean(roi_course, axis = 0)
    # Compute ROI timecourse normalized by mean global signal
    roi_course_normglobmean = dRS_normglobmean[droi == 1]
    roi_mean_course_normglobmean = np.mean(roi_course_normglobmean, axis = 0)

    plt.figure()

    plt.subplot(311)
    plt.plot(roi_mean_course , label=roi_name)
    plt.legend()

    plt.subplot(312)
    plt.plot(roi_mean_course_normglobmean, label = roi_name + ' normalized by mean global signal')
    plt.legend()

    plt.subplot(313)
    plt.plot(global_mean_course , label='global mean')
    plt.legend()

    figure = plt.gcf()
    figure.set_size_inches(16, 8)
    plt.savefig(folder_res + "/" + roi_name + "_timecourse.png")
    plt.show()

    folder_res_roi = folder_res + "/" + roi_name
    if not os.path.isdir(folder_res_roi):
        os.mkdir(folder_res_roi)

    np.savetxt(folder + roi_name + "_timecourse.txt", roi_mean_course)
    # save a copy of roi.nii and timecourse.txt in the folder where the Seed Based Feat analysis will be be run
    nib.save(roi, folder_res_roi + "/" + roi_name + ".nii.gz")
    np.savetxt(folder_res_roi + "/" + roi_name + "_timecourse.txt", roi_mean_course)
    print('Timecourse files are saved in ' + folder_res)