import numpy as np
import nibabel as nib

folder = '../RestingState/'
filename = folder + 'meanaRS_mask.nii'

mask = nib.load(filename)
file_format = filename[-3:]
filename_corr = filename[:filename.rfind(".nii")]  + "_corr.nii"

dmask = mask.get_fdata()
hmask = mask.header
amask = mask.affine

dmask[dmask!=0] = 1.0 

mask_corrected_nii = nib.Nifti1Image(dmask, amask, hmask)
nib.save(mask_corrected_nii, filename_corr)


# RS = nib.load(folder + 'raRS.nii')
# dRS = RS.get_fdata()
# hRS = RS.header
# aRS = RS.affine
# 
# # dRS[dRS<0.01]=0.01
# dRS = dRS + 1.0
# 
# RS_corrected_nii = nib.Nifti1Image(dRS, aRS, hRS)
# nib.save(RS_corrected_nii, folder + 'raRS_thr0.nii.gz')








