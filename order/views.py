from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response

from .models import Order, Item, DeliveryAddress
from .serializers import OrderSerializer, ItemSerializer

class OrderUpdateAddressView(APIView):
	@swagger_auto_schema(
		request_body=openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'delivery_address': openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						'street_name': openapi.Schema(type=openapi.TYPE_STRING),
						'number': openapi.Schema(type=openapi.TYPE_STRING),
						'complement': openapi.Schema(type=openapi.TYPE_STRING),
						'reference_point': openapi.Schema(type=openapi.TYPE_STRING),
					},
					required=['street_name', 'number']
				)
			},
			required=['delivery_address']
		),
		responses={200: openapi.Response('Endereço atualizado com sucesso.')}
	)
	def patch(self, request, pk):
		try:
			order = Order.objects.get(pk=pk)
		except Order.DoesNotExist:
			return Response({'detail': 'Pedido não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

		address_data = request.data.get('delivery_address')
		if not address_data:
			return Response({'detail': 'delivery_address é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

		if order.delivery_address:
			for attr, value in address_data.items():
				setattr(order.delivery_address, attr, value)
			order.delivery_address.save()
		else:
			order.delivery_address = DeliveryAddress.objects.create(**address_data)
			order.save()

		return Response({'detail': 'Endereço atualizado com sucesso.'}, status=status.HTTP_200_OK)

class ItemDeleteView(APIView):
	def delete(self, request, pk, item_id):
		try:
			item = Item.objects.get(pk=item_id, order_id=pk)
		except Item.DoesNotExist:
			return Response({'detail': 'Item não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
		item.delete()
		return Response({'detail': 'Item removido com sucesso.'}, status=status.HTTP_204_NO_CONTENT)

class OrderCreateView(generics.CreateAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer

class OrderUpdateView(APIView):
	@swagger_auto_schema(
		request_body=openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'items': openapi.Schema(
					type=openapi.TYPE_ARRAY,
					items=openapi.Schema(
						type=openapi.TYPE_OBJECT,
						properties={
							'name': openapi.Schema(type=openapi.TYPE_STRING),
							'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
							'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal'),
						},
						required=['name', 'quantity', 'unit_price']
					)
				)
			},
			required=['items']
		),
		responses={200: openapi.Response('Itens adicionados com sucesso.')}
	)
	def patch(self, request, pk):
		try:
			order = Order.objects.get(pk=pk)
		except Order.DoesNotExist:
			return Response({'detail': 'Pedido não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

		items_data = request.data.get('items')
		if not items_data:
			return Response({'detail': 'items é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

		errors = []
		created = 0
		for item_data in items_data:
			item_data['order'] = order.id
			serializer = ItemSerializer(data=item_data)
			if serializer.is_valid():
				serializer.save(order=order)
				created += 1
			else:
				errors.append(serializer.errors)
		if errors:
			return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'detail': f'{created} itens adicionados com sucesso.'}, status=status.HTTP_200_OK)

class OrderDetailView(generics.RetrieveAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer


# Documentação Swagger para filtros
class OrderListByDocumentView(generics.ListAPIView):
	serializer_class = OrderSerializer

	@swagger_auto_schema(
		manual_parameters=[
			openapi.Parameter(
				'client_document', openapi.IN_QUERY, description="Documento do cliente (obrigatório)", type=openapi.TYPE_STRING, required=True
			),
			openapi.Parameter(
				'delivery_date', openapi.IN_QUERY, description="Data de entrega (opcional, formato YYYY-MM-DD)", type=openapi.TYPE_STRING, required=False
			),
		]
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	def get_queryset(self):
		document = self.request.query_params.get('client_document')
		delivery_date = self.request.query_params.get('delivery_date')
		queryset = Order.objects.all()
		if document:
			queryset = queryset.filter(client_document=document)
		if delivery_date:
			queryset = queryset.filter(delivery_date=delivery_date)
		return queryset
