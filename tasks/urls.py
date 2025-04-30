# Importaciones necesarias
from django.urls import path
from . import views

# Definición de las rutas de la aplicación
urlpatterns = [
    # Ruta para la vista de inicio de sesión
    path('login/', views.login_view, name='login'),
    # Ruta para la vista de registro
    path('signup/', views.signup_view, name='signup'),
    # Ruta para la vista del dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # Ruta para la vista de cierre de sesión
    path('logout/', views.logout_view, name='logout'),
    # Nueva URL para Barra 1
    path('barra1/', views.barra1_dashboard, name='barra1_dashboard'),
    # Nueva URL para Barra 2
    path('barra2/', views.barra2_dashboard, name='barra2_dashboard'),
    # Nueva URL para Cocina
    path('cocina/', views.cocina_dashboard, name='cocina_dashboard'),
    # Nueva URL para el dashboard del administrador
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # Ruta para redirigir la raíz del sitio al dashboard
    path('', views.dashboard, name='home'),
    # Nueva URL para eliminar producto
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    # Nueva URL para actualizar producto
    path('actualizar_producto/<int:producto_id>/', views.actualizar_producto, name='actualizar_producto'),
    # Nueva URL para dar de baja producto en Cocina
    path('cocina/dar_baja/<int:producto_id>/', views.dar_baja_producto, name='dar_baja_producto'),
    # Nueva URL para dar de baja producto en Barra
    path('barra/dar_baja/<int:producto_id>/', views.dar_baja_producto_barra, name='dar_baja_producto_barra'),
]