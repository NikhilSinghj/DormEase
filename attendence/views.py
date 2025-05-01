from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from dorm.authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated
from dorm.permissions import IsStaff
from rest_framework.views import APIView
from .models import Attendance,AttendanceRecord,Grievance
from .serializers import (AttendanceSerializer,AttendanceRecordSerializer,AbsentiesSerializer,GrievanceSerializer,
GrievanceListSerializer,GrievanceApproveSerializer,DropdownSerializer)

class AttendanceCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated, IsStaff]

    def create(self, request, *args, **kwargs):
        # Extracting data from the request
        date = request.data.get('date')
        hostel = request.data.get('hostel')

        # Validation to check if attendance has already been marked for the same date and hostel
        if Attendance.objects.filter(date=date, hostel=hostel).exists():
            return Response({"message": "Attendance already marked."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with serializer validation and instance creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data from the serializer
        validated_data = serializer.validated_data

        # Create the Attendance instance
        attendance_records_data = validated_data.pop('atd_rec')
        attendance = Attendance.objects.create(marked_by=request.user, **validated_data)

        try:
            # Creating attendance records
            for record_data in attendance_records_data:
                AttendanceRecord.objects.create(attendance=attendance, **record_data)
        except Exception as e:
            attendance.delete()  # Rollback Attendance creation
            return Response({"detail": f"Error creating attendance record: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Attendance Marked"}, status=status.HTTP_201_CREATED)





class AbsentiesView(APIView):
    def get(self, request):
        print(request.GET.get('date'))
        absenties = AttendanceRecord.objects.filter(attendance__date=request.GET.get('date'),atd_status="A")

        serializer = AbsentiesSerializer(absenties, many=True)

        return Response(serializer.data)
    
   
class AttendanceListView(APIView):
    def get(self, request):
        print(request.GET.get('date'))
        absenties = AttendanceRecord.objects.filter(attendance__date=request.GET.get('date'))

        serializer = AbsentiesSerializer(absenties, many=True)

        return Response(serializer.data)
    

class GrievanceListCreateAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):

        grievances = Grievance.objects.filter(student=self.request.user.pk)

        serializer = GrievanceListSerializer(grievances, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):

        serializer = GrievanceSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(student=self.request.user) 

            return Response({'message': 'Grievance Added'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GrievanceApprovalAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated,IsStaff]

    def get(self, request, pk):

        grievances = Grievance.objects.filter(pk=pk)

        serializer = GrievanceListSerializer(grievances, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        status = request.data.get('status')
        pk = self.kwargs.get('pk')
        if not pk:
            return Response({'error': 'Grievance id required'}, status=status.HTTP_400_BAD_REQUEST)

        grievance = Grievance.objects.get(pk=pk)

        if grievance:

            grievance.approval_status = status 

            grievance.save()

            return Response({'message': 'Grievance approved successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'Grievance not found'}, status=status.HTTP_404_NOT_FOUND)
    

class ListAllGrievanceAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated,IsStaff]

    def get(self, request):

        grievances = Grievance.objects.filter()

        serializer = GrievanceListSerializer(grievances, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class HostelAPIView(generics.ListAPIView):
    serializer_class = DropdownSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated,IsStaff]

    def get_queryset(self):
        
        return super().get_queryset()