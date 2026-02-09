from django.urls import path
from .views import CSVUploadView, SummaryView,EquipmentListView,UploadHistoryView

urlpatterns = [
    path('upload/', CSVUploadView.as_view()),
    path('summary/',SummaryView.as_view()),
    path('equipment/',EquipmentListView.as_view()),
    path("upload-history/", UploadHistoryView.as_view()),

]
