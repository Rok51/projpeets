from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla
from flask_admin.menu import MenuLink
from flask_login import current_user, login_user, login_required, LoginManager, UserMixin, logout_user
import bcrypt
from flask import flash

from sqlalchemy import inspect, TypeDecorator, LargeBinary

app = Flask(__name__)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://u8hf3tngk7lq8:pf4fa23bc3495b770de663d39d42f658753263a693a39976d2e008040fd2c87f6@ccba8a0vn4fb2p.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/daiokr68kqi0jb"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///2.sqlite"
#app.config["SQLALCHEMY_DATABASE_URI"] = "user/Ro5/files/home/Ro5/projpeets/instance/example.sqlite"

app.secret_key = 'super secret key'
app.app_context().push()
db = SQLAlchemy(app)

# Custom TypeDecorator to ensure consistent byte storage/retrieval
class BytesType(TypeDecorator):
    impl = LargeBinary

    def process_bind_param(self, value, dialect):
        # Ensure value is bytes when saving to the database
        if isinstance(value, str):
            return value.encode('utf-8')
        return value

    def process_result_value(self, value, dialect):
        # Ensure value is bytes when retrieved from the database
        if isinstance(value, memoryview):
            return value.tobytes()
        return value

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(BytesType, unique=True, nullable=False)  # Use custom BytesType
    name = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean)

    posts = db.relationship('Posts', backref='user')
    comments = db.relationship('Comments', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        # Hash the password and store it as bytes
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        # Directly compare password with stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

class Posts(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    title = db.Column(db.String)
    body = db.Column(db.String)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    comment = db.relationship('Comments', backref='posts')
    rating = db.relationship('Ratings', backref='posts')

    def __repr__(self):
        return '<Posts %r>' % self.title

class Comments(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    body = db.Column(db.String)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    rating = db.relationship('Ratings', backref='post')

    def __repr__(self):
        return '<Comments %r>' % self.body

class Ratings(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    rating = db.Column(db.Integer)

class Followed(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship("User", foreign_keys=[user_id])
    followed = db.relationship("User", foreign_keys=[followed_id])


with app.app_context():
   
    db.create_all()

def can_access_admin_db():

    return current_user.get_id() and current_user.is_admin

class UserModelView(sqla.ModelView):
    column_hide_backrefs = False
    
    column_list = ['id', 'username', 'name', 'is_admin']

    def is_accessible(self):
        return can_access_admin_db()

    def inaccessible_callback(self, name, **kwargs):
      
        return redirect(url_for('login', next=request.url))


class PostModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Posts).mapper.column_attrs]

    def is_accessible(self):
        return can_access_admin_db()

    def inaccessible_callback(self, name, **kwargs):
       
        return redirect(url_for('login', next=request.url))


class CommentModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Comments).mapper.column_attrs]

    def is_accessible(self):
        return can_access_admin_db()
    
    def inaccessible_callback(self, name, **kwargs):
       
        return redirect(url_for('login', next=request.url))


class RatingModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Ratings).mapper.column_attrs]

    def is_accessible(self):
        return can_access_admin_db()

    def inaccessible_callback(self, name, **kwargs):
      
        return redirect(url_for('login', next=request.url))
    
class FollowedModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Followed).mapper.column_attrs]

    def is_accessible(self):
        return can_access_admin_db()

    def inaccessible_callback(self, name, **kwargs):
       
        return redirect(url_for('login', next=request.url))


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated

class LoginMenuLink(MenuLink):
    def is_accessible(self):
        return not current_user.is_authenticated

admin = Admin(app, name='gradebook', template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session))
admin.add_view(PostModelView(Posts, db.session))
admin.add_view(CommentModelView(Comments, db.session))
admin.add_view(RatingModelView(Ratings, db.session))
admin.add_view(FollowedModelView(Followed, db.session))
admin.add_link(LoginMenuLink(name='Return to Login Page', category='', url="/login"))
admin.add_link(LogoutMenuLink(name='Return to Homepage', category='', url="/index"))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def get_followed_posts():
    tempData = Followed.query.filter_by(user_id=current_user.id).all()
    print(f"Followed Relationships: {tempData}")  # Debug Output

    followed_ids = [x.followed_id for x in tempData]
    print(f"Followed User IDs: {followed_ids}")  # Debug Output

    if not followed_ids:
        return []

    posts = Posts.query.filter(Posts.user_id.in_(followed_ids)).distinct().all()
    print(f"Fetched Unique Posts: {posts}")  # Debug Output
    return posts


