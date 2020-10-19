from rest_framework import routers

from jobs import views

router = routers.DefaultRouter()
router.register('shortest-path-jobs', views.JobsViewSet, basename="shortest-path-jobs")

app_name = 'jobs'
urlpatterns = router.urls
