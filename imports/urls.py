from django.urls import path
from  .views import *

urlpatterns = [
    path('', upload_treatments),
    path('<int:imports_id>/citizens/<int:citizens>/', patch_imports)
]
