from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer

import json

@api_view(['GET'])
def get_users(request):

    if request.method == 'GET':

        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_by_nick(request, nick):
        try:
            user = User.objects.get(pk=nick)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':

            serializer = UserSerializer(user)
            return Response(serializer.data)
        

#CRUDZAO
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request):
    # GET (Recuperando dados)
    if request.method == 'GET':
        try:
            if request.GET['user']: 
                user_nickname = request.GET['user']

                try: 
                    user = User.objects.get(pk=user_nickname)
                except User.DoesNotExist:
                    return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({"error": "Ocorreu um erro interno."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "Parâmetro 'user' ausente na requisição GET."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Ocorreu um erro inesperado no GET."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # CRIANDO DADOS (POST)
    elif request.method == 'POST':
        new_user = request.data

        serializer = UserSerializer(data=new_user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)