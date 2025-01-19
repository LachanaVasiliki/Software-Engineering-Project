from django.urls import path
from . import views

from project import settings

from django.conf.urls.static import static

app_name = "festivalsystem"
urlpatterns = [
    path('', views.index, name='index'),  # Αρχική σελίδα
    path('festivals/', views.festivals, name='festivals'),  # Λίστα φεστιβάλ
    path('signup/', views.signup, name='signup'),  # Σελίδα εγγραφής
    path('login/', views.login_view, name='login'),  # Σελίδα σύνδεσης
    path('profile/', views.profile, name='profile'),  # Προφίλ χρήστη
    path('logout/', views.logout_view, name='logout'),  # Αποσύνδεση
    
    path('view_perfomances/', views.view_user_perfomances, name='view_user_perfomances'),  # Προβολή παραστάσεων χρήστη
    path('perfomances/<int:perfomance_id>', views.perfomance_detail, name='perfomance_detail'),  # Λεπτομέρειες παράστασης
    path('perfomances/<int:perfomance_id>/download_perfomance', views.download_perfomance, name='download_perfomance'),  # Λήψη παράστασης
    path('perfomances/<int:perfomance_id>/review_perfomance', views.review_perfomance, name='review_perfomance'),  # Αξιολόγηση παράστασης
    path('perfomances/<int:perfomance_id>/add_reviewers/', views.add_reviewers, name='add_reviewers'),  # Προσθήκη κριτών
    path('perfomances/<int:perfomance_id>/remove_reviewer/<int:reviewer_id>', views.remove_reviewer, name='remove_reviewer'),  # Αφαίρεση κριτή

    path('festival/<int:festival_id>/', views.festival_details, name='festival_details'),  # Λεπτομέρειες φεστιβάλ
    path('festival/<int:festival_id>/submit_perfomance/', views.submit_perfomance, name='submit_perfomance'),  # Υποβολή παράστασης
    path('festival/<int:festival_id>/view_perfomances/', views.view_festival_perfomances, name='view_fest_perfomances'),  # Προβολή παραστάσεων φεστιβάλ
]