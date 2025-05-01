from rest_framework import serializers
from .models import Attendance, AttendanceRecord, Dropdown, User, Students,Grievance

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'atd_status']

class AttendanceSerializer(serializers.ModelSerializer):
    atd_rec = AttendanceRecordSerializer(many=True)

    class Meta:
        model = Attendance
        fields = ['id', 'date', 'atd_rec', 'hostel']


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','std_name', 'dept', 'year', 'u_rollno', 'std_contact', 'f_contact', 'm_contact', 'room_altd', 'seater_altd']

class AbsentiesSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='student.email')
    std_name = serializers.CharField(source='student.std_name')
    dept = serializers.CharField(source='student.dept')
    year = serializers.IntegerField(source='student.year')
    u_rollno = serializers.CharField(source='student.u_rollno')
    std_contact = serializers.CharField(source='student.std_contact')
    f_contact = serializers.CharField(source='student.f_contact')
    m_contact = serializers.CharField(source='student.m_contact')

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'email', 'std_name', 'dept', 'year', 'u_rollno', 'std_contact', 'f_contact', 'm_contact', 'atd_status']



class GrievanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grievance
        fields = '__all__'


class GrievanceListSerializer(serializers.ModelSerializer):
    student = StudentsSerializer()
    class Meta:
        model = Grievance
        fields = ['id','type','problem','description','approval_status','created_date','created_time','student']

class GrievanceApproveSerializer(serializers.ModelSerializer):
    student = StudentsSerializer()
    class Meta:
        model = Grievance
        fields = ['id','type','problem','description','approval_status','student']


class DropdownSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dropdown
        fields = ['id','name']