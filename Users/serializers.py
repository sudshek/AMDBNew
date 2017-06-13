from rest_framework.serializers import ModelSerializer
from models import user
from models import Movie
from models import Review
class UserSerializer(ModelSerializer):
    class Meta:
       model = user
       fields = ('id','name','username','short_bio','updated_on','created_on','contact','email')
class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('name','duration_in_minutes','release_date','censor_board_rating','overall_rating','poster_picture_url','user_id',)

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('movie','user','rating','review')

