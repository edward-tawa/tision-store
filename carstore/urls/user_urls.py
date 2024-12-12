from django.urls import path
from carstore.views.user.user_view import RegisterView, LogInView, LogOutView, VerifyEmailView
from carstore.views.user.profile_view import ProfileView, ProfileViewUpdate


urlpatterns= [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('profile/<int:user_id>/',ProfileView.as_view(), name="profile"),
    path('profile/<int:user_id>/update/',ProfileViewUpdate.as_view(), name="profile-update"),
    path('verify-email/', VerifyEmailView.as_view(), name='email-verify')

]