def post_data(item):
    return {"title": item.title,
            "id": item.id,
            "body": item.body,
            "poster": (User.query.filter_by(id=item.user_id).first()).username,
            "following": False if not current_user.is_authenticated else
                Followed.query.filter_by(user_id=current_user.id, followed_id=item.user_id).first() is not None,
            "likes": item.likes,
            "dislikes": item.dislikes,
            "comments": item.comments,
            "rating": 0 if not (current_user.is_authenticated and 
                                Ratings.query.filter_by(post_id=item.id, user_id=current_user.id).first()) else 
                Ratings.query.filter_by(post_id=item.id, user_id=current_user.id).first().rating}

def post_to_json(item):
    return jsonify(post_data(item))

def posts_to_json(data):
    return jsonify([post_data(item) for item in data])

def comment_data(item):
    return {"body": item.body,
            "commentor": (User.query.filter_by(id=item.user_id).first()).username,
            "following": False if not current_user.is_authenticated else
                Followed.query.filter_by(user_id=current_user.id, followed_id=item.user_id).first() is not None,
            "id": item.id,
            "likes": item.likes,
            "dislikes": item.dislikes,
            "rating": 0 if not (current_user.is_authenticated and 
                                Ratings.query.filter_by(comment_id=item.id, user_id=current_user.id).first()) else 
                Ratings.query.filter_by(comment_id=item.id, user_id=current_user.id).first().rating}

@app.route('/index')
@app.route('/')
def index(): 
    if current_user.is_authenticated:
        all_posts = [post_data(item) for item in Posts.query.all()]
        followed_posts = [post_data(item) for item in get_followed_posts()]
        return render_template('index.html', posts=all_posts, followed=followed_posts)
    else:
        all_posts = [post_data(item) for item in Posts.query.all()]
        return render_template('index.html', posts=all_posts)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.form['username']).first()
    if user is None or not user.check_password(request.form['password']):
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))

@app.route('/postsby/<username>', methods=['GET'])
def userPosts(username):
    tempData = User.query.filter_by(username=username).first()
    data = Posts.query.filter_by(user_id=tempData.id).all()
    return posts_to_json(data)

@app.route('/allposts', methods=['GET'])

def allPosts():
    data = Posts.query.all()
    return posts_to_json(data)

@app.route('/page/<postID>', methods=["GET"])
def postPage(postID):
    # TODO: return data of the post for jinja template
    return render_template("post_page.html", 
                           postInfo=post_data(Posts.query.filter_by(id=postID).first()), 
                           comments=[comment_data(item) for item in Comments.query.filter_by(post_id=postID)])

@app.route("/posts", methods=['POST'])
@login_required
def addPost():
    # add Post
    body = request.form
    title = body['title']
    tempbody = body['body']
    newPost = Posts(user_id=current_user.id, title=title, body=tempbody, likes=0, dislikes=0, comments=0)
    db.session.add(newPost)
    db.session.commit()
    postID = newPost.id
    return redirect("/page/" + str(postID))

@app.route("/delete_post/<int:postID>", methods=["POST"])
@login_required
def delete_post(postID):
    post = Posts.query.filter_by(id=postID, user_id=current_user.id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "success")
    else:
        flash("Post not found or unauthorized action!", "danger")
    return redirect(url_for('profile_page', username=current_user.username))


@app.route("/posts", methods=['DELETE'])
@login_required
def deletePost():
    body = request.get_json()
    postID = body['postID']
    post = Posts.query.filter_by(id=postID).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@app.route('/posts/<postID>', methods=['GET'])
def postbyID(postID):
    data = Posts.query.filter_by(id=postID).first()
    return post_to_json(data)

@app.route('/followed', methods=['GET'])
@login_required
def followedPosts():
    posts = get_followed_posts()
    print(f"Posts Sent to Client: {posts}")  # Debug
    return posts_to_json(posts)


@app.route('/posts/<postID>/comments', methods=['GET'])
@login_required
def seeComments(postID):
    temp = Posts.query.filter_by(id=postID).first()
    data = Comments.query.filter_by(post_id=temp.id).all()
    return jsonify([{"body": item.body,
                    "id": item.id,
                    "likes": item.likes,
                    "dislikes": item.dislikes} for item in data])

@app.route("/posts/<postID>/comments", methods=['POST'])
@login_required
def addComment(postID):
    # add Comment
    body = request.form
    tempbody = body['body']
    newComment = Comments(user_id=current_user.id, post_id=postID, body=tempbody, likes=0, dislikes=0)
    Posts.query.filter_by(id=postID).first().comments += 1
    db.session.add(newComment)
    db.session.commit()
    return redirect("/page/" + str(postID))


@app.route("/posts/<postID>/comments", methods=['DELETE'])
@login_required
def deleteComment(postID):
    # delete Comment
    comment = Comments.query.filter_by(user_id=current_user.id, post_id=postID)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@app.route("/posts/<int:postID>/rating/<int:rating>", methods=['POST'])
