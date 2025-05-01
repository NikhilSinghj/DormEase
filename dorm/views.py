from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import CreateAPIView,ListCreateAPIView,ListAPIView
from .models import User,Students,Room,Warden
from .serializers import (UserRegistrationSerializer,LoginSerializer,RoomSerializer,WardenSerializer,StudentSerializer,
                          UserSerializer)


class UserRegistrationView(ListCreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        print(request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            password = serializer.validated_data['password']
            
            # Fetch the user using username or email
            try:
                user = User.objects.get(Q(username=identifier) | Q(email=identifier))
            except User.DoesNotExist:
                user = None
            
            # If user is found, use the username to authenticate
            if user:
                user = authenticate(request, username=user.username, password=password)
                if user:
                    login(request, user)
                    return Response({"message": "User logged in successfully."}, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
    


class RoomListCreate(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


    def perform_create(self, serializer):

        serializer.save(hostel_id=self.request.data.get('hostel'),

                         room_number=self.request.data.get('room_number'),

                         capacity_id=self.request.data.get('capacity'))
        

class WardenListCreate(ListCreateAPIView):

    queryset = Warden.objects.all()

    serializer_class = WardenSerializer


    def perform_create(self, serializer):

        serializer.save(user_id=self.request.data.get('user'),

                         hostel_id=self.request.data.get('hostel'))
        

class StudentListCreate(ListCreateAPIView):

    queryset = Students.objects.all()

    serializer_class = StudentSerializer


    def perform_create(self, serializer):

        serializer.save(user_id=self.request.data.get('user'),

                         room_id=self.request.data.get('room'))
        


class StudentAPIView(APIView):

    def get(self, request):

        students = User.objects.all()

        serializer = StudentSerializer(students,many=True)

        return Response(serializer.data)
    


import pandas as pd
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UploadExcelView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Ensure the file is read using pandas for .xlsx files
            df = pd.read_excel(file)
            
            # Print columns for debugging
            print("Columns in Excel file:", df.columns.tolist())

            required_columns = ['std_name', 'dept', 'year', 'u_rollno', 'std_contact', 'f_contact', 'm_contact', 'room_altd', 'seater_altd','email']
            if not all(column in df.columns for column in required_columns):
                return Response({"error": "Invalid file format"}, status=status.HTTP_400_BAD_REQUEST)
            
            errors = []
            with transaction.atomic():
                for _, row in df.iterrows():
                    user_data = {
                        'username': row['u_rollno'],  # Assuming u_rollno is unique and can be used as username
                        'std_name': row['std_name'],
                        'email': row['email'],
                        'dept': row['dept'],
                        'year': row['year'],
                        'u_rollno': row['u_rollno'],
                        'std_contact': row['std_contact'],
                        'f_contact': row['f_contact'],
                        'm_contact': row['m_contact'],
                        'room_altd': row['room_altd'],
                        'seater_altd': row['seater_altd'],
                        'password' : "Kiet@123"
                    }
                    # Assuming User model has a custom create_user method
                    user = User.objects.create_user(**user_data)
                    if user:
                        # Optionally, you can serialize the created user and return it in the response
                        serializer = UserSerializer(user)
                    else:
                        errors.append({"error": f"Failed to create user with u_rollno: {user_data['username']}"})
            
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"status": "success", "message": "Data imported successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
