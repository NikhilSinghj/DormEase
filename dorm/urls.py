# from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     # path('',)

# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import path

from.views import get_users , register


urlpatterns = [

    path('users/', get_users),
    path('register/', register, name='register'),

]