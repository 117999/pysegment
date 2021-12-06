# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 13:25:32 2021

@author: Tobias Vendetta
"""

'''
pysegment: a small utility for cellular segementation from HE stained images
'''
### import libraries
import matplotlib.pyplot as plt
from skimage.io import imread, imsave
from skimage.feature import canny
from skimage.filters import threshold_otsu, gaussian
from skimage.filters import threshold_multiotsu
from skimage import img_as_ubyte
from skimage.color import label2rgb
import numpy as np
from sklearn.cluster import KMeans
from fcmeans import FCM
###loading the image
##Todo: these should be passed by the user
## if no filenames specified, it will generate automatically
input_filename='breast.png'
output_filename='breast_segment.png'

###Read img
img=imread(input_filename)
###segmentation
thre=threshold_otsu(img)
plt.show(img>thre,cmap='gray')
plt.axis('off')
plt.title(f'OTSUs threshold ({thre})',fontsize=18)
plt.show()
##noise is problem for otsu's threshold, gaussian will help
thre=threshold_multiotsu(img,classes=3)
img_gaus=img_as_ubyte(gaussian(img,5))
img_thre_gaus=np.digitize(img_gaus,t)

###clustering methods for segmentation
##Create K means models with 4 clusters
kmeans=KMeans(n_clusters=4, random_state=42)
blobs=imread('blobs_green.tif')
kmeans.fit(blobs.reshape(-1,3))# reshape the image in 3 columns
clusters=kmeans.predict(blobs.reshape(-1,3))
clusters=clusters.reshape(blobs.shape[0],blobs.shape[1])
plt.imshow(label2rgb(clusters,bg_label=0))
plt.plot()
###Fuzzy-C-means segmentation
##data points can belong to different clusters with differenet probabilities
## FCM is similar to k-means but more robust to noise, inconsistent illuminations
n_clusters=4
fcm=FCM(n_clusters=n_clusters,max_iter=100)
fcm.fit(img.reshape(-1,1))
clusters=fcm.predict(img.reshape(-1,1))
clusters=clusters.reshape(img.shape)





