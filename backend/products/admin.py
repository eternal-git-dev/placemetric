from django.contrib import admin
from django.db.models import QuerySet
from .models import TelegramAccount, Product, ProductItem, PriceSnapshot, Niche


@admin.register(TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_id', 'created_at')
    list_filter = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'root', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'nm', 'name', 'is_tracked', 'is_alive', 'created_at')
    list_filter = ('is_tracked', 'is_alive', 'created_at')
    search_fields = ('name',)

    list_select_related = ('product',)


@admin.register(PriceSnapshot)
class PriceSnapshotAdmin(admin.ModelAdmin):
    list_display = ('item', 'option_id', 'size_name', 'price', 'basic_price', 'stock', 'rating', 'reviews_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('item__name',)
    date_hierarchy = 'created_at'
    list_select_related = ('item',)


@admin.register(Niche)
class NicheAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'products_count')
    search_fields = ('user__username', 'name')


    def products_count(self, obj: Niche) -> int:
        """Возвращает количество связанных продуктов для данной ниши."""
        return obj.products.count()

    products_count.short_description = "Количество товаров"