@login_required
def ratePost(postID, rating):
    post = Posts.query.filter_by(id=postID).first()
    rate = Ratings.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if rate and rating == 0: 
        if rate.rating == 1:
            post.likes -= 1
        elif rate.rating == 2:
            post.dislikes -= 1
        db.session.delete(rate)
    elif rate and rate.rating != rating: 
        rate.rating = rating
        if rating == 1:
            post.likes += 1
            post.dislikes -= 1
        elif rating == 2: 
            post.likes -= 1
            post.dislikes += 1
    elif not rate and rating != 0: 
        newRating = Ratings(user_id=current_user.id, post_id=postID, rating=rating)
        if rating == 1: 
            post.likes += 1
        elif rating == 2: 
            post.dislikes += 1
        db.session.add(newRating)
    db.session.commit()
    return jsonify({"rating": rating})

@app.route("/comments/<int:commentID>/rating/<int:rating>", methods=['POST'])
@login_required
def rateComment(commentID, rating):
    comment = Comments.query.filter_by(id=commentID).first()
    rate = Ratings.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
    if rate and rating == 0:
        if rate.rating == 1:
            comment.likes -= 1
        elif rate.rating == 2:
            comment.dislikes -= 1
        db.session.delete(rate)
    elif rate and rate.rating != rating: 
        rate.rating = rating
        if rating == 1:
            comment.likes += 1
            comment.dislikes -= 1
        elif rating == 2:
            comment.likes -= 1
            comment.dislikes += 1
    elif not rate and rating != 0:
        newRating = Ratings(user_id=current_user.id, comment_id=commentID, rating=rating)
        if rating == 1:
            comment.likes += 1
        elif rating == 2:
            comment.dislikes += 1
        db.session.add(newRating)
    db.session.commit()
    return jsonify({"rating": rating})


@app.route('/posts/<postID>/rating', methods=['GET'])
def getUserRating(postID):
    data = 0 if not current_user.is_authenticated else Ratings.query.filter_by(post_id=postID, user_id=current_user.id).first()
    return jsonify({"rating": data.rating})

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    check = request.form["confirm"]
    if check != password:
        return redirect('register')
    name = request.form["name"]
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        return "Username already exists", 409
    newUser = User(username=username, password_hash="", name=name, is_admin=False)
    newUser.set_password(password)
    db.session.add(newUser)
    db.session.commit()
    return redirect('login')

@app.route("/users/<username>", methods=["GET", "POST"])
@login_required
def profile_page(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return "User does not exist", 404

    # Check if the logged-in user is following the profile owner
    is_following = Followed.query.filter_by(user_id=current_user.id, followed_id=user.id).first() is not None

    # Handle form submission
    if request.method == "POST" and username == current_user.username:
        name = request.form['name']
        new_username = request.form['username']
        password = request.form['password']

        # Update fields
        user.name = name
        user.username = new_username
        if password and password != "********":
            user.set_password(password)  # Hash the new password

        db.session.commit()  # Save changes
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile_page", username=user.username))

    # Render the page for GET
    id = user.id
    return render_template(
        "profile_page.html",
        username=user.username,
        posts=[post_data(item) for item in Posts.query.filter_by(user_id=id)],
        following=is_following  # Pass the 'following' variable
    )


@app.route("/new_post", methods=["GET"])
def new_post_page():
    return render_template("new_post.html")

@app.route("/follow/<username>", methods=["POST"])
@login_required
def toggle_follow(username):
    desired_follow = request.json["now_following"]
    followed = User.query.filter_by(username=username).first()

    if followed:
        print(f"Requested Follow User: {followed.username} (ID: {followed.id}), Desired Follow: {desired_follow}")  # Debug

        follow_object = Followed.query.filter_by(user_id=current_user.id, followed_id=followed.id).first()
        
        if follow_object and not desired_follow:  # Unfollow
            print("Unfollowing user...")  # Debug
            db.session.delete(follow_object)
            db.session.commit()
        elif not follow_object and desired_follow:  # Follow
            print("Following user...")  # Debug
            follow = Followed(user_id=current_user.id, followed_id=followed.id)
            db.session.add(follow)
            db.session.commit()

        # Verify follow status after changes
        updated_follow_object = Followed.query.filter_by(user_id=current_user.id, followed_id=followed.id).first()
        print(f"Follow status after change: {'Followed' if updated_follow_object else 'Not Followed'}")  # Debug

        return jsonify({"now_following": desired_follow})
    else:
        print("User does not exist!")  # Debug
        return "User does not exist", 404

if __name__ == "__main__":
    app.run()
