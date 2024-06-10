from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
# class UserDetails(models.Model):
#     f_name = models.CharField(max_length=30)
#     hostel_name = models.CharField(max_length=30)
#     room_no = models.PositiveSmallIntegerField()
#     year = models.PositiveSmallIntegerField()

    # admission_year = models.s 

class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    deleted_time = models.DateTimeField(null=True)
    updated_time = models.DateTimeField(null=True)
    deleted_status = models.BooleanField(default=False)
    class Meta:
        abstract = True

class Roles(models.Model):
    role_name = models.CharField(max_length=50,null=True)

class UserRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='user_identity')
    role = models.ForeignKey(Roles,on_delete=models.SET_NULL,null=True,related_name='role_identity')

class Dropdown(models.Model):
    name = models.CharField(max_length=50)
    relation = models.ForeignKey("Dropdown", on_delete=models.SET_NULL, null=True)
    order_by = models.PositiveIntegerField(default=0)

class Attendence(BaseModel):
    student = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='stu_idty')
    marked_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='markedby_idty')
    status = models.BooleanField(default=False)



class Hostel(models.Model):

    name = models.CharField(max_length=50)

    description = models.TextField(max_length=200)


class Room(models.Model):

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    room_number = models.CharField(max_length=10)

    capacity = models.PositiveSmallIntegerField()


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    roll_number = models.CharField(max_length=10, unique=True)

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Warden(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)


class Attendance(models.Model):

    date = models.DateField()

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    warden = models.ForeignKey(Warden, on_delete=models.CASCADE)


class AttendanceRecord(models.Model):

    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=[('P', 'Present'), ('A', 'Absent')])


class LeaveApplication(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField(max_length=200)

    status = models.CharField(max_length=10, choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')])


class LeaveApproval(models.Model):

    leave_application = models.ForeignKey(LeaveApplication, on_delete=models.CASCADE)

    warden = models.ForeignKey(Warden, on_delete=models.CASCADE)

    approval_date = models.DateField()

    comments = models.TextField(max_length=200, blank=True)
