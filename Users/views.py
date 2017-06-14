# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Users.views import Review
from Users.serializers import MovieSerializer
from Users.serializers import ReviewSerializer
from Users.models import user
from django.db.models import Avg
from django.http import HttpResponse
from django.utils.datetime_safe import datetime, date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Users.serializers import UserSerializer
from rest_framework import filters
from django.contrib.auth.hashers import check_password, make_password
from Users.models import AccessToken
from Users.models import Movie
from Users.models import Genre
from Users.models import MovieGenre


@api_view(['POST'])
def create_user(request):
    name = request.data['name']
    username = request.data['username']
    password = request.data['password']
    short_bio = request.data['short_bio']

    if name is None or len(name)==0:
        return Response ({"error_message": "Name field cannot be empty"}, status=400)

    if username is None or len(username)==0:
        return Response({"error_message": "Username can not be empty"},status=400)
    if password is None or len(password)<=6:
        return Response({"error_message": "Password should not be empty or less than 6 characters long"},status=400)
    #return HttpResponse(True)

    does_username_exist = user.objects.filter(username=username)

#
    if len(does_username_exist)>0:
        return Response({"error_message":"Username already exists"},status= 400)
    else:
        new_user= user.objects.create(username=username,name=name,password=make_password(password),short_bio=short_bio)
        new_user.save()


    return Response(UserSerializer(instance=new_user).data, status=200)


@api_view(['GET'])
def get_user(request):

    if 'user_id' in request.query_params:

        new_user = user.objects.filter(id=request.query_params['user_id'])
        if len(new_user)>0:
            return Response(UserSerializer(instance=new_user[0]).data,status=200)
        else :
            return Response({"error_message":"User Not Found!!"},status=200)
    else:
        user_all= user.objects.all()
        return Response(UserSerializer(instance=user_all,many=True).data,status=200)


@api_view(['POST'])
def login_user(request):
    username=request.data['username']
    password=request.data['password']

    new_user = user.objects.filter(username=username).first()
    if new_user:
        if not check_password(password, new_user.password):
            return Response({"message":"User name or password wrong"},status=200)


        else :
            token = AccessToken(users_id=new_user)
            token.create_token()
            token.save()
            return Response({"message":token.access_token},status=200)
    else :
        return Response({"message":"Username or password wrong"},200)



@api_view(['POST'])
def create_movie(request):

    current_user = check_token(request)
    user_id = current_user.username
    if current_user is not None:

        if 'name' in request.data:
            name = request.data['name']
            does_movie_exist = Movie.objects.filter(name=name).first()
            if does_movie_exist is not None:
                return Response({"error_message":"This movie exists already!!"},status=200)

        else:
            return Response({'error_message ': 'Movie name not provided '}, status=200)


        if 'duration_in_minutes' in request.data:
            duration_in_minutes = request.data['duration_in_minutes']
        else:
            return Response({'error_message': 'Movie Duration not provided '}, status=200)


        if 'release_date' in request.data:
            release_date = request.data['release_date']
        else:
            return Response({'error_message ': 'Release Date not provided '}, status=200)


        if 'poster_picture_url' in request.data:
            poster_picture_url = request.data['poster_picture_url']
        else:
            return Response({'error_message ': 'Poster picture url not provided '}, status=200)


        if 'overall_rating' in request.data:
            overall_rating = request.data['overall_rating']
        else:
            return Response({'error_message ': 'Overall rating not provided '}, status=200)



        if 'censor_board_rating' in request.data:
            censor_board_rating = request.data['censor_board_rating']
        else:
            return Response({'error_message ': 'Censor Board Rating not provided '}, status=200)


        if 'genre_name' in request.data:
            genre_name = request.data['genre_name']
        else:
            return Response({'error_message ': 'Genre name not provided '}, status=200)

        if len(name)==0:
            return Response({"error_message":"Name cannot be empty"})

        if len(genre_name)<1:
            return Response({"error_message":"You need to enter atleast one genre."})

        if censor_board_rating>5:
            return Response ({"error_message":"You are supposed to rate movie between 1 to 5"})


        if overall_rating>5:
            return Response ({"error_message":"You are supposed to rate movie between 1 to 5"})

        new_movie = Movie.objects.create(name=name, release_date=release_date, duration_in_minutes=duration_in_minutes,
                                         poster_picture_url=poster_picture_url, overall_rating=overall_rating,
                                         censor_board_rating=censor_board_rating, user_id=user_id)
        new_movie.save()

        for name in genre_name:
           does_genre_exists = Genre.objects.filter(name=name).first()
           if does_genre_exists is not None:
               new_genre = MovieGenre.objects.create(genre_id=does_genre_exists,movie_id=new_movie)

               new_genre.save()
           else:
                return Response({"error_message":"Genre does not exist"},status=200)


        return Response(MovieSerializer(instance=new_movie).data,status=200,)
    else:
        return Response("You are not authorized to perform this action!")



