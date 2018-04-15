# 파일네임 정의 
file_name =('her.jpg')

# 로컬에서 이미지 불러들이기
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# 주석을 추가 할 이미지 파일의 이름
def detect_text(file):
    client = vision.ImageAnnotatorClient()

    with io.open(file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:') #텍스트를 인식하는 절 
    response = client.image_properties(image=image)
    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))  

    response = client.web_detection(image=image)
    annotations = response.web_detection
# 웹상에서 누구와 얼마나 일치하는지 찾아낸다. 신기하지?
    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))

    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

detect_text(file_name)

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
    hist = centroid_histogram(clt)
    bar = plot_colors(hist, clt.cluster_centers_)
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.show()
    print(hist)

image = mpimg.imread(file_name)
plt.imshow(image)
image_color_cluster(file_name)  
