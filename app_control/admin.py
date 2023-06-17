import imp
from django.contrib import admin
# from .forms import InventoryCreateForm, InventoryPurchaseForm
from app_control.models import (
    CanalPlus, CanalPlusItem, CanalItemAbonnement, CanalItemReabonnement, CanalItemRecharge,
    Inventory, InventoryGroup, InventoryItem, ItemPurchase, ItemSupply, ItemSale, 
    MoneyTransactionDetail, Shop, 
    InvoiceItem, Invoice, Service, IncomeOutcome, IncomeOutcomeItem, IncomeDb, OutcomeDb,
    ServiceGroup, ServiceItem, 
    MoneyType, MoneyTransactionType, MoneyTransaction, MoneyRefill,
    Asset, AssetGroup, Asset, AssetItem, AssetAccessory, AssetPurchase, AssetRepairs, AssetDiscard)

admin.site.register([InventoryGroup, Shop,
        MoneyTransactionType, MoneyTransactionDetail, MoneyRefill,
        AssetGroup,
    ])

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "description", "group", "available_stock", "reorder_level",
    "available_shop", "total_quantity_sold", "total_amount_sold",
    "cost_price_unit", "cost_price_bulk", "selling_price_unit", "selling_price_bulk", "total",
    "active", "created_at",)
    #list_filter = ("id", "code", "name")
    search_fields = ("code__startswith", "id__startswith", "name__startswith")


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("id", "inventory", "purpose", "quantity", "reorder_level",
    "cost_price_unit", "cost_price_bulk", "cost_price_total", "selling_price_unit", "selling_price_bulk",
    "sold_price_unit", "sold_price_bulk", "sold_price_total", "created_at",)
    search_fields = ("inventory__startswith", "id__startswith", "cost_price_unit__startswith")


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    # list_display = ("id", "item_code", "item", "item_name", "quantity", "amount", "created_at")
    list_display = ("id", "item_code", "item_name", "quantity", "amount", "total", "created_at")
    search_fields = ("id", "item_code", "item_name")


@admin.register(Invoice)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ("id", "shop", "created_at")
    search_fields = ("id", "item_code", "item_name")


@admin.register(ItemPurchase)
class ItemPurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "purchaser", "purpose", "inventory", "quantity_unit", "quantity_bulk",
    "cost_price_unit", "cost_price_bulk", "cost_price_total", "created_at",)
    search_fields = ("inventory__startswith", "id__startswith", "purchaser__startswith")


@admin.register(ItemSupply)
class ItemSupplyAdmin(admin.ModelAdmin):
    list_display = ("id", "supplier", "purpose", "inventory", "quantity_unit", "quantity_bulk",
    "selling_price_unit", "selling_price_bulk", "created_at",)
    search_fields = ("inventory__startswith", "id__startswith", "supplier__startswith")


@admin.register(ItemSale)
class ItemSaleAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "purpose", "inventory", "quantity_unit", "quantity_bulk",
    "sold_price_unit", "sold_price_bulk", "sold_price_total", "created_at",)
    search_fields = ("inventory__startswith", "id__startswith", "seller__startswith")


@admin.register(MoneyType)
class MoneyTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "total_refills", "total_amount_cash_out", "total_amount_cash_in", "available_amount", "total_transactions")
    search_fields = ("name", "code", "total")


@admin.register(MoneyTransaction)
class MoneyTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_number", "customer_name", "amount",
    "category", "type", "type2", "created_at")
    search_fields = ("customer_number__startswith", "customer_name__startswith")


@admin.register(CanalPlus)
class CanalPlusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "total", "available_balance", 
    "total_amount_recharged","total_amount_subscribed","total_amount_resubscribed", "active", "reorder_level", "created_at",)
    search_fields = ("code__startswith", "id__startswith", "name__startswith")


