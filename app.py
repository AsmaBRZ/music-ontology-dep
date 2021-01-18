from flask import Flask,request, render_template

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/requestResult', methods=['POST'])
def requestResult():
    if request.method == 'POST': 
        #data = request.files['image_data']
        data = 1
        print()
        if data == None:
            return 'no image received'
        else:
            # model.predict.predict returns a dictionary
            print()
    else:
      return render_template('index.html')

    return jsonify(results=prediction)


if __name__ == '__main__':
   app.run(debug = True)