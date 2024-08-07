from flask import request, render_template
from main import app, db

@app.route('/new')
def user_registration():

    return render_template('new.html')

@app.route('/create', methods=['POST'])
def create_user():

    user = User()
    user.name = request.form['name']
    user.email = request.form['email']
    user.password = request.form['password']
    db.session.add(user)
    db.session.commit()

    return render_template('show.html', user = user)

if __name__ == "__main__":
    app.run(debug=True)  