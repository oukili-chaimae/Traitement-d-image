import cv2, os
from projet.color.moment import color_moments

def index():
	# creating a gaborDescripto instance and its kernels
	color = color_moments()
	
	output_file = 'index.csv'
	c = 1
	all_files = os.listdir('static/image/')  ##path relative to server.py

	#For each image in the database we will extract the Gabor kernels based vector features and saving it in a csv file
	for imagePath in all_files:
		imageId = imagePath[imagePath.rfind("/")+1:]
		image = cv2.imread("./static/image/"+imagePath)

		features = color.color_moments(image)
		features = [str(f) for f in features]
		# print("c = {}".format(c))
		c += 1
		with open(output_file, 'a', encoding="utf8") as f:
			f.write("%s,%s\n" % ("./static/images/"+imageId, ",".join(features)))
			f.close()
