from flask import Flask, render_template,request
from flask.wrappers import Request
from projet.color.moment import color_moments
import os, time, cv2
from flask import jsonify 
from projet.color.search import Search

app = Flask(__name__,static_url_path='/static/image')
#general parameters
UPLOAD_FOLDER = '/static/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
def index():

    return render_template('index.html')
#C:/Users/chaimae/Desktop/obj1__0.png

@app.route('/indexColor')
def test():
    output_file = 'index.csv'
    c=1
    all_files = os.listdir('static/image/')
    
	#For each image in the database we will extract the Gabor kernels based vector features and saving it in a csv file
    for imagePath in all_files:
        imageId = imagePath[imagePath.rfind("/")+1:]
        image = "./static/image/"+imagePath

        features = color_moments(image)
        features = [str(f) for f in features]
		# print("c = {}".format(c))
        c += 1
        with open(output_file, 'a', encoding="utf8") as f:
            f.write("%s,%s\n" % ("static/image/"+imageId, ",".join(features)))
            f.close()
    return "Done !!"



#function upload
@app.post('/upload')
def upload():
    #Saving the Uploaded image in the Upload folder
    file = request.files['image']
    new_file_name = str(
        str(time.time()) + '.png'
    )
    file.save(os.path.join(
            app.config['UPLOAD_FOLDER'],new_file_name
        ))
    #Extracting the feature vetor from the uploaded images and adding this vector to our database
    features = color_moments(str(UPLOAD_FOLDER + '/' + new_file_name))
    #Comparing and sorting the uploaded image's features with the offline-calulcated images features
    searcher = Search('./index.csv')
    results = searcher.search(features)
    # results = searcher.gaborSearch(features)
    RESULTS_LIST = list()
    for (score, pathImage) in results:
        RESULTS_LIST.append(
            {"image": str(pathImage), "score": str(score)}
        )
    #returning the search results
    return jsonify(RESULTS_LIST)

if __name__ == "__main__":
        app.run()