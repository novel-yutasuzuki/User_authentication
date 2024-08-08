# from flask import request, render_template
# from models import user
# from main import app, SessionLocal

# @app.route('/new')
# def user_registration():
#     return render_template('new.html')

# @app.route('/create', methods=['POST'])
# def create_user():
#     session = SessionLocal()
#     try:
#         user = user.User()
#         user.name = request.form['name']
#         user.email = request.form['email']
#         user.password = request.form['password']
#         session.add(user)
#         session.commit()
#     finally:
#         session.close()

#     return render_template('show.html', user = user)

# if __name__ == "__main__":
#     app.run(debug=True)