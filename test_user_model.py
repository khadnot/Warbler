"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        Likes.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(user)
        db.session.commit()

        # User should have no messages, followers, or likes
        self.assertEqual(len(user.messages), 0)
        self.assertEqual(len(user.followers), 0)
        self.assertEqual(len(user.likes), 0)

    def test_repr_method(self):
        """Test repr method"""

        user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(user)
        db.session.commit()

        self.assertEqual(
            repr(user), f'<User #{user.id}: testuser, test@test.com>'
        )

    def test_is_following(self):
        """Test is_following method"""

        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        user2 = User(
            email="test2@testing.com",
            username="test2user",
            password="PASSWORD123!"
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        #Create follow relationship
        follows = Follows(user_being_followed_id=user1.id,
                          user_following_id=user2.id)
        
        db.session.add(follows)
        db.session.commit()

        #Test if user2 is following user1
        self.assertEqual(user2.is_following(user1), True)
        self.assertEqual(len(user2.following), 1)

        #Test if user1 is following user2
        self.assertEqual(user1.is_following(user2), False)
        self.assertEqual(len(user2.following), 1)

    def test_is_followed_by(self):
        """Test is_followed_by method"""

        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        user2 = User(
            email="test2@testing.com",
            username="test2user",
            password="PASSWORD123!"
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        #Create follow relationship
        follows = Follows(user_being_followed_id=user1.id,
                          user_following_id=user2.id)

        db.session.add(follows)
        db.session.commit()

        #Test if user1 is followed by user2
        self.assertEqual(user1.is_followed_by(user2), True)
        self.assertEqual(len(user1.followers), 1)

        #Test if user2 is followed by user1
        self.assertEqual(user2.is_followed_by(user1), False)
        self.assertEqual(len(user2.followers), 0)
        
    def test_user_signup(self):
        """Test creating new user"""

        user1 = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        user2 = User(
            email="test2@testing.com",
            username="test2user",
            password="PASSWORD123!",
            image_url=None
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        user_count = User.query.count()

        self.assertEqual(user_count, 2)

    
    def test_user_authenticate(self):
        """Test user authentication"""

        user = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        db.session.add(user)
        db.session.commit()

        auth = User.authenticate("testuser", "HASHED_PASSWORD")
        invalid_user = User.authenticate("kenbo", "HASHED_PASSWORD")
        invalid_pass = User.authenticate("testuser", "pa$$word123")

        self.assertTrue(auth)
        self.assertFalse(invalid_user)
        self.assertFalse(invalid_pass)