from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
    print("youhou",name)
    return 'welcome %s' % name

@app.route('/sendData',methods = ['POST'])
def sendData():
    print(request.form)
    print(request.json)

    user = request.json["fridgeName"]
    
    f = open("BDD/data", "a")
    f.write(request.json["contents"])
    f.close()
    return redirect(url_for('success',name = user))

@app.route("/getData/<source>")
def getData(source):
    return open("BDD/"+source).read()
    
if __name__ == '__main__':
    app.run(debug = True)