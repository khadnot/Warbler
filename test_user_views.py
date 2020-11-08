"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        self.testuser2 = User.signup(username="test2user",
                                     email="tester@test2.org",
                                     password="th1$pa$$w0rd!",
                                     image_url=None)

        self.lmp_bizkit = User.signup(username="lmp_bizkit",
                                      email="bizzy1@gmail.com",
                                      password="N00K13!",
                                      image_url=None)

        db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_create_user(self):
        """Can we create a new user?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/signup", data={"username": "kenbo",
                                           "email": "k3nb0@gmail.com",
                                           "password": "password123",
                                           "image_url": None
                                           })

            self.assertEqual(resp.status_code, 302)

            user = User.query.filter_by(username="kenbo").one()

            self.assertEqual(user.username, "kenbo")

    def test_users_index(self):
        """Test show all users"""

        with self.client as c:
            resp = c.get("/users")

            self.assertIn("testuser", str(resp.data))
            self.assertIn("test2user", str(resp.data))
    
    def test_users_search(self):
        """Test search for users"""

        with self.client as c:
            resp = c.get("/users?q=test")

            self.assertIn("testuser", str(resp.data))
            self.assertIn("test2user", str(resp.data))

    def test_user_show(self):
        """Test show user page"""

        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("testuser", str(resp.data))

    def test_like_post(self):
        """Test liking a warble"""
        
        msg = Message(id=2020, text="Kanye West 2020!!", user_id=self.lmp_bizkit.id)
        db.session.add(msg)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/add_like/2020")
            self.assertEqual(resp.status_code, 302)

            likes = Likes.query.filter(Likes.message_id==2020).all()
            self.assertEqual(len(likes), 1)
            self.assertEqual(likes[0].user_id, self.testuser.id)

    def test_unlike_post(self):
        """Test removing like from a warble"""

        msg = Message(id=1988, text="Where's a good place to eat??", user_id=self.testuser2.id)
        db.session.add(msg)
        db.session.commit()

        liked_msg = Likes(user_id=self.testuser.id, message_id=1988)
        db.session.add(liked_msg)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/add_like/1988")
            self.assertEqual(resp.status_code, 302)

            unliked = Likes.query.filter(Likes.message_id==1988).all()
            self.assertEqual(len(unliked), 0)
            










