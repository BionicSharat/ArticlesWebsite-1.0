from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('delete/<article_id>', views.delet_article, name='delete'),
    path('get_article/<article_ids>', views.get_article, name='get_article'),
    path('collection/get_article/<article_ids>', views.get_article, name='get_article_collection'),
    path('delete_category/<category_id>', views.delet_category, name='delete_category'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.login_user, name="signin"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('collection/', views.collection_mg, name="collection_mg"),
    path('collection/delete/<collection_id>', views.delete_collection, name="collection_delete"),
    path('collection/<collection_id>', views.collection_home, name="collection_spec"),
    path('remove/<collection_id>', views.remove_participant, name='remove_user'),
    path('change_role/<role_number>', views.change_role, name='change_role')
] 