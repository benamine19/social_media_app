from django.contrib import admin
from .models import User,Post,Like,Invitation,Comentaire,Message,Group
# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Invitation)
admin.site.register(Comentaire)
admin.site.register(Message)
admin.site.register(Group)



