from flask import Flask, render_template,request
from flask.wrappers import Request
from projet.color.index import index
from projet.color.moment import color_moments


app = Flask(__name__,static_url_path='/static')
#general parameters
UPLOAD_FOLDER = 'static/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/indexColor')
def test():
    output_file = 'index.csv'
    c=1
    image = "C:/Users/chaimae/Desktop/obj1__0.png"
    features = color_moments(image)
    features = [str(f) for f in features]
		# print("c = {}".format(c))
    c += 1
    with open(output_file, 'a', encoding="utf8") as f:
        f.write("%s,%s\n" % ("C:/Users/chaimae/Desktop/obj1__0.png", ",".join(features)))
        f.close()
    return "Done !!"


if __name__ == "__main__":
        app.run()