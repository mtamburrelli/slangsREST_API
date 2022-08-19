from flask import Flask, render_template, request
from api import slangs


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def addSlang():
    if request.method == 'POST':
        name = request.form['word'].capitalize()
        definicion = request.form['meaning'].capitalize()
        newSlang = {
            "name": name,
            "definicion": definicion
        }
        slangs.append(newSlang)
        return render_template("index.html", message=True)
    else:
        return 'error'


@app.route('/editar', methods=['GET', 'POST'])
def editSlang():
    if request.method == 'POST':
        oldWord = request.form["oldWord"].capitalize()
        slangFound = [slang for slang in slangs if slang['name'] == oldWord]
        if len(slangFound) > 0:
            newName = request.form["word"]
            newDef = request.form["meaning"]
            slangFound[0]["name"] = newName
            slangFound[0]["definicion"] = newDef

            return render_template('editar.html', newDef=newDef, newName=newName, message=True)
        else:
            return 'Palabra inexistente, intente de nuevo'

    return render_template('editar.html')


@app.route("/eliminar", methods=['GET', 'POST'])
def delSlang():
    if request.method == 'POST':
        delWord = request.form["word"].capitalize()
        for slang in slangs:
            if slang['name'] == delWord:
                slangFound = slang
                if len(slangFound) > 0:
                    slangs.remove(slangFound)
                return render_template('eliminar.html', message=True)

    return render_template('eliminar.html')


@app.route('/diccionario', methods=['GET', 'POST'])
def listadoSlangs():
    return render_template("diccionario.html", palabras=slangs)


@app.route('/definicion', methods=['GET', 'POST'])
def slangDef():
    if request.method == 'POST':
        word = request.form["palabra"].capitalize()
        for slang in slangs:
            if slang["name"] == word:
                definicion = slang["definicion"]
                return render_template('definicion.html', palabra=word, definicion=definicion)
        else:
            return "palabra inexistente, intente de nuevo"
    else:
        return render_template('definicion.html')


if __name__ == '__main__':
    app.run(debug=True)
