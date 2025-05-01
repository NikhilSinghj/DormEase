from django.urls import path
from .views import (UserRegistrationView,LoginView,LogoutView,RoomListCreate
                    ,WardenListCreate,StudentListCreate,UploadExcelView,StudentAPIView)

urlpatterns = [
    # path('user/', UserRegistrationView.as_view(), name='register-user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('rooms/',RoomListCreate.as_view(),name='add-room-to-hostel'),
    path('warden/',WardenListCreate.as_view(),name='add-warden-to-hostel'),
    path('room-allotment/',StudentListCreate.as_view(),name='roomallotment'),
    path('upload-excel/', UploadExcelView.as_view(), name='upload-excel'),
    path('users/', StudentAPIView.as_view(), name='all-students'),
]
