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
UPLOAD_FOLDER = '/static/image'#chemin pour enregistrer les images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')

#page d'accueil
@app.route('/')
def index():

    return render_template('home.html')

#Eextraction des carateristique des images et les stocker dans le fichier index.csv
@app.route('/indexColor')
def test():
    output_file = 'index.csv'
    c=1
    all_files = os.listdir('static/image/')
	#Pour chaque image extraire leur caracteristique concernant les 3 moments de couleur et les stocker dans le csv
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
    # Exctration du caracteristique du nouvelle image et les ajouter a notre base de donnees
    features = color_moments(str("./static/image/" + filename))
     #Comparer et trier les fonctionnalités de l'image téléchargée avec les fonctionnalités des images calculées hors ligne
    searcher = Search('./index.csv')
    results = searcher.search(features)
    RESULTS_LIST = list()
    for (score, pathImage) in results:
        RESULTS_LIST.append(
            {"image": str(pathImage), "score": str(score)}
        )    
    output_file = 'index.csv'
    image = "./static/image/" + '/' + filename
	#Pour l'image téléchargée, nous extrairons et renverrons les fonctionnalités des moments de couleur
    #et l'enregistrerons également dans un fichier csv
    features = color_moments(image)
    print(features)
    features = [str(f) for f in features]
    with open(output_file, 'a', encoding="utf8") as f:
            f.write("%s,%s\n" % (image, ",".join(features)))
            f.close()
    #afficher les resultats
    return jsonify(RESULTS_LIST)

@app.route('/positive', methods=['POST'])
def positive():
 print("Got request in static files")
 print(request.files)
 f = request.files['static/new']
 f.save(f.filename)
 resp = {"success": True, "response": "file saved!"}
 return jsonify(resp), 200


if __name__ == "__main__":
        app.run()