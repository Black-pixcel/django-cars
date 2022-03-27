from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic.base import View
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets  # status, generics
from django.db.models import Sum
from .serializers import *
from .models import *
# from django.forms import model_to_dict
# from datetime import date
# from django.db import connection
# from rest_framework import generics
# from rest_framework.views import APIView
# from django.views import generic

# Create your views here.


# class OrdersView(View):
#     """Список заказов"""
#     def get(self, request):
#         orders = Orders.objects.all()
#         return render(request, 'carsbase/base.html', {'orders_list': orders})


def zero_if_null(value):
    return 0 if value is None else value


class OrdersViewFull(View):
    """Список заказов"""
    def get(self, request):
        brands_filter = request.GET.getlist('brand')
        if len(brands_filter) > 0:
            data = Orders.objects.filter(model__in=Models.objects.filter(brand__in=Brands.objects.filter(name__in=brands_filter)))
        else:
            data = Orders.objects.all()
        order = request.GET.get('order')
        if order == 'desc':
            data = data.order_by('-count')
        else:
            data = data.order_by('count')
        brands_list = Brands.objects.all()
        queryset = Paginator(data, 10).get_page(request.GET.get('page', 1))
        columns = ['ID', 'Дата', 'Цвет', 'Марка', 'Модель', 'Количество']
        result = [{'id': row.id,
                   'order_date': row.order_date,
                   'color': row.color.name,
                   'brand': row.model.brand.name,
                   'model': row.model.name,
                   'count': row.count}
                  for row in queryset]
        out_dict = {'queryset': queryset, 'columns': columns, 'orders_list': result, 'brands_list': brands_list}
        return render(request, 'carsbase/base.html', out_dict)


class ColorsViewSet(viewsets.ModelViewSet):
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer

    @action(methods=['get'], detail=False)
    def summary(self, request):
        queryset = Colors.objects.all()
        result = [{'color': row.name,
                   'count_cars': zero_if_null(Orders.objects.filter(color=row).aggregate(count=Sum('count'))['count'])}
                  for row in queryset]
        return Response(result)


class BrandsViewSet(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer

    @action(methods=['get'], detail=False)
    def summary(self, request):
        queryset = Brands.objects.all()
        result = [{'brand': row.name,
                   'count_cars': zero_if_null(Orders.objects.filter(model__in=Models.objects.filter(brand=row)).aggregate(count=Sum('count'))['count'])}
                  for row in queryset]
        return Response(result)


class ModelsViewSet(viewsets.ModelViewSet):
    queryset = Models.objects.all()
    serializer_class = ModelsSerializer

    @action(methods=['get'], detail=False)
    def view(self, request):
        queryset = Models.objects.all()
        result = [{'name': row.name,
                   'brand': row.brand.name}
                  for row in queryset]
        return Response(result)

    @action(methods=['get'], detail=False)
    def summary(self, request):
        queryset = Models.objects.all()
        result = [{'model': row.name,
                   'count_cars': zero_if_null(Orders.objects.filter(model=row).aggregate(count=Sum('count'))['count'])}
                  for row in queryset]
        return Response(result)


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    @action(methods=['get'], detail=False)
    def view(self, request):
        queryset = Orders.objects.all()
        result = [{'order_date': row.order_date,
                   'color': row.color.name,
                   'brand': row.model.brand.name,
                   'model': row.model.name,
                   'count': row.count}
                  for row in queryset]
        return Response(result)



# class OrdersAPIView(generics.ListAPIView):
#     """Список заказов"""
#     queryset = Orders.objects.all()
#     serializer_class = OrdersSerializer


# class OrdersAPIView(APIView):
#     def get(self, request):
#         # queryset = Orders.objects.all().values()
#         # queryset = Orders.objects.select_related('color', 'model').values()
#         # cursor = connection.cursor()
#         # cursor.execute("""select co.order_date as order_date,
#         #                            cc.name as color,
#         #                            cb.name as brand,
#         #                            cm.name as model,
#         #                            co.count as count
#         #                     from postgres.public.carsbase_orders co
#         #                     join carsbase_colors cc on co.color_id = cc.id
#         #                     join carsbase_models cm on co.model_id = cm.id
#         #                     join carsbase_brands cb on cm.brand_id = cb.id""")
#         #
#         # def dictfetchall(cursor):
#         #     columns = [col[0] for col in cursor.description]
#         #     return [dict(zip(columns, row)) for row in cursor.fetchall()]
#         # queryset = dictfetchall(cursor)
#         queryset = Orders.objects.all()
#         result = [{'order_date': row.order_date,
#                    'color': row.color.name,
#                    'brand': row.model.brand.name,
#                    'model': row.model.name,
#                    'count': row.count}
#                   for row in queryset]
#         # return Response({'posts': list(queryset)})
#         # return Response({'get': OrdersSerializer(queryset, many=True).data})
#         return Response(result)
#
#
#     def post(self, request):
#         serializer = OrdersSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             color = Colors.objects.get(name=request.data['color'])
#         except Colors.DoesNotExist:
#             return Response({'color': 'Полученного значения нет в модели Colors'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             brand = Brands.objects.get(name=request.data['brand'])
#         except Brands.DoesNotExist:
#             return Response({'brand': 'Полученного значения нет в модели Brands'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             model = Models.objects.get(name=request.data['model'], brand=brand.id)
#         except Models.DoesNotExist:
#             return Response({'model': 'Полученного значения нет в модели Models'}, status=status.HTTP_400_BAD_REQUEST)
#         post_new = Orders.objects.create(
#             color=color,
#             model=model,
#             count=request.data['count'],
#             order_date=request.data.get('order_date', date.today()),
#         )
#         # post_new = Models.objects.get(name=request.data['model'], brand=Brands.objects.get(name=request.data['brand']).id)
#         result = {'order_date': post_new.order_date,
#                   'color': post_new.color.name,
#                   'brand': brand.name,
#                   'model': model.name,
#                   'count': post_new.count}
#         # return Response(model_to_dict(post_new))
#         return Response(result)
#         # return Response({'post': model_to_dict(Colors.objects.get(name='Белый'))})
#
#
#     def put(self, request):
#         # brand = Brands.objects.get(name=request.data['brand'])
#         try:
#             brand = Brands.objects.get(name=request.data['brand'])
#         except Brands.DoesNotExist:
#             return Response({'brand': 'Полученного значения нет в модели Brands'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(brand.name)


# class OrdersAPIView_new(generics.UpdateAPIView):
#     queryset = Orders.objects.all()
#     serializer_class = OrdersSerializer
