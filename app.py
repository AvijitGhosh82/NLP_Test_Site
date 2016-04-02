from flask import Flask, render_template, request,redirect,url_for
from werkzeug import secure_filename
import os
import time
# timestr = time.strftime("%Y%m%d-%H%M%S")

app = Flask(__name__)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['ALLOWED_EXTENSIONS'] = set(['txt','dat'])

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def filesave(flist):
	uploaded_files = request.files.getlist(flist)
	print uploaded_files

	for file in uploaded_files:
		if file and allowed_file(file.filename):
			# filename = secure_filename(file.filename)
			filename=time.strftime("%Y%m%d-%H%M%S")+".txt"
			absolute_path = os.path.abspath(UPLOAD_FOLDER+filename)
			file.save(absolute_path)
		#return 'file uploaded successfully'



@app.route("/")
def main():
	return render_template('index.html')

@app.route("/classify", methods=['GET'])
def classify():
	print "howmow"
	return render_template('classify.html')

@app.route("/summarize", methods=['GET'])
def summarize():
	return render_template('summarize.html')


# Route that will process the file upload
@app.route('/uploader', methods=['POST'])
def upload():
	file = request.files['file']
	if file and allowed_file(file.filename):
		# filename = secure_filename(file.filename)
		filename=time.strftime("%Y%m%d-%H%M%S")+".txt"
		absolute_path = os.path.abspath(UPLOAD_FOLDER+filename)
		file.save(absolute_path)
		return 'file uploaded successfully'

	with open("output/abcd.txt", "r") as f:
		content = f.read()
	return render_template("processing.html", content=content)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)


if __name__ == "__main__":
	app.debug = True
	app.run()