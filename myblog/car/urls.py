from django.urls import path
from .views import*

urlpatterns = [
    path('', CarHome.as_view(), name='home'),
    path('about/', about.as_view(), name='about'),
    path('profile/', profile.as_view(), name='profile'),
    path('addpage/', Addpage.as_view(), name='addpage'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('logout/', Logout_user, name='logout'),
    path('spisok_user/', spisok_user.as_view(), name='spisok_user'),
    path('register/', RegisterUserForm.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', CarCategory.as_view(), name='category'),
    path('user_profile/<slug:slug>/', ShowProfilePageView.as_view(), name='user_profile'),
    path('create_profile_page/',CreateProfilePageView.as_view(), name='create_user_profile'),
    ]