# creates the review of a movie.
@api_view(['POST'])
def review_movie(request):
    current_user = check_token(request)
    if current_user is not None:

        if 'name' in request.data:
            name = request.data['name']
        else:
            return Response({"error_message":"Movie Name not provided"},status=200)

        if 'user' in request.data:
            user = request.data['user']
        else:
            return Response({"error_message": "User name not provided"}, status=200)

        if 'rating' in request.data:
            rating= request.data['rating']
        else:
            return Response({"error_message": "Rating not provided"}, status=200)

        if 'review' in request.data:
            review = request.data['review']
        else:
            return Response({"error_message": "Review not provided"}, status=200)

        if len(name) == 0:
            return Response({"error_message":"Please enter a name"},status=200) # returns error message if review is empty!


        movie_exists = Movie.objects.filter(name=name).first()

        if movie_exists:

            does_rating_exist = Review.objects.filter(movie=movie_exists,user = current_user)

            if  does_rating_exist:
                return Response({"error_message":"You have already rated this movie!!"})

            elif float(rating) > 5.0:
                return Response({"error_message":"You have to rate movie between zero to 5"})

            elif len(review) == 0:
                return Response({"error-message":"You haven't written the review!"})

            else :
                new_review = Review.objects.create(movie=movie_exists,user=current_user,rating=rating,review=review)
                new_review.save()
                average_rating = Review.objects.filter(movie=movie_exists).aggregate(avg_rating=Avg('rating'))

                movie_rating = Movie.objects.filter(id=movie_exists.id).first()
                movie_rating.overall_rating = average_rating['avg_rating']
                movie_rating.save()
                return Response(ReviewSerializer(instance=new_review).data, status=200)
        else:
            return Response({"error_message":"No such movie exists, Create movie!"})
    else :
        return Response("You are not authorized to perform this action!")



#Returns the list of movie searched by user. The named is passed by  query parameter'q'. If no such movie is present,it returns all the movies.
@api_view(['GET'])
def get_movie(request):
    movie_list=[]
    if 'q' in request.query_params:
        # name_icontains covers all matches for all types of upper and lower case of queries.
        movies = Movie.objects.filter(name__icontains=request.query_params['q'])
        if movies is not None:
            for movie in movies:
                movie_list.append(movie)

            genre_query = request.query_params['q']
            genre = Genre.objects.filter(name__icontains=genre_query).first()

            movie_genre = MovieGenre.objects.filter(genre_id=genre)
            for i in range(len(movie_genre)):
                movie_id = (Movie.objects.filter(id=movie_genre[i].movie_id).first()).id
                movie_list.append(movie_id)
                movie_set = set(movie_list)
                movie_list = list(movie_set)

            for i in range(len(movie_list)):
                movie_list[i] = MovieSerializer(instance=Movie.objects.filter(id=movie_list[i]).first()).data
            return Response(movie_list,status=200)


        else:
            all_movies = Movie.objects.all()
            return Response(MovieSerializer(instance=all_movies,many=True),status=400)
    else:
        return Response({"error_message":"query parameter not found!"})


@api_view(['POST'])
def logout_user(request):
    current_user = check_token(request)

    if current_user is not None:
        token= AccessToken.objects.filter(users_id="current_user",is_valid="true" )
        token.is_valid=False
        return Response({"message":"You are successfully logged out"})

    else :
        return Response({"message":"We could not log you out"})

#Checks whether provided token exists or not, If it exists, whether it is valid or not.
def check_token(request):
    token = request.META['HTTP_TOKEN']
    token_exist = AccessToken.objects.filter(access_token = token,is_valid=True).first()
    if not token_exist:
        return None
    else:
        return token_exist.users_id





