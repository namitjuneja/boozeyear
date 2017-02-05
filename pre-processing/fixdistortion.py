import lensfunpy

import exifread
# Open image file for reading (binary mode)
f = open('abc.jpg', 'rb')

# Return Exif tags
tags = exifread.process_file(f)


print "APERTURE", float(str(tags["EXIF ApertureValue"]).split("/")[0])/float(str(tags["EXIF ApertureValue"]).split("/")[1])
print "EXPOSURE", float(str(tags["EXIF ExposureTime"]).split("/")[0])/float(str(tags["EXIF ExposureTime"]).split("/")[1])
print "FOCAL-LENGTH", float(str(tags["EXIF FocalLength"]).split("/")[0])/float(str(tags["EXIF FocalLength"]).split("/")[1])


cam_maker = 'NIKON CORPORATION'
cam_model = 'NIKON D3S'
lens_maker = 'Nikon'
lens_model = 'Nikkor 28mm f/2.8D AF'

db = lensfunpy.Database()
cam = db.find_cameras(cam_maker, cam_model)[0]
lens = db.find_lenses(cam, lens_maker, lens_model)[0]

print(cam)
# Camera(Maker: NIKON CORPORATION; Model: NIKON D3S; Variant: ;
#        Mount: Nikon F AF; Crop Factor: 1.0; Score: 0)

print(lens)
# Lens(Maker: Nikon; Model: Nikkor 28mm f/2.8D AF; Type: RECTILINEAR;
#      Focal: 28.0-28.0; Aperture: 2.79999995232-2.79999995232;
#      Crop factor: 1.0; Score: 110)




import cv2 # OpenCV library

# focal_length = 28.0
focal_length = float(str(tags["EXIF FocalLength"]).split("/")[0])/float(str(tags["EXIF FocalLength"]).split("/")[1])
# aperture = 1.4
aperture = float(str(tags["EXIF ApertureValue"]).split("/")[0])/float(str(tags["EXIF ApertureValue"]).split("/")[1])
# distance = 10


image_path = 'ttt4.jpg'
undistorted_image_path = 'ttt5.jpg'

im = cv2.imread(image_path)
height, width = im.shape[0], im.shape[1]

mod = lensfunpy.Modifier(lens, cam.crop_factor, width, height)
mod.initialize(focal_length, aperture)

undist_coords = mod.apply_geometry_distortion()
im_undistorted = cv2.remap(im, undist_coords, None, cv2.INTER_LANCZOS4)
cv2.imwrite(undistorted_image_path, im_undistorted)

