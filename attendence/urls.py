from django.urls import path
from .views import (AttendanceCreateView,AbsentiesView,AttendanceListView,
                    GrievanceListCreateAPIView,GrievanceApprovalAPIView,ListAllGrievanceAPIView)

urlpatterns = [
    path('mark-attendance/', AttendanceCreateView.as_view(), name='attendance-create'),
    path('absenties/', AbsentiesView.as_view(), name='absenties'),
    path('list/', AttendanceListView.as_view(), name='list'),
    path('add-grievance/', GrievanceListCreateAPIView.as_view(), name='add-grievance'),
    path('all-grievances/', ListAllGrievanceAPIView.as_view(), name='all-grievances'),
    path('approve-grievance/<pk>', GrievanceApprovalAPIView.as_view(), name='approve-grievance'),
]