@admin.register(CanalPlusItem)
class CanalPlusItemAdmin(admin.ModelAdmin):
    list_display = ("id", "canal_plus", "decoder_number", "purpose", "quantity", "amount", "total_amount", 
    "reorder_level", "comments", "created_at",)
    search_fields = ("canal_plus__startswith", "id__startswith", "quantity__startswith")


@admin.register(CanalItemRecharge)
class CanalItemRechargeAdmin(admin.ModelAdmin):
    list_display = ("id", "recharger", "canal_plus", "amount", "created_at",)
    search_fields = ("canal_plus__startswith", "id__startswith", "recharger__startswith")


@admin.register(CanalItemAbonnement)
class CanalItemAbonnementAdmin(admin.ModelAdmin):
    list_display = ("id", "subscriber", "canal_plus", "phone", "decoder", "amount", "created_at",)
    search_fields = ("canal_plus__startswith", "id__startswith", "subscriber__startswith")


@admin.register(CanalItemReabonnement)
class CanalItemReabonnementAdmin(admin.ModelAdmin):
    list_display = ("id", "resubscriber", "canal_plus", "phone", "decoder", "amount", "created_at",)
    search_fields = ("cana_plus__startswith", "id__startswith", "resubscriber__startswith")


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "description_1", "description_2", "repairs", "total", "cost_price", 
        "quantity", "available_quantity","physical_state"
    )
    search_fields = ("name", "code", "description")


@admin.register(AssetAccessory)
class AssetAccessoryAdmin(admin.ModelAdmin):
    list_display = ("id", "asset", "name", "description_1", "condition",) 
    search_fields = ("name", "code", "description")


@admin.register(AssetItem)
class AssetItemAdmin(admin.ModelAdmin):
    list_display = ("id", "asset", "maintener_discarder", "diagnosis_reason", "cost_price", "quantity", "physical_state")
    search_fields = ("name", "code", "description")

@admin.register(AssetPurchase)
class AssetPurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "purchaser", "asset", "quantity", "cost_price", "total")
    search_fields = ("name", "code", "description")

@admin.register(AssetRepairs)
class AssetRepairsAdmin(admin.ModelAdmin):
    list_display = ("id", "maintener", "asset", "diagnosis", "state", "recommendations", "cost_of_repair")
    search_fields = ("name", "code", "description")

@admin.register(AssetDiscard)
class AssetDiscardAdmin(admin.ModelAdmin):
    list_display = ("id", "person", "asset", "reason", "state", "recommendations")
    search_fields = ("name", "code", "description")

@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "belongs_to", "belongs_to_shop", )
    search_fields = ("code__startswith", "id__startswith", "name__startswith")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "description", "group", "service_cost", "total_quantity_sold", "total_amount_sold", 
    "active", "created_at",)
    search_fields = ("name__startswith", "id__startswith", "code__startswith")

@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "quantity", "paid_amount_unit", "total_amount", 
    "comments_1", "comments_2", "created_at",)
    search_fields = ("service__startswith", "quantity__startswith", "created_at__contains")

@admin.register(IncomeOutcome)
class IncomeOutcomeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "number_of_transactions", "created_at")
    search_fields = ("service__startswith", "id__startswith", "quantity__startswith")

@admin.register(IncomeOutcomeItem)
class IncomeOutcomeItemAdmin(admin.ModelAdmin):
    list_display = ("created_by", "income_outcome", "code", "total_amount", "purpose", "issuer", "reciever", "comments", "created_at")
    search_fields = ("income_outcome__startswith", "id__startswith", "total_amount__startswith")

@admin.register(IncomeDb)
class IncomeDbAdmin(admin.ModelAdmin):
    list_display = ("person", "income_outcome", "total_amount", "reason", "issuer", "reciever", "created_at")
    search_fields = ("person__startswith", "id__startswith", "income_outcome__startswith")

@admin.register(OutcomeDb)
class OutcomeDbAdmin(admin.ModelAdmin):
    list_display = ("person", "income_outcome", "total_amount", "reason", "issuer", "reciever", "created_at")
    search_fields = ("person__startswith", "id__startswith", "total_amount__startswith")
