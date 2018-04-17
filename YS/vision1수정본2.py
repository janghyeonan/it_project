    import numpy as np
    import cv2
    import matplotlib.image as mpimg
    from matplotlib import pyplot as plt
    from sklearn.cluster import KMeans
# 데이터로 그래프를 그림
    def histogram(clt):   
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=numLabels)   
        hist = hist.astype("float")
        hist /= hist.sum()
        return hist
    
    def plot_colors(hist, centroids):
        bar = np.zeros((50, 300, 3), dtype="uint8")
        startX = 0
        for (percent, color) in zip(hist, centroids):
            endX = startX + (percent * 300) #x 시작점의 3배 
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                          color.astype("uint8").tolist(), -1)
            startX = endX
        return bar
    
    #  scikit-learn의 k-mean 알고리즘으로 이미지를 학습
    def image_color_cluster(file_name, k = 5):
        image = cv2.imread(file_name)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.reshape((image.shape[0] * image.shape[1], 3))    
        clt = KMeans(n_clusters = k)
        clt.fit(image)
        hist = histogram(clt)
        bar = plot_colors(hist, clt.cluster_centers_)
        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()
        print(hist)
    
  
    plt.imshow(file_name)
    image_color_cluster(file_name) 
