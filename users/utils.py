# from django.shortcuts import get_object_or_404
# from .models import Message, Room,User


# def get_user(username):
#     user = get_object_or_404(User, username=username)
#     return user


# def get_groupId(group_name):
#     group = get_object_or_404(Group, name=group_name)
#     return group


# def last_25_messages(group_name):
#     group = get_object_or_404(Group, name=group_name)
#     return Message.objects.filter(group=group).order_by('-timestamp').all()[:25]