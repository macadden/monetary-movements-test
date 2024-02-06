from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, CategoriaViewSet, CuentaViewSet, MovimientoViewSet, SaldoView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'cuentas', CuentaViewSet)
router.register(r'movimientos', MovimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('clientes/<int:pk>/saldo/', SaldoView.as_view(), name='cliente-saldo'),
]
