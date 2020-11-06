"""Message model tests."""

import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.drop_all()
db.create_all()

class UserMessageTestCase(TestCase):
    """Test model for Messages"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        Likes.query.delete()

        self.client = app.test_client()

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

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_warble(self):
        """Test for posting a warble"""

        user = User(
            email="msg@test.com",
            username="msgtester",
            password="HASHED_PASSWORD"
        )

        db.session.add(user)
        db.session.commit()

        msg = Message(text="Testing Testing 1,2,3", user_id=user.id)

        db.session.add(msg)
        db.session.commit()

        msg_count = Message.query.count()

        self.assertEqual(msg_count, 1)

    def delete_warble(self):
        """Test deleting warble"""

        user = User.query.get(1)

        msg = Message(text="Testing Testing 1,2,3", user_id=user.id)

        db.session.add(msg)
        db.session.commit()

        get_msg = Message.query.get(1)

        db.session.delete(get_msg)
        db.session.commit()

        msg_count = Message.query.count()

        self.assertEqual(msg_count, 0)