from app import db, User, Posts, Comments, Ratings

users = [
    User(username="user1", name="Derozan", is_admin=False),
    User(username="user2", name="Curry", is_admin=False),
    User(username="user3", name="MJ", is_admin=False),
    User(username="admin", name="admin", is_admin=True)
]

for user in users:
    user.set_password(user.username)


db.session.add_all(users)
db.session.commit()


posts = [
    Posts(
        title="My First Post",
        body="coffee sucked had no sugar",  
        likes=1,
        dislikes=1,
        comments=2,
        user_id=User.query.filter_by(username="user1").first().id
    ),
    Posts(
        title="My Second Post",
        body="bagels suck",  
        likes=0,
        dislikes=1,
        comments=1,
        user_id=User.query.filter_by(username="user1").first().id
    ),
    Posts(
        title="Test post",
        body="testing", 
        likes=0,
        dislikes=0,
        comments=0,
        user_id=User.query.filter_by(username="user2").first().id
    )
]


db.session.add_all(posts)
db.session.commit()


comments = [
    Comments(
        body="bad",
        likes=0,
        dislikes=0,
        user_id=User.query.filter_by(username="user3").first().id,
        post_id=Posts.query.filter_by(title="My Second Post").first().id
    ),
    Comments(
        body="good",
        likes=0,
        dislikes=0,
        user_id=User.query.filter_by(username="user3").first().id,
        post_id=Posts.query.filter_by(title="My First Post").first().id
    ),
    Comments(
        body="meh",
        likes=0,
        dislikes=1,
        user_id=User.query.filter_by(username="user2").first().id,
        post_id=Posts.query.filter_by(title="My First Post").first().id
    )
]


db.session.add_all(comments)
db.session.commit()


ratings = [
    Ratings(
        rating=1,
        user_id=User.query.filter_by(username="user3").first().id,
        post_id=Posts.query.filter_by(title="My First Post").first().id
    ),
    Ratings(
        rating=2,
        user_id=User.query.filter_by(username="user3").first().id,
        post_id=Posts.query.filter_by(title="My Second Post").first().id
    ),
    Ratings(
        rating=2,
        user_id=User.query.filter_by(username="user3").first().id,
        comment_id=Comments.query.filter_by(body="meh").first().id
    ),
    Ratings(
        rating=2,
        user_id=User.query.filter_by(username="user2").first().id,
        post_id=Posts.query.filter_by(title="My First Post").first().id
    )
]


db.session.add_all(ratings)
db.session.commit()
