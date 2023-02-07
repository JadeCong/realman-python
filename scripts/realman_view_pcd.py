import sys, os, time
import numpy as np
import pcl
import pcl.pcl_visualization


path = "../data/realsense_reconstruction.pcd"
cloud = pcl.load(path)

# visual = pcl.pcl_visualization.CloudViewing()
# visual.ShowMonochromeCloud(cloud)

# flag = "True"
# while flag:
#     flag = not(visual.WasStopped())


