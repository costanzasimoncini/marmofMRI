import ants
import numpy as np
from tools_ants import ch_pxdim_to_human_sizeAnts



# Load images in good labels and TR corrected
folder = '/Users/costanza/workspace/PROJETS/fMRI_Jacquette/pretraitementsRS/data/'
RS =  ants.image_read(folder + 'raRS.nii')
T2 =  ants.image_read(folder + 'rT2.nii')
# mask = ants.image_read(folder + 'mask_LIP.nii.gz')
# mask_onbrain = ants.image_read(folder + 'mask_onbrain_LIP.nii.gz')


# Bias correction of RS et T2

bcT2 = ants.n4_bias_field_correction(T2)
bcRS = ants.n4_bias_field_correction(RS)

ants.image_write( bcT2, folder + 'bcrT2.nii' )
ants.image_write( bcRS, folder + 'bcraRS.nii' )


# Change pixel size to human size
factor = 10 
tpl = ch_pxdim_to_human_sizeAnts(tpl, 10)
RS =  ch_pxdim_to_human_sizeAnts(RS, 10)
T2 =  ch_pxdim_to_human_sizeAnts(T2, 10)
mask =  ch_pxdim_to_human_sizeAnts(mask, 10)
mask_onbrain =  ch_pxdim_to_human_sizeAnts(mask_onbrain, 10)





# T2 = ants.image_read( T2, folder + 'T2_bc.nii' )
# RS = ants.image_read( RS_bc, folder + 'RS_bc.nii' )






# mywarpedimage = ants.apply_transforms( fixed_image, moving_image, reg_fm[ 'fwdtransforms' ], interpolator  = 'bSpline')
                                       
# mywarpedimage = ants.apply_transforms( fixed = img3, 
#                                        moving = seg1['segmentation'] , 
#                                        transformlist = mytx, 
#                                        interpolator  = 'nearestNeighbor', 
#                                        whichtoinvert = [True,False,True,False])

# ants.plot(T2_warped, tpl_resT2, overlay_alpha = 0.5 )
# ants.image_write( warpedim, folder + 'test.nii' )
# ants.write_transform(reg_fm, 'reg_fm' ) # controlla se non vuole piuttosto una trasf e con file.mat







# ants.get_orientation(T2)
# com = ants.get_center_of_mass(T2)
# ants.set_origin(T2, (138,200,8))
# ants.image_write( T2, folder + 'testCOM.nii' )

# seg1 = ants.kmeans_segmentation( moving_image, 3 )
# ants.plot(T2, fixed_image, overlay_alpha = 0.5 )