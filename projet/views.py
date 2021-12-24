from flask import Flask, render_template,request
from flask.wrappers import Request
from projet.color.moment import color_moments
import os, time, cv2
from flask import jsonify 
from projet.color.search import Search
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename


app = Flask(__name__,static_url_path='/static/image')
Bootstrap(app)
#general parameters
UPLOAD_FOLDER = '/static/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
def index():

    return render_template('home.html')
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

    filename = secure_filename(file.filename)
    file.save(os.path.join("static/image/",filename))
    # #Extracting the feature vetor from the uploaded images and adding this vector to our database
    features = color_moments(str("./static/image/" + filename))

     #Comparing and sorting the uploaded image's features with the offline-calulcated images features
    searcher = Search('./index.csv')
    results = searcher.search(features)
    RESULTS_LIST = list()
    for (score, pathImage) in results:
        RESULTS_LIST.append(
            {"image": str(pathImage), "score": str(score)}
        )
         
    output_file = 'index.csv'
    image = "./static/image/" + '/' + filename

	# # For the uploaded image ,we will extract and return the color moments features and also saving it in a csv file
    features = color_moments(image)
    print(features)
    features = [str(f) for f in features]
    with open(output_file, 'a', encoding="utf8") as f:
            f.write("%s,%s\n" % (image, ",".join(features)))
            f.close()
    #returning the search results
    return jsonify(RESULTS_LIST)

# @app.route('/positive', methods=['POST','GET'])
# def positive():
    
#     file = request.files['image']

#     filename = secure_filename(file.filename)
#     file.save(os.path.join("static/new/",filename))
#     return "Done !!"



if __name__ == "__main__":
        app.run()