"""
URL configuration for cv_generator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from pdf.views import accept, resume, resume_pdf, user_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_list, name='user_list'),
    path('accept/', accept, name='accept'),
    path('pdf/<int:id>/', resume_pdf, name='resume_pdf'),
    path('<int:id>/',resume, name='resume'), # OPTIONAL
]
