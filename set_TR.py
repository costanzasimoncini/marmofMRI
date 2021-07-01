import nibabel as nib

# set fMRI data file path
# Example: 
filename = "../RestingState/RS.nii"

# SET NEW Repetition Time
TR = 2.0
TRms = TR * 1000 # save TR in ms in filename in order to have integer values


file_format = filename[-3:]
filename_newTR = filename[:filename.rfind(".nii")] + "TR" + str(int(TRms)) + "ms.nii"

fMRI = nib.load(filename)

data = fMRI.get_fdata()
hd = fMRI.header
affine = fMRI.affine

# in Nifti metadata TR is saved as the voxel size in the 4th dimension 
zooms = hd.get_zooms()[:3] + (TR,)
print(zooms)
hd.set_zooms(zooms)

newfMRI = nib.Nifti1Image(data, affine, hd)
nib.save(newfMRI, filename_newTR) 
# nib.save(newfMRI, filename) # overwrite the same file