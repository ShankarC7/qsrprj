from django.urls import path
from qsr_app import views
from django.conf.urls.static import static
from qsr import settings


urlpatterns = [
    path('home',views.home),
    path('login', views.user_login),
    path('register', views.register),
    path('lg', views.lg),
    path('addtocart/<pid>', views.addtocart),
    path('cart', views.cart),
    path('updateqty/<qv>/<cid>', views.updateqty),
    path('orderpg', views.orderpg),
    path('delivery', views.delivery),
    path('address', views.address),
    path('payment', views.payment),
    path('remove/<cid>', views.remove),
    path('sndmail/<uemail>', views.sndmail),
    path('shopparcel', views.shopparcel),
    path('wait', views.wait),
    path('removep/<cid>', views.removep),
    path('contact', views.contact),
    path('aboutus', views.aboutus),
    path('Cashe', views.Cashe),
    path('report', views.reports)
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)