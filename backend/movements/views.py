from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework import status
from .models import Cliente, Categoria, Cuenta, Movimiento
from .serializers import ClienteSerializer, CategoriaSerializer, CuentaSerializer, MovimientoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """
    Conjunto de vistas para el modelo Cliente.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=True, methods=['post'], url_path='agregar-categoria', url_name='agregar-categoria')
    def agregar_categoria(self, request, pk=None):
        """
        Agrega un cliente a una categoría específica.
        """
        cliente = self.get_object()
        categoria_id = request.data.get('categoria_id')
        categoria = get_object_or_404(Categoria, id=categoria_id)

        cliente.agregar_a_categoria(categoria)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CuentaViewSet(viewsets.ModelViewSet):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

class SaldoView(APIView):
    def get(self, request, pk):
        try:
            cliente = get_object_or_404(Cliente, id=pk)
            cuenta_cliente = Cuenta.objects.filter(cliente=cliente).first()
            if not cuenta_cliente:
                raise NotFound(detail="Cuenta no encontrada para el cliente.")

            valor_dolar_bolsa = cuenta_cliente.obtener_valor_dolar_bolsa()
            saldo_movimientos_total = list(cuenta_cliente.get_saldo_movimientos())
            saldo_usd_total = cuenta_cliente.get_total_usd(valor_dolar_bolsa)

            cuenta_serializer = CuentaSerializer(cuenta_cliente, context={'valor_dolar_bolsa': valor_dolar_bolsa})
            cuenta_data = cuenta_serializer.data

            return JsonResponse({
                "saldo_movimientos": saldo_movimientos_total,
                "saldo_usd": saldo_usd_total,
                "cuenta_data": cuenta_data,
            }, status=status.HTTP_200_OK)

        except Cliente.DoesNotExist:
            raise NotFound(detail="Cliente no encontrado")
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
