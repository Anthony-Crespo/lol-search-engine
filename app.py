from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route('/hello/<name>')
def index(name='there'):
    return render_template('index.html', name=name)


# USE FLASK RUN INSTEAD
# if __name__ == '__main__':
#     app.run()