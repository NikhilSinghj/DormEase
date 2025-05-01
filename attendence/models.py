from django.db import models
from dorm.models import BaseModel,User,Warden,Students,Dropdown

class Attendance(BaseModel):
    date = models.DateField()
    hostel = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='at_hostel')
    marked_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='markedby')


class AttendanceRecord(BaseModel):
    attendance = models.ForeignKey(Attendance,on_delete=models.SET_NULL,null=True,related_name='atd_rec')
    student = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='std_rec')
    atd_status = models.CharField(max_length=10, choices=[('P', 'Present'), ('A', 'Absent')])


# class LeaveApplication(models.Model):

#     student = models.ForeignKey(Student, on_delete=models.CASCADE)

#     start_date = models.DateField()

#     end_date = models.DateField()

#     reason = models.TextField(max_length=200)

#     status = models.CharField(max_length=10, choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')])


# class LeaveApproval(models.Model):

#     leave_application = models.ForeignKey(LeaveApplication, on_delete=models.CASCADE)

#     warden = models.ForeignKey(Warden, on_delete=models.CASCADE)

#     approval_date = models.DateField()

#     comments = models.TextField(max_length=200, blank=True)

class Grievance(models.Model):
    student = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='std_griev')
    type = models.CharField(max_length=50)
    problem = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    approval_status = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)  
    created_time = models.TimeField(auto_now_add=True)
   