from django.shortcuts import render
from users.serializers import MyTokenObtainPairSerializer,GroupSerializer,UserSerializer,MessageSerializer ,RegisterSerializer,PostSerializer,LikeSerializer,ComentaireSerializer,InvitationSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from users.models import User,Post,Like,Comentaire,Invitation,Message,Group
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['POST'])
def user_add_post(request):
    user_id = request.data.get('user_id')
    content = request.data.get('content')
    post_pic = request.data.get('post_pic')
    if request.method == 'POST':
        user=User.objects.filter(id=user_id).first()
        post=Post.objects.create(
            user=user,
            content=content,
            post_pic=post_pic
        )
        response="Succed to create post"
        return Response({
            'response':response,
            'data':PostSerializer(post).data
            } ,status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_delete_post(request):
    user_id = request.data.get('user_id')
    post_id = request.data.get('post_id')
    user_courant=User.objects.filter(id=user_id).first()
    post=Post.objects.filter(id=post_id).first()
    if(post.user.id == user_courant.id ):
        post.delete()
        response="le poste a ete supprimer "
        return Response({ 'response':response}, status=status.HTTP_200_OK)   
    else:
        response="tu peux pas supprimer ce poste "
        return Response({ 'response':response}, status=status.HTTP_400_BAD_REQUEST)   


@api_view(['POST'])
def user_faire_like(request):
    user_id = request.data.get('user_id')
    post_id = request.data.get('post_id')
    user=get_object_or_404(User,id=user_id)
    post=get_object_or_404(Post,id=post_id)
    like_exist= Like.objects.filter(user=user, post=post).exists()
    if like_exist :
        return Response({ 'response':'tu ne peux pas'}, status=status.HTTP_200_OK)   
    like=Like.objects.create(
            user=user,
            post=post,
        )
    return Response({ 'response':LikeSerializer(like).data}, status=status.HTTP_200_OK)   

@api_view(['POST'])
def user_faire_dislike(request):
    user_id = request.data.get('user_id')
    post_id = request.data.get('post_id')
    user=get_object_or_404(User,id=user_id)
    post=get_object_or_404(Post,id=post_id)
    like_exist= Like.objects.filter(user=user, post=post).exists()
    if(like_exist):
        like=get_object_or_404(Like,user=user,post=post)
        like.delete()
        return Response({ 'response':'bien recu'}, status=status.HTTP_200_OK)   
    else :
        return Response({ 'response':'zabi'}, status=status.HTTP_200_OK)   




# user_faire_commentaire 
@api_view(['POST'])
def user_faire_coomentaire(request):
    user_id = request.data.get('user_id')
    post_id = request.data.get('post_id')
    content = request.data.get('content')
    user=get_object_or_404(User,id=user_id)
    post=get_object_or_404(Post,id=post_id) 
    commentaire=Comentaire.objects.create(
            user=user,
            post=post,
            content=content,
    )
    return Response({ 'response':ComentaireSerializer(commentaire).data}, status=status.HTTP_200_OK)   

@api_view(['POST'])
def user_delete_commentaire(request):
    user_id = request.data.get('user_id')
    commentaire_id = request.data.get('commentaire_id')
    user_courant=User.objects.filter(id=user_id).first()
    commentaire=Comentaire.objects.filter(id=commentaire_id).first()
    if(commentaire.user.id == user_courant.id ):
        commentaire.delete()
        response="le poste a ete supprimer "
        return Response({ 'response':response}, status=status.HTTP_200_OK)   
    else:
        response="tu peux pas supprimer ce poste "
        return Response({ 'response':response}, status=status.HTTP_400_BAD_REQUEST)   



@api_view(['POST'])
def user_faire_invitation(request):
    from_user_id = request.data.get('from_user_id')
    to_user_id = request.data.get('to_user_id')
    from_user=get_object_or_404(User,id=from_user_id)
    to_user=get_object_or_404(User,id=to_user_id)
    user1=from_user
    user2=to_user    
    if user1.username < user2.username:
        username1, username2 = user1.username, user2.username
    else:
        username1, username2 = user2.username, user1.username
    # Créer un nom de groupe unique
    group_name = f"{username1}_{username2}"
    # Vérifier si un groupe existe déjà
    group = Group.objects.filter(name=group_name).first()
    if not group:
        # Créer un nouveau groupe
        group = Group.objects.create(name=group_name)
        # Ajouter les utilisateurs au groupe
    invitation=Invitation.objects.create(
            from_user=from_user,
            to_user=to_user,
            group=group
    )
    return Response({ 'response 1':InvitationSerializer(invitation).data,'response 2':GroupSerializer(group).data}, status=status.HTTP_200_OK)   


@api_view(['POST'])
def user_views_posts(request):
    user_id = request.data.get('user_id')
    user=get_object_or_404(User,id=user_id)
    les_amies=Invitation.objects.filter(from_user=user,accepted =True).values_list('to_user', flat=True)
    amies_posts = Post.objects.filter(user__in=les_amies).order_by('-created_at')
    serialized_posts = PostSerializer(amies_posts, many=True).data
    return Response(serialized_posts)

@api_view(['POST'])
def user_views_amies(request):
    user_id = request.data.get('user_id')
    user = get_object_or_404(User, id=user_id)
    les_amies_data = Invitation.objects.filter(from_user=user, accepted=True).values_list('to_user', 'group')

    # Liste pour stocker les données des amis
    les_amies = []

    # Parcourir chaque tuple retourné par la requête
    for to_user_id, group_id in les_amies_data:
        # Récupérer l'objet utilisateur
        to_user = get_object_or_404(User, id=to_user_id)
        # Récupérer l'objet groupe
        group = get_object_or_404(Group, id=group_id)
        
        # Créer un dictionnaire contenant les informations de l'utilisateur et du groupe
        ami_data = {
            'user': UserSerializer(to_user).data,
            'group': GroupSerializer(group).data
        }
        # Ajouter le dictionnaire à la liste des amis
        les_amies.append(ami_data)

    return Response({'amis': les_amies})

@api_view(['POST'])
def user_view_info(request):
    user_id = request.data.get('user_id')
    user=get_object_or_404(User,id=user_id)
    serialized_amies = UserSerializer(user).data
    return Response(serialized_amies)

@api_view(['POST'])
def get_likes_count(request):
    post_id = request.data.get('post_id')
    post=get_object_or_404(Post,id=post_id)
    likes_count = Like.objects.filter(post=post).count()
    return Response({'likes_count': likes_count})

@api_view(['POST'])
def user_ecrire_message(request):
    source_id = request.data.get('source_id')
    destination_id = request.data.get('destination_id')    
    content = request.data.get('content')
    source_user=get_object_or_404(User,id=source_id)
    destination_user=get_object_or_404(User,id=destination_id)
    message=Message.objects.create(
            source=source_user,
            destinataion=destination_user,
            content=content
    )
    return Response({ 'response':MessageSerializer(message).data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_voir_messages(request):
    source_id = request.data.get('source_id')
    destination_id = request.data.get('destination_id')    
    source_user = get_object_or_404(User, id=source_id)
    destinataion_user = get_object_or_404(User, id=destination_id)
    
    # Récupérer les messages des deux directions
    messages_source_destination = Message.objects.filter(source=source_user, destinataion=destinataion_user)
    messages_destination_source = Message.objects.filter(source=destinataion_user, destinataion=source_user)
    
    # Serializer les messages
    serialized_messages_source_destination = MessageSerializer(messages_source_destination, many=True).data
    serialized_messages_destination_source = MessageSerializer(messages_destination_source, many=True).data
    
    # Concaténer les deux ensembles de messages
    all_messages = serialized_messages_source_destination + serialized_messages_destination_source
    
    # Trier les messages par created_at
    sorted_messages = sorted(all_messages, key=lambda x: x['created_at'], reverse=False)
    
    return Response(sorted_messages, status=status.HTTP_200_OK)


