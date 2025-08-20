from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order, Item

class OrderAPITestCase(APITestCase):
	def setUp(self):
		self.order_data = {
			"client_name": "João Silva",
			"client_document": "12345678901",
			"delivery_date": "2025-08-20",
			"items": [
				{"name": "Produto A", "quantity": 2, "unit_price": 10.50},
				{"name": "Produto B", "quantity": 1, "unit_price": 20.70}
			]
		}
		self.address_data = {
			"street_name": "Rua das Flores",
			"number": "123",
			"complement": "Apto 45",
			"reference_point": "Próximo à padaria"
		}
		
	def test_create_order_with_address(self):
		url = reverse('order-create')
		data = self.order_data.copy()
		data["delivery_address"] = self.address_data
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["delivery_address"]["street_name"], self.address_data["street_name"])

	def test_update_address(self):
		# Cria pedido sem endereço
		url = reverse('order-create')
		response = self.client.post(url, self.order_data, format='json')
		order_id = response.data['id']
		update_url = reverse('order-update-address', args=[order_id])
		response = self.client.patch(update_url, {"delivery_address": self.address_data}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# Busca pedido e verifica endereço
		detail_url = reverse('order-detail', args=[order_id])
		response = self.client.get(detail_url, format='json')
		self.assertEqual(response.data["delivery_address"]["street_name"], self.address_data["street_name"])

	def test_delete_item(self):
		# Cria pedido
		url = reverse('order-create')
		response = self.client.post(url, self.order_data, format='json')
		order_id = response.data['id']
		item_id = response.data['items'][0]['id']
		delete_url = reverse('order-item-delete', args=[order_id, item_id])
		response = self.client.delete(delete_url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		# Verifica se item foi removido
		detail_url = reverse('order-detail', args=[order_id])
		response = self.client.get(detail_url, format='json')
		self.assertEqual(len(response.data['items']), 1)

	def test_create_order_invalid(self):
		url = reverse('order-create')
		data = self.order_data.copy()
		data["client_name"] = ""  # Nome obrigatório
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_update_order_with_invalid_item(self):
		url = reverse('order-create')
		response = self.client.post(url, self.order_data, format='json')
		order_id = response.data['id']
		update_url = reverse('order-update', args=[order_id])
		# Falta campo obrigatório 'name'
		new_items = {"items": [{"quantity": 1, "unit_price": 5.20}]}
		response = self.client.patch(update_url, new_items, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_order(self):
		url = reverse('order-create')
		response = self.client.post(url, self.order_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Order.objects.count(), 1)
		self.assertEqual(Item.objects.count(), 2)

	def test_update_order_with_new_items(self):
		# Cria pedido inicial
		url = reverse('order-create')
		response = self.client.post(url, self.order_data, format='json')
		order_id = response.data['id']
		update_url = reverse('order-update', args=[order_id])
		new_items = {"items": [{"name": "Produto C", "quantity": 3, "unit_price": 5.10}]}
		response = self.client.patch(update_url, new_items, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Item.objects.filter(order_id=order_id).count(), 3)

	def test_retrieve_order_with_total_price(self):
		# Cria pedido
		url = reverse('order-create')
		response = self.client.post(url, self.order_data, format='json')
		order_id = response.data['id']
		detail_url = reverse('order-detail', args=[order_id])
		response = self.client.get(detail_url, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('total_price', response.data)
		self.assertEqual(float(response.data['total_price']), 41.70)

	def test_create_order_without_items(self):
		url = reverse('order-create')
		data = self.order_data.copy()
		data.pop('items')
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(len(response.data['items']), 0)

	def test_update_address_overwrite(self):
		url = reverse('order-create')
		data = self.order_data.copy()
		data["delivery_address"] = self.address_data
		response = self.client.post(url, data, format='json')
		order_id = response.data['id']
		update_url = reverse('order-update-address', args=[order_id])
		new_address = self.address_data.copy()
		new_address['street_name'] = 'Rua Nova'
		response = self.client.patch(update_url, {"delivery_address": new_address}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		detail_url = reverse('order-detail', args=[order_id])
		response = self.client.get(detail_url, format='json')
		self.assertEqual(response.data["delivery_address"]["street_name"], 'Rua Nova')

	def test_list_order_by_document_and_date(self):
		url = reverse('order-create')
		self.client.post(url, self.order_data, format='json')
		list_url = reverse('order-list-by-document')
		params = {'client_document': self.order_data['client_document'], 'delivery_date': self.order_data['delivery_date']}
		response = self.client.get(list_url, params)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertGreaterEqual(len(response.data), 1)

	def test_delete_nonexistent_item(self):
		url = reverse('order-create')
		response = self.client.post(url, self.order_data, format='json')
		order_id = response.data['id']
		delete_url = reverse('order-item-delete', args=[order_id, 9999])
		response = self.client.delete(delete_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_create_order_with_incomplete_address(self):
		url = reverse('order-create')
		data = self.order_data.copy()
		data["delivery_address"] = {"number": "123"}  # falta street_name
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_order_with_negative_quantity(self):
		url = reverse('order-create')
		data = self.order_data.copy()
		data['items'][0]['quantity'] = -1
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_order_with_negative_unit_price(self):
		url = reverse('order-create')
		data = self.order_data.copy()
		data['items'][0]['unit_price'] = -10.99
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_created_at_and_updated_at_fields(self):
		url = reverse('order-create')
		data = self.order_data.copy()
		data["delivery_address"] = self.address_data
		response = self.client.post(url, data, format='json')
		order_id = response.data['id']
		order = Order.objects.get(id=order_id)
		self.assertIsNotNone(order.created_at)
		self.assertIsNotNone(order.updated_at)
		item = Item.objects.filter(order=order).first()
		self.assertIsNotNone(item.created_at)
		self.assertIsNotNone(item.updated_at)
		self.assertIsNotNone(order.delivery_address.created_at)
		self.assertIsNotNone(order.delivery_address.updated_at)