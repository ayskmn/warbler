import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
from app import app
db.create_all()

class UserModelTestCase(TestCase):
	
	def setUp(self):
		db.drop_all()
		db.create_all()

		self.uid = 4444
		u = User.signup("testuser", "testuser@test.com", "testpassword", None)
		u.id = self.uid
		db.session.commit()

		self.u = User.query.get(self.uid)

		self.client = app.test_client()

	def tearDown(self):
		res = super().tearDown()
		db.session.rollback()
		return res

	def test_message_model(self):
		m =  Message(text="test warble", user_id=self.uid)
		db.session.add(m)
		db.session.commit()

		#Test when user has 1 message
		self.assertEqual(len(self.u.messages), 1)
		self.assertEqual(self.u.messages[0].text, "test warble")

	def test_message_likes(self):
		m1 = Message(text="a warble", user_id=self.uid)
		m2 = Message(text="another warble", user_id=self.uid)

	u = User.signup("anothertest", "a@test.com", "password", None)
	uid = 666
	u.id = self.uid
	db.session.add([m1, m2, u])
	db.session.commit()

	u.likes.append(m1)
	db.session.commit()

	l = Likes.query.filter(Likes.user_id == uid).all()
	self.assertEqual(len(l), 1)
	self.assertEqual(l[0].message_id, m1.id)