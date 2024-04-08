from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyObtainTokenPairView,user_voir_messages,user_view_info,user_ecrire_message,get_likes_count,RegisterView,user_add_post,user_delete_post,user_views_amies,user_faire_like,user_faire_dislike,user_faire_coomentaire,user_delete_commentaire,user_views_posts,user_faire_invitation


urlpatterns =[
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),    
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('RegisterView/', RegisterView.as_view(), name='RegisterView'),
    path('user_add_post/', user_add_post, name='user_add_post'),
    path('user_delete_post/', user_delete_post, name='user_delete_post'),
    path('user_faire_like/', user_faire_like, name='user_faire_like'),
    path('user_faire_dislike/', user_faire_dislike, name='user_faire_dislike'),
    path('user_faire_coomentaire/', user_faire_coomentaire, name='user_faire_coomentaire'),
    path('user_delete_commentaire/', user_delete_commentaire, name='user_delete_commentaire'),
    path('user_views_posts/', user_views_posts, name='user_views_posts'),
    path('user_views_amies/', user_views_amies, name='user_views_amies'),
    path('user_view_info/', user_view_info, name='user_view_info'),
    path('get_likes_count/', get_likes_count, name='get_likes_count'),
    path('user_faire_invitation/', user_faire_invitation, name='user_faire_invitation'),
    path('user_ecrire_message/', user_ecrire_message, name='user_ecrire_message'),
    path('user_voir_messages/', user_voir_messages, name='user_voir_messages'),
]