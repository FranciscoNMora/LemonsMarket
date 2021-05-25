from django.shortcuts import render

from rest_framework import mixins, generics, permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from OrdersApp.models import Stock
from OrdersApp.serializers import OrderSerializer, StockSerializer
from OrdersApp.utils import utc_now


class OrdersAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        """
        Creates a new Order.
        The JSON file must have the following fields:
            i. isin (String, 12 chars (this identifies a stock)). Note: the stock that the ISIN identify must exists in
                DB, see /v1/stocks/ endpoint.
            ii. limit_price (Float, always >0)
            iii. side (Enum: buy | sell, case sensitive tolerant)
            iv. valid_until (Integer, Unix UTC Timestamp)
            v. quantity (Integer, always >0)
        """
        serializer = self.serializer_class(data=request.data, context={'now': utc_now()})
        if serializer.is_valid():
            o = serializer.save()
            return Response(data={'order_uuid': o.uuid}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockListAPI(ListAPIView, mixins.CreateModelMixin):
    """
    It shows the list of available Stocks
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def post(self, request, *args, **kwargs):
        """
        Creates new stock
        """
        return self.create(request, *args, **kwargs)
