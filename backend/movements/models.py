from django.db import models, transaction
from django.db.models import Sum, F, Value, Case, When
import requests

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)

    def agregar_a_categoria(self, categoria):
        """
        Agrega al cliente a una categoría específica.
        """
        CategoriaCliente.objects.create(cliente=self, categoria=categoria)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

class CategoriaCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Cuenta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def get_total_usd(self, valor_dolar_bolsa):
        try:
            valor_dolar_bolsa = self.obtener_valor_dolar_bolsa()
            return float(self.get_total_saldo()) * valor_dolar_bolsa
        except ValueError as e:
            print(f"Error al obtener el valor del dólar: {e}")
            return None

    def get_total_saldo(self):
        ingresos = self.movimientos.aggregate(
            saldo_movimientos=Sum(
                Case(
                    When(tipo='Ingreso', then=F('importe')),
                    default=Value(0),
                    output_field=models.DecimalField(),
                )
            )
        )['saldo_movimientos'] or 0

        egresos = self.movimientos.aggregate(
            saldo_movimientos=Sum(
                Case(
                    When(tipo='Egreso', then=F('importe')),
                    default=Value(0),
                    output_field=models.DecimalField(),
                )
            )
        )['saldo_movimientos'] or 0

        saldo = ingresos - egresos
        return saldo

    def get_saldo_movimientos(self):
        try:
            return self.__class__.objects.filter(cliente=self.cliente).annotate(
                saldo_movimientos=Sum(
                    Case(
                        When(movimientos__tipo='Ingreso', then=F('movimientos__importe')),
                        When(movimientos__tipo='Egreso', then=-F('movimientos__importe')),
                        default=0,
                        output_field=models.DecimalField(),
                    )
                )
            ).values('saldo_movimientos')
        except Exception as e:
            raise ValueError(f"No se pudo obtener el saldo de movimientos: {str(e)}")
        
    def obtener_valor_dolar_bolsa(self):
        dolar_bolsa_response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        dolar_bolsa_data = dolar_bolsa_response.json()
        dolar_bolsa_raw = next((item['casa'] for item in dolar_bolsa_data if item['casa']['nombre'] == 'Dolar Bolsa'), None)
        valor_dolar_bolsa_str = dolar_bolsa_raw['compra'].replace('.', '').replace(',', '.')
        
        if not valor_dolar_bolsa_str:
            raise ValueError("No se pudo obtener el valor del dólar.")
            
        return float(valor_dolar_bolsa_str)

class Movimiento(models.Model):
    TIPO_CHOICES = [('Ingreso', 'Ingreso'), ('Egreso', 'Egreso')]

    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()

    def save(self, *args, **kwargs):
        """
        Guarda el movimiento y valida el saldo suficiente en caso de un Egreso.
        """
        with transaction.atomic():
            if self.tipo == 'Egreso' and self.importe > self.cuenta.get_total_saldo():
                raise ValueError("Saldo insuficiente para realizar el Egreso.")
            super().save(*args, **kwargs)
