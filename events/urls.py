# events/urls.py
from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/',Dashboard.as_view(),name='dashboard'),

    path('api/enrolled_events/', EnrolledEventsListView.as_view(), name='enrolled-events-list'),
    path('api/events/', EventListView.as_view(), name='event_list'),  # List of events
    # path('api/event/create/', EventCreateView.as_view(), name='event_create'),  # Event creation
    path('api/event/enroll/', EnrollInEventView.as_view(), name='event_enroll'), 
    path('api/update_user/', UpdateUserView.as_view(), name='update-user'),
]
