import numpy as np
import cv2
import os
import scipy.io
import pyrealsense2 as rs

# Set path to save folder location, this Folder needs 4 subfolder: depth_mat, depth_img, rgb_mat, rgb_img
path_data = r"/home/luongmanh/lab/python/getdata/data9/"
path_depth_mat =path_data+r"depth_mat"
path_depth_img =path_data+r"depth_img"
path_rgb_mat =path_data+r"rgb_mat"
path_rgb_img =path_data+r"rgb_img"

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    a = 0
    while True:
        a += 1
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        
        # Save data to save folder
        cv2.imwrite(os.path.join(path_depth_img , 'depth'+str(a)+'.jpg'), depth_colormap)
        cv2.imwrite(os.path.join(path_rgb_img , 'rgb'+str(a)+'.jpg'), color_image)
        scipy.io.savemat(os.path.join(path_rgb_mat, 'rgb'+str(a)+'.mat'), {'rgb'+str(a): color_image})
        scipy.io.savemat(os.path.join(path_depth_mat, 'depth'+str(a)+'.mat'), {'depth'+str(a): depth_image})
        
        # Stop iterate
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    cv2.destroyAllWindows()
    pipeline.stop()





