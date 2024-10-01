# views.py

import io
from rest_framework import viewsets
from .models import Category, StockItem
from .serializers import CategorySerializer, StockItemSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from openpyxl import Workbook

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'name'

    def get_queryset(self):
        queryset = super().get_queryset()
        shop = self.request.query_params.get('shop')
        if shop:
            queryset = queryset.filter(shop=shop)
        return queryset

class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.request.query_params.get('category')
        shop = self.request.query_params.get('shop')

        if shop:
            # Filter items by shop
            queryset = queryset.filter(category__shop=shop)
        
        if category_name:
            # Filter items by category if provided
            category = get_object_or_404(Category, name=category_name)
            queryset = queryset.filter(category=category)
        
        return queryset


def download_shop_items(request, shop_id):
    try:
        # Query data
        items = StockItem.objects.filter(category__shop=shop_id).order_by('-id')
        
        # Create an Excel workbook and sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Shop Items"

        # Define the headers
        headers = ["Code", "G.wt", "N.wt", "Kund", "K-amt", "Moti", "M-amt", "PO", "P-amt", "Pcs", "Supp", 'Category Name', "Image"]
        ws.append(headers)

        # Add data rows
        for item in items:
            row = [
                item.code,
                item.gw,
                item.nw,
                item.kundan,
                item.k_amt,
                item.moti,
                item.m_amt,
                item.po,
                item.p_amt,
                item.pcs,
                item.supplier,
                item.category.name,
                item.image.url if item.image else 'No Image'  # Handle image URL
            ]
            ws.append(row)
        
        # Save the workbook to a BytesIO object
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        # Return the file as a downloadable response
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=shop_{shop_id}_stock_items.xlsx'
        return response

    except Exception as e:
        # Handle errors and provide feedback
        return HttpResponse(f"Failed to generate Excel file: {str(e)}", status=500)