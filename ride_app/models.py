from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Ride(models.Model):

    class Meta:
        db_table = 'ride'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    is_request = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20,
                              choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('completed', 'Completed'),
                                       ('cancelled', 'Cancelled')], default='requested')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture_url = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=200,blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    class Meta:
        db_table = 'userProfile'

class Friends(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections2')

    class Meta:
        db_table = 'friends'

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        db_table = 'member'

class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256,blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups', null=True, blank=True,
                              default=None)

    class Meta:
        db_table = 'group'
