from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Cliente, Categoria, Cuenta, Movimiento
from unittest.mock import patch

class MovementsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear datos de prueba
        self.cliente = Cliente.objects.create(nombre="Cliente de prueba")
        self.categoria = Categoria.objects.create(nombre="Categoria de prueba")
        self.cuenta = Cuenta.objects.create(cliente=self.cliente)
        self.movimiento = Movimiento.objects.create(cuenta=self.cuenta, tipo='Ingreso', importe=100, fecha='2024-02-01')


    @patch('movements.models.requests.get')
    def test_consultar_cliente_saldo(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"casa": {"compra": "1196,690", "venta": "1197,830", "nombre": "Dolar Bolsa"}}
        ]

        url = reverse('cliente-saldo', kwargs={'pk': self.cliente.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        json_data = response.json()
        
        # Verifica que las claves esperadas están presentes en los datos JSON
        self.assertIn('saldo_movimientos', json_data)
        self.assertIn('saldo_usd', json_data)
        self.assertIn('cuenta_data', json_data)

    @patch('movements.models.requests.get')
    def test_registrar_cuenta(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"casa": {"compra": "1.196,690", "venta": "1.197,830", "nombre": "Dolar Bolsa"}}
        ]

        url = reverse('cuenta-list')
        data = {'cliente': self.cliente.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('movements.models.requests.get')
    def test_listar_cuentas(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"casa": {"compra": "1.196,690", "venta": "1.197,830", "nombre": "Dolar Bolsa"}}
        ]

        url = reverse('cuenta-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_listar_clientes(self):
        url = reverse('cliente-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_registrar_cliente(self):
        url = reverse('cliente-list')
        data = {'nombre': 'Nuevo Cliente'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_eliminar_cliente(self):
        url = reverse('cliente-detail', args=[self.cliente.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_editar_cliente(self):
        url = reverse('cliente-detail', args=[self.cliente.id])
        data = {'nombre': 'Cliente Modificado'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Cliente Modificado')


    def test_agregar_categoria_a_cliente(self):
        url = reverse('cliente-agregar-categoria', args=[self.cliente.id])
        data = {'categoria_id': self.categoria.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_listar_categorias(self):
        url = reverse('categoria-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_registrar_categoria(self):
        url = reverse('categoria-list')
        data = {'nombre': 'Nueva Categoria'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_eliminar_categoria(self):
        url = reverse('categoria-detail', args=[self.categoria.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_eliminar_cuenta(self):
        url = reverse('cuenta-detail', args=[self.cuenta.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    def test_registrar_movimiento(self):
        url = reverse('movimiento-list')
        data = {'cuenta': self.cuenta.id, 'tipo': 'Ingreso', 'importe': 50, 'fecha': '2024-02-01'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_eliminar_movimiento(self):
        url = reverse('movimiento-detail', args=[self.movimiento.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_consultar_movimiento(self):
        url = reverse('movimiento-detail', args=[self.movimiento.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cuenta'], self.cuenta.id)
        self.assertEqual(response.data['tipo'], 'Ingreso')
        

    def test_listar_movimientos(self):
        url = reverse('movimiento-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        


    def test_registrar_cliente_sin_nombre(self):
        url = reverse('cliente-list')
        data = {'nombre': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_registrar_movimiento_sin_cuenta(self):
        url = reverse('movimiento-list')
        data = {'tipo': 'Ingreso', 'importe': 50, 'fecha': '2024-02-01'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_eliminar_cliente_inexistente(self):
        url = reverse('cliente-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_eliminar_movimiento_inexistente(self):
        url = reverse('movimiento-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_agregar_categoria_a_cliente_inexistente(self):
        url = reverse('cliente-agregar-categoria', args=[999])
        data = {'categoria_id': self.categoria.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_consultar_movimiento_inexistente(self):
        url = reverse('movimiento-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_listar_clientes_vacio(self):
        Cliente.objects.all().delete()
        url = reverse('cliente-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


    def test_registrar_movimiento_egreso_sin_saldo_suficiente(self):
        url = reverse('movimiento-list')
        # Crear un movimiento de tipo Egreso con un importe mayor al saldo disponible, el cual es 100
        data = {'cuenta': self.cuenta.id, 'tipo': 'Egreso', 'importe': 150, 'fecha': '2024-02-01'}
        try:
            response = self.client.post(url, data, format='json')
        except ValueError as e:
            self.assertIn("Saldo insuficiente para realizar el Egreso", str(e))
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['saldo'][0], 'Saldo insuficiente para realizar el movimiento')
