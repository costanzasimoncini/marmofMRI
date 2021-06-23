import os
import numpy as np
import nibabel as nb
from f_applymaskto4Dim import apply_mask_4D_nibabel
# import nipype

folder = "/Users/costanza/workspace/PROJETS/fMRI_marmo/210607_02_Josette3M/RestingState/"

name = "Jos3M"

in_file = folder + "sraRS" + name + ".nii"
mask_file = folder + "meanaRS" + name + "_mask.nii"
out_file = folder + "sraRS" + name + "_brain_bpft_tmp.nii.gz"
mean_file = folder + "meanaRS" + name + ".nii" # fslmaths raRS_bc_brain.nii.gz -Tmean mean.nii
img = nb.load(in_file)
mask = nb.load(mask_file)
mean = nb.load(mean_file)

# Compute mean and add filtered image (to recover anatomy)

# imgdata = img.get_fdata()
# img_mean = np.mean(imgdata, axis = 3)
# funziona ma sbatti cambiare i metadata per cambiare dim


TR = img.header.get_zooms()[3]


if TR == 0 :
    print(" ! TR = " + str(TR) + "s ! Modify using 'set_TR.py'")
else :
    print("TR = " + str(TR) + "s")


# Band Pass frequencies (Hz)
lowpass_freq = 0.1     # cutoff frequency for the low pass filter (in Hz)
highpass_freq = 0.008  # cutoff frequency for the high pass filter (in Hz)
# highpass_freq = 0.01
# highpass_freq = 0.025

fs = 1./TR # sampling rate (in Hz)

timepoints = img.shape[-1]
F = np.zeros((timepoints))

print("timepoints = " + str(timepoints))

# BAND PASS FILTER
# taken from Nipype 'bandpass_filter' function ??????

lowidx = timepoints // 2 + 1 # "/" replaced by "//"
# lowidx = int(timepoints / 2) + 1

if lowpass_freq > 0:
    lowidx = int(np.round(lowpass_freq / fs * timepoints)) # "np.round(..." replaced by "int(np.round(..."
highidx = 0
if highpass_freq > 0:
    highidx = int(np.round(highpass_freq / fs * timepoints)) # same
F[highidx:lowidx] = 1
F = ((F + F[::-1]) > 0).astype(int)
data = img.get_fdata()
if np.all(F == 1):
    filtered_data = data
else:
    filtered_data = np.real(np.fft.ifftn(np.fft.fftn(data) * F))
img_out = nb.Nifti1Image(filtered_data, img.affine, img.header)
img_out.to_filename(out_file) # save to "out_file" filename


# ADD MEAN
dmask = mask.get_fdata()
print ("Unique values in brain mask : " + str(np.unique(dmask)))
dmask[dmask!=0] = 1.0 # in case brain values are not exactly = 1
nonzerosvx = filtered_data[dmask==1,:]
m = nonzerosvx.min() 

for i in np.arange(timepoints) :
    filtered_data[...,i] = filtered_data[...,i] + mean.get_fdata()
img_out2 = nb.Nifti1Image(filtered_data, img.affine, img.header)

# APPLY MASK
img_out2_mask = apply_mask_4D_nibabel(img_out2, mask)

# img_out2_mask.to_filename(folder + "raRS_bc_brain_bpft_min0_mask.nii.gz") # save
img_out2_mask.to_filename(folder + "sraRS" + name + "_brain_bpft.nii.gz") # save



# ## FSL
# from nipype.interfaces.fsl import TemporalFilter
# TF = TemporalFilter(in_file=in_file, out_file=out_file, 
#                     highpass_sigma = 1 / (2 * TR * highpass_freq),
#                     lowpass_sigma = 1 / (2 * TR * lowpass_freq))
# TF.run()




# # AFNI
# from nipype.interfaces import afni
# bandpass = afni.Bandpass(in_file=in_file, highpass=0.008, lowpass=0.08, 
#                          despike=False, no_detrend=True, notrans=True, 
#                          tr=TR, out_file=out_file)
# bandpass.run()