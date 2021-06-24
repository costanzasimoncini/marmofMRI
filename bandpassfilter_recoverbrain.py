# - Band pass filter fMRI 
# - Add mean to filtered image to recover brain anatomy
# - Apply brain mask to final image.

import numpy as np
import nibabel as nib
from f_applymaskto4Dim import apply_mask_4D_nibabel
# import nipype

# set working folder
folder = "../RestingState/"
# set animal name
name = "Fri3M"

in_file = folder + "sraRS" + name + ".nii"
mask_file = folder + "meanaRS" + name + "_mask.nii"
out_file = folder + "sraRS" + name + "_brain_bpft_tmp.nii.gz"
mean_file = folder + "meanaRS" + name + ".nii" # can be computed by: $ fslmaths img.nii.gz -Tmean img_mean.nii

img = nib.load(in_file)
mask = nib.load(mask_file)
mean = nib.load(mean_file)

# get Repetition Time TR (s)
TR = img.header.get_zooms()[3]
if TR == 0 :
    print(" ! TR = " + str(TR) + " s ! Modify using 'set_TR.py'")
else :
    print("TR = " + str(TR) + " s")


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
# modified from Nipype 'bandpass_filter' function

lowidx = int(timepoints / 2) + 1

if lowpass_freq > 0:
    lowidx = int(np.round(lowpass_freq / fs * timepoints)) 
highidx = 0
if highpass_freq > 0:
    highidx = int(np.round(highpass_freq / fs * timepoints))
F[highidx:lowidx] = 1
F = ((F + F[::-1]) > 0).astype(int)
data = img.get_fdata()
if np.all(F == 1):
    filtered_data = data
else:
    filtered_data = np.real(np.fft.ifftn(np.fft.fftn(data) * F))

 # save filtered image to "out_file" filename
img_out = nib.Nifti1Image(filtered_data, img.affine, img.header)
nib.save(img_out, out_file) 


# Add Mean image to recover brain anatomy
dmask = mask.get_fdata()
print ("Unique values in brain mask : " + str(np.unique(dmask)))
dmask[dmask!=0] = 1.0 # in case brain values are not exactly = 1
nonzerosvx = filtered_data[dmask==1,:]
m = nonzerosvx.min() 

for i in np.arange(timepoints) :
    filtered_data[...,i] = filtered_data[...,i] + mean.get_fdata()
img_out_addmean = nib.Nifti1Image(filtered_data, img.affine, img.header)

# APPLY MASK
img_out_addmean_mask = apply_mask_4D_nibabel(img_out_addmean, mask)

nib.save(img_out_addmean_mask, folder + "sraRS" + name + "_brain_bpft.nii.gz")


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