from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Piece

UserModel = get_user_model()

# Create your tests here.
class TestModelPiece(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testUser = UserModel.objects.create_user(
            username = 'testUser', 
            password = 'password'
        )
        cls.testUser.save()

        cls.testPiece = Piece(
            user = cls.testUser, 
            text = 'test text'
        )
        cls.testPiece.save()
    
    def testPieceContent(self):
        piece = Piece.objects.filter(id=self.testPiece.id)
        slugIsGenerated = True if piece[0].slug is not None else False
        slugIsUnique = True if piece.count() == 1 else False
        
        self.assertEqual(piece[0].user, self.testPiece.user)
        self.assertEqual(piece[0].text, self.testPiece.text)
        self.assertTrue(slugIsGenerated)
        self.assertTrue(slugIsUnique)

