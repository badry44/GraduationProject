# Import the used libs
from keras.models import load_model
import pickle 
import cv2
import keras
# Predict function
# imageUrl : Local url of the image
# modelUrl : Local url of the model
# labelsUrl: Local url of the labels
# width    : The width after resizing
# height   : The height after resizing

def predict(imageUrl:str, modelUrl:str, labelsUrl:str, width:int=200, height:int=200):

	# Load image at given url
	image = cv2.imread(imageUrl)
	output = image.copy()

	# Resize the image to fit model
	image = cv2.resize(image, (width, height))

	# Normalize the colors of the image
	image = image.astype("float") / 255.0

	# reshape the image
	image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

	# Loading the model
	model=load_model(modelUrl)
	# Load the labels
	lb = pickle.loads(open(labelsUrl, "rb").read())

	# Predict the given image
	preds = model.predict(image)
	# print(preds)

	# Load the prediction with the highest probability 
	i = preds.argmax(axis=1)[0]
	label = lb.classes_[i]

	# print(label)
	# # Show the prediction
	# text = "{}: {:.2f}%".format(label, preds[0][i]*100)
	# cv2.putText(output, text, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

	# # Show the output image
	# cv2.imshow("Image ", output)
	# cv2.waitKey(0)

	# Return the classification and the probability
	keras.backend.clear_session()
	return label, preds[0][i]*100

# Testing
# imageUrl = "output/ISIC_0010167.jpeg"
# modelUrl = "output/trainedModel.model"
# labelsUrl= "output/labels.pickle"
# (l, p) = predict(imageUrl, modelUrl, labelsUrl)
# print(l)
# print(p)