from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from recipes import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('', SpectacularAPIView.as_view(), name='schema'),
    
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('admin/', admin.site.urls),
    path('api/recipes/', views.RecipeListView.as_view()),
    path('api/recipes/create/', views.RecipeCreateView.as_view()),
    path('api/recipes/<int:pk>/', views.RecipeDetailsView.as_view()),
    path('api/recipes/<int:pk>/update/', views.RecipeUpdateView.as_view()),
    path('api/recipes/<int:pk>/vote/', views.CreateUpvoteView.as_view()),
    path('api/ingredients/', views.IngredientCreateView.as_view()),
    path('api/register/', views.UserRegistrationView.as_view()),
    path('api/login/', views.LoginView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
