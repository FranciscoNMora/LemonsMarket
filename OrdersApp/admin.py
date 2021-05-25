from django.contrib import admin

from OrdersApp.models import Stock, Order


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('isin', 'name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'stock', 'side', 'quantity')
    list_filter = ('stock',)
    readonly_fields = ('uuid', 'created',)
    ordering = ('-created',)

