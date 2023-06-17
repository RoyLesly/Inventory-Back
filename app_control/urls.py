from django.urls import path, include
from rest_framework import routers
from user_control.models import UserActivities
# from . import views
from app_control.views import (
    AssetGroupView, AssetItemView, InventoryItemView, NewServiceItemView, ShopView, SummaryView, PurchaseView, SupplyView, SaleByShopView, 
    InventoryGroupView, ServiceGroupView, MegaSummaryOneView, MegaSummaryTwoView, SalePerformanceView,
    # InventoryItemViewTest, 
    MoneyItemView, MoneyCategoryView, MoneyTransactionTypeView, MoneyTransactionDetailView, UploadView, InvoiceView, InventoryCSVLoaderView, 
    ServiceItemView, ServiceView, CanalItemView, CanalPlusView, GetCanalAbonnementView, GetCanalRechargeView, GetCanalReabonnementView,
    GetIncomeOutcomeView, GetIncomeOutcomeItemView, GetIncomeOutcomeDetailView, InventoryItemPurchaseView, InventoryItemSupplyView, InventoryItemSaleView
)

app_name = "app_control"

router = routers.DefaultRouter(trailing_slash=False)

router.register("inventory-item", InventoryItemView, "inventory-item")
router.register("inventory-item-purchase", InventoryItemPurchaseView, "inventory-item-purchase")
router.register("inventory-item-supply", InventoryItemSupplyView, "inventory-item-supply")
router.register("inventory-item-sale", InventoryItemSaleView, "inventory-item-sale")
router.register("service", ServiceView, "service")
router.register("service-item", NewServiceItemView, "service-item")
router.register("service-details", NewServiceItemView, "service-item")

router.register("money-item", MoneyItemView, "money-item")
router.register("money-item-summary", MoneyCategoryView, "money-item")
router.register("money-transaction-category", MoneyCategoryView, "money-transaction-category")
router.register("money-transaction-type", MoneyTransactionTypeView, "money-transaction-type")
router.register("money-transaction-type-detail", MoneyTransactionDetailView, "money-transaction-detail")
router.register("canal-transaction", CanalItemView, "canal-transaction")
router.register("canal-recharge-transaction", GetCanalRechargeView, "canal-recharge-transaction")
router.register("canal-abonnement-transaction", GetCanalAbonnementView, "canal-abonnement-transaction")
router.register("canal-reabonnement-transaction", GetCanalReabonnementView, "canal-reabonnement-transaction")
router.register("income-outcome", GetIncomeOutcomeView, "income-outcome")
router.register("income-outcome-details", GetIncomeOutcomeDetailView, "income-outcome-detail")
router.register("income", GetIncomeOutcomeItemView, "income-outcome")
router.register("outcome", GetIncomeOutcomeItemView, "income-outcome")

router.register("asset-item", AssetItemView, "asset-item")

router.register("inventory-csv", InventoryCSVLoaderView, "login")
router.register("shop", ShopView, "shop")
# router.register("summary", SummaryView, "summary")
router.register("summary", SummaryView, "summary")
router.register("purchase-summary", PurchaseView, "purchase-summary")
router.register("sale-by-shop", SaleByShopView, "sale-by-shop")
router.register("group", InventoryGroupView, "group")
router.register("canal-plus", CanalPlusView, "canal-plus")
router.register("asset-group", AssetGroupView, "asset-group")
router.register("service-group", ServiceGroupView, "service-group")
router.register("top-selling", SalePerformanceView, "top-selling")
router.register("purchase", PurchaseView, "purchase")
router.register("supply", SupplyView, "supply")
router.register("invoice", InvoiceView, "invoice")
router.register("uploads", UploadView, "invoice")
router.register("mega-summary-one", MegaSummaryOneView, "mega-summary-one")
router.register("mega-summary-two", MegaSummaryTwoView, "mega-summary-two")

urlpatterns = [
    path('/', include(router.urls)),
    # path('purchase', purchase_view),
]
