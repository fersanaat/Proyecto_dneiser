"""proyecto_neiser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from dneiser.views import * 

urlpatterns = [
        path('principal/', index_index, name='index'),
        path('secund/', index_index1, name='index1'),
        path('detalles/', index_detalles, name='detalles'),
        path('papeleria/', index_papeleria, name='papeleria'),
        path('maquillaje/', index_maqui_page, name='maquillaje'),
        path('golosina/', index_golosina, name='golosina'),
        path('products/create/', ProductCreateView.as_view(), name='product_create'),
        path('product/list/', ProductListView.as_view(), name='product_list'),
        path('product/<int:id>', ProductDetailView.as_view(), name='product_detail'),
        path('product/<int:id>/update/', ProductUpdateView.as_view(), name='product_update'),
        path('product/<int:id>/delete', ProductDeleteView.as_view(), name='product_delete'),
        path('login/', UserLoginView.as_view(), name='login'),
        path('register/', UserRegisterView.as_view(), name='register'),
        path('logout/', UserLogoutView.as_view(), name='logout')
        
]

        