from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
def upload_path_profile_pic(instance, filename):
    return 'coversProfile_pic/{0}/{1}'.format(instance.username, filename)

def upload_path_post_pic(instance, filename):
    return 'covers_post_pic/{0}/{1}'.format(instance.user.username, filename)


AUTH_PROVIDER={'email':'email','google':'google'}
class User(AbstractUser):
  username=models.CharField( max_length=50,unique=True)
  email=models.EmailField(unique=True)
  is_bloque=models.BooleanField(default=False)
  auth_provider=models.CharField(max_length=50 ,default=AUTH_PROVIDER.get('email'))
  profile_pic = models.ImageField(upload_to=upload_path_profile_pic,default='aaa.jpg')
  USERNAME_FIELD='email'
  REQUIRED_FIELDS=['username']
  def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_pic = models.ImageField(upload_to=upload_path_post_pic, default='aaa.jpg')
    def __str__(self):
        return self.user.username


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class Comentaire(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username



class Group(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    private = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Invitation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent')  # Changement ici
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_received')  # Changement ici
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='invitations', null=True)  # Changement ici
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Invitation from {self.from_user.username} to {self.to_user.username}"




class Message(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')  # Changement ici
    destinataion = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')  # Changement ici
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages', null=True)  # Changement ici
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message from {self.source.username} to {self.destinataion.username}"
