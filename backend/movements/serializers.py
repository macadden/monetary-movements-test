from rest_framework import serializers
from .models import Categoria, Cliente, Cuenta, Movimiento

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = '__all__'

class CuentaSerializer(serializers.ModelSerializer):
    saldo_usd = serializers.SerializerMethodField()

    def get_saldo_usd(self, obj):
        try:
            valor_dolar_bolsa = self.context.get('valor_dolar_bolsa')
            return obj.get_total_usd(valor_dolar_bolsa)
        except ValueError:
            return None

    class Meta:
        model = Cuenta
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'
