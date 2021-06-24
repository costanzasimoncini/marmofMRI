import numpy as np
import nibabel as nib

def apply_mask_4D_nibabel(RS, mask):

    dRS = RS.get_fdata()
    hRS = RS.header
    aRS = RS.affine
  
    dmask = mask.get_fdata()
    
    for t in np.arange(dRS.shape[3]):
        dRS[...,t] = dRS[...,t] * dmask
    
    masked_data_nii = nib.Nifti1Image(dRS, aRS, hRS)

    return masked_data_nii