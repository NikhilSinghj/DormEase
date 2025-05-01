from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = None
    last_name = None
    std_name = models.CharField(max_length=50)
    dept = models.CharField(max_length=15)
    year = models.CharField(max_length=2)
    u_rollno = models.CharField(max_length=15)
    std_contact = models.CharField(max_length=15)
    f_contact = models.CharField(max_length=15)
    m_contact = models.CharField(max_length=15)
    room_altd = models.CharField(max_length=5)
    seater_altd = models.CharField(max_length=2)



class Roles(models.Model):
    role_name = models.CharField(max_length=50,null=True)
    deleted_status = models.BooleanField(default=False)

class UserRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='user_idty')
    role = models.ForeignKey(Roles,on_delete=models.SET_NULL,null=True,related_name='role_idty')
    deleted_status = models.BooleanField(default=False)

class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    deleted_time = models.DateTimeField(null=True)
    updated_time = models.DateTimeField(null=True)
    deleted_status = models.BooleanField(default=False)
    class Meta:
        abstract = True

class Dropdown(BaseModel):
    name = models.CharField(max_length=50)
    relation = models.ForeignKey("Dropdown", on_delete=models.SET_NULL, null=True)
    order_by = models.PositiveIntegerField(default=0)


class Room(models.Model):
    hostel = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='room_ref')
    room_number = models.CharField(max_length=10)
    capacity = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='roon_cap')


class Warden(models.Model):
    user = models.OneToOneField(UserRole,on_delete=models.SET_NULL,null=True,related_name='warden_info')
    hostel = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='hostel_ref')


class Students(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,related_name='std_idty')
    room = models.ForeignKey(Room,on_delete=models.SET_NULL,null=True,related_name='rel_room')

