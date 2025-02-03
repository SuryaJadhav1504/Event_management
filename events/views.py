# events/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
# from events.models import Profile
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics
from .serializers import *
from .serializers import EventSerializer, EnrollmentSerializer
from .tasks import send_enrollment_confirmation_email  

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer



class LoginView(generics.GenericAPIView):
    # permission_classes = [AllowAny]  
    serializer_class = LoginSerializer
    def post(self, request,*args, **kwargs):
        email = request.data.get('email')
        print(email)
        password = request.data.get('password')
        print(password)

        # user = authenticate(email=email,password=password)
        # print(user)
        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):  
            refresh = RefreshToken.for_user(user)
            user_serializer=UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user':user_serializer.data
            })
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        # return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class Dashboard(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        user=request.user
        user_serializer= UserSerializer(user)
        return Response({
            'message':"Welcom to Dashboard",
            'user':user_serializer.data
            })
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
print("RedisCheck",r.ping())  





# View for listing all events
class EventListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


# View for creating new events (Admin Only)
# class EventCreateView(generics.CreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticated]


# View for enrolling a user into an event
class EnrollInEventView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        event_id = request.data.get('event')

        # Check if event exists
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if user is already enrolled
        if Enrollment.objects.filter(user=user, event=event).exists():
            return Response({"detail": "User is already enrolled in this event."}, status=status.HTTP_400_BAD_REQUEST)

        # Enroll the user
        enrollment_data = {'user': user.id, 'event': event.id}
        serializer = self.get_serializer(data=enrollment_data)

        if serializer.is_valid():
            serializer.save()
            send_enrollment_confirmation_email(event.name, user.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrolledEventsListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
 
        user = self.request.user  # Get the current logged-in user
        enrolled_events = Enrollment.objects.filter(user=user).values_list('event', flat=True)  # Get the event IDs the user is enrolled in
        events = Event.objects.filter(id__in=enrolled_events)  # Get the events based on the IDs
        return events

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def get_object(self):
        # Return current logged-in user....
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FileUpload
from .serializers import FileUploadSerializer
from .tasks import process_uploaded_file  # Celery task to process files

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_upload = serializer.save()
            
            # Trigger background processing task with Celery
            process_uploaded_file.delay(file_upload.id)
            
            return Response({
                "message": "File uploaded successfully and processing started.",
                "file_id": file_upload.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
