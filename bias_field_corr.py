import ants
from tools_ants import ch_pxdim_to_human_sizeAnts


# Load images
folder = '../RestingState/'
RS =  ants.image_read(folder + 'raRS.nii')
T2 =  ants.image_read(folder + 'rT2.nii')


# Bias correction of RS and T2

T2_bc = ants.n4_bias_field_correction(T2)
RS_bc = ants.n4_bias_field_correction(RS)

ants.image_write( T2_bc, folder + 'T2_bc.nii' )
ants.image_write( RS_bc, folder + 'RS_bc.nii' )


# Change pixel size to human size (to use tools tuned on human brain)
factor = 10 
RS_bc_hs =  ch_pxdim_to_human_sizeAnts(RS_bc, 10)
T2_bc_hs =  ch_pxdim_to_human_sizeAnts(T2_bc, 10)

ants.image_write( T2_bc, folder + 'T2_bc_hs.nii' )
ants.image_write( RS_bc, folder + 'RS_bc_hs.nii' )