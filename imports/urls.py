from django.urls import path
from  .views import *

urlpatterns = [
    path('', upload_treatments),
    path('/<int:imports_id>/citizens/<int:citizens>', patch_imports),
    path('/<int:imports_id>/citizens', get_imports),
    path('/<int:imports_id>/citizens/birthdays', calc_birthdays),
    path('/<int:imports_id>/towns/stat/percentile/age', age_percentile)
]
