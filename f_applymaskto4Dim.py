# import os
import numpy as np
import nibabel as nib
# import matplotlib.pyplot as plt
# from nilearn import image
# from nilearn.masking import apply_mask


# folder = '/Users/costanza/workspace/PROJETS/fMRI_Jacquette/pretraitementsRS/data/'
# RS = nib.load(folder + 'raRS_bc.nii.gz')
# mask = nib.load(folder + 'rT2_mask_resT2corr.nii.gz')

def apply_mask_4D_nibabel(RS, mask):

    dRS = RS.get_fdata()
    dmask = mask.get_fdata()
    
    hRS = RS.header
    # hmask = mask.header
    
    aRS = RS.affine
    # amask = mask.affine
    
    for t in np.arange(dRS.shape[3]):
        dRS[...,t] = dRS[...,t]*dmask
    
    masked_data_nii = nib.Nifti1Image(dRS, aRS, hRS)

    return masked_data_nii

# nib.save(masked_data_nii, folder + 'raRS_bc_braincorr.nii.gz')

# RS_hs = ch_pxdim_to_human_size(masked_data_nii, 10.0) # change pizel size to ~ human size
# nib.save(RS_hs, folder + 'raRS_bc_brainx10.nii.gz')







