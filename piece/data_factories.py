from django.contrib.auth import get_user_model
from .models import Piece
import factory

User = get_user_model()

class PieceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Piece
    
    text = factory.Faker('text', max_nb_chars=200)
    user = User.objects.get(pk = 1)