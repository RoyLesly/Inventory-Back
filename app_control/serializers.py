# from asyncore import read, write
# from re import T
from statistics import mode
from django.forms import IntegerField
from rest_framework import serializers
from app_control.models import ( Asset, AssetGroup, CanalPlus, CanalPlusItem, 
    InventoryGroup, MoneyTransaction, MoneyTransactionDetail, MoneyTransactionType, MoneyType, ServiceGroup, 
    Inventory, Service, InventoryItem, ItemSupply, ServiceItem, Shop, Invoice, InvoiceItem, ItemPurchase, ItemSupply, ItemSale,
    CanalItemAbonnement, CanalItemRecharge, CanalItemReabonnement, IncomeOutcome, IncomeOutcomeItem, 
)
from user_control.serializers import CustomUserSerializer


# ========================= INVENTORY SECTION =======================================
class InventoryGroupSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    belongs_to = serializers.SerializerMethodField(read_only=True)
    belongs_to_id = serializers.CharField(write_only=True, required=False)
    total_items = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = InventoryGroup
        fields = "__all__"

    def get_belongs_to(self, obj):
        if obj.belongs_to is not None:
            return InventoryGroupSerializer(obj.belongs_to).data
        return None


class InventorySerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    group = InventoryGroupSerializer(read_only=True)
    group_id = serializers.CharField(write_only=True)
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Inventory
        fields = "__all__"


class ItemPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPurchase
        fields = "__all__"


class ItemSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSupply
        fields = "__all__"


class ItemPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSale
        fields = "__all__"


class InventoryWithSumSerializer(InventorySerializer):
    sum_of_item = serializers.IntegerField()


class InventoryItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        item = InventoryItem.objects.create(**validated_data)
        item.save()
        return item

    class Meta:
        model = InventoryItem
        fields = "__all__"


class InventoryItemWithSumSerializer(InventoryItemSerializer):
    sum_of_item = serializers.IntegerField()


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class ServiceGroupSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    belongs_to = serializers.SerializerMethodField(read_only=True)
    belongs_to_id = serializers.CharField(write_only=True, required=False)
    belongs_to_shop = ShopSerializer(read_only=True)
    belongs_to_shop_id = serializers.CharField(write_only=True, required=False)
    total_items = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = ServiceGroup
        fields = "__all__"

    def get_belongs_to(self, obj):
        if obj.belongs_to is not None:
            return ServiceGroupSerializer(obj.belongs_to).data
        return None


class ServiceSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    group = ServiceGroupSerializer(read_only=True)
    group_id = serializers.CharField(write_only=True)

    class Meta:
        model = Service
        fields = "__all__"

class ServicesWithSumSerializer(ServiceSerializer):
    sum_of_item = serializers.IntegerField()


class ServiceItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        item = ServiceItem.objects.create(**validated_data)
        item.save()
        return item

    class Meta:
        model = ServiceItem
        fields = "__all__"


class GetServiceItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = ServiceItem
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = MoneyType
        fields = "__all__"


class MoneyTransactionTypeSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = MoneyTransactionType
        fields = "__all__"


class MoneyTransactionDetailSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = MoneyTransactionDetail
        fields = "__all__"


class MoneyTransactionSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    category = CategorySerializer(read_only=True)
    category_id = serializers.CharField(write_only=True, required=False)
    type = MoneyTransactionTypeSerializer(read_only=True)
    type_id = serializers.CharField(write_only=True, required=False)
    type2 = MoneyTransactionDetailSerializer(read_only=True)
    type2_id = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = MoneyTransaction
        fields = "__all__"


class MoneyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoneyType
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    amount_total = serializers.CharField(read_only=True, required=False)
    count_total = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Shop
        fields = "__all__"


class ShopWithAmountSerializer(ShopSerializer):
    amount_total = serializers.FloatField()
    month = serializers.CharField(required=False)

# ===================================   INVOICE SECTION ===================================
class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = serializers.CharField(read_only=True)
    invoice_id = serializers.CharField(write_only=True)
    item = InventorySerializer(read_only=True)
    item_id = serializers.CharField(write_only=True)

    class Meta:
        model = InvoiceItem
        fields = "__all__"

    # def create(self, validated_data):
    #     print("validated_data: ", validated_data)



class InvoiceItemDataSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    quantity = serializers.IntegerField()
    amount = serializers.IntegerField()
    total = serializers.IntegerField()


class InvoiceSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    shop = ShopSerializer(read_only=True)
    shop_id = serializers.CharField(write_only=True)
    invoice_items = InvoiceItemSerializer(read_only=True, many=True)
    invoice_item_data = InvoiceItemDataSerializer(write_only=True, many=True)

    class Meta:
        model = Invoice
        fields = "__all__"

    def create(self, validated_data):
        invoice_item_data = validated_data.pop("invoice_item_data")
        if not invoice_item_data:
            raise Exception("You need to provide atleast 1 invoice item")
        invoice = Invoice.objects.create(**validated_data)
        updated_data = [
            {"invoice_id": invoice.id, **item} for item in invoice_item_data
        ]

        invoice_item_serializer = InvoiceItemSerializer(data = updated_data, many=True)

        if invoice_item_serializer.is_valid():
            invoice_item_serializer.save()
            print("valid  and saved")
        else:
            invoice.delete()
            print("not saved")
            raise Exception(invoice_item_serializer.errors)

        return invoice


# ==================================   INVENTORY ITEM SECTION ===================================
# ================ PURCHASE SUB-SECTION ================
class ItemPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPurchase
        fields = "__all__"

# ================ SUPPLY SUB-SECTION ================
class ItemSupplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ItemSupply
        fields = "__all__"

# ================ SALE SUB-SECTION ================
class ItemSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSale
        fields = "__all__"


class InventoryItemDataSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    quantity = serializers.IntegerField()


class PurchaseSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    inventory_items = ItemPurchaseSerializer(read_only=True, many=True)
    inventory_item_data = InventoryItemDataSerializer(write_only=True, many=True)

    class Meta:
        model = InventoryItem
        fields = "__all__"

    def create(self, validated_data):
        inventory_item_data = validated_data.pop("inventory_item_data")
        if not inventory_item_data:
            raise Exception("You need to provide atleast 1 inventory item")

        inventory_item = InventoryItem.objects.create(**validated_data)
        #inventory_item = super().create(**validated_data)

        inventory_item_serializer = ItemPurchaseSerializer(data=[
            {"inventory_id": inventory_item.id, **item} for item in inventory_item_data
        ], many=True)

        if inventory_item_serializer.is_valid():
            inventory_item_serializer.save()
        else:
            inventory_item.delete()
            raise Exception(inventory_item_serializer.errors)

        return inventory_item

    
class SupplySerializer(serializers.ModelSerializer):
        created_by = CustomUserSerializer(read_only=True)
        created_by_id = serializers.CharField(write_only=True, required=False)
        inventory_items = ItemSupplySerializer(read_only=True, many=True)
        inventory_item_data = InventoryItemDataSerializer(write_only=True, many=True)

        class Meta:
            model = InventoryItem
            fields = "__all__"

        def create(self, validated_data):
            inventory_item_data = validated_data.pop("inventory_item_data")
            if not inventory_item_data:
                raise Exception("You need to provide atleast 1 inventory item")

            inventory_item = InventoryItem.objects.create(**validated_data)
            #inventory_item = super().create(**validated_data)

            inventory_item_serializer = ItemSupplySerializer(data=[
                {"inventory_id": inventory_item.id, **item} for item in inventory_item_data
            ], many=True)

            if inventory_item_serializer.is_valid():
                inventory_item_serializer.save()
            else:
                inventory_item.delete()
                raise Exception(inventory_item_serializer.errors)

            return inventory_item

    
class SupplySerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    inventory_items = ItemSupplySerializer(read_only=True, many=True)
    inventory_item_data = InventoryItemDataSerializer(write_only=True, many=True)

    class Meta:
        model = InventoryItem
        fields = "__all__"

    def create(self, validated_data):
        inventory_item_data = validated_data.pop("inventory_item_data")
        if not inventory_item_data:
            raise Exception("You need to provide atleast 1 inventory item")

        inventory_item = InventoryItem.objects.create(**validated_data)
        #inventory_item = super().create(**validated_data)

        inventory_item_serializer = ItemSaleSerializer(data=[
            {"inventory_id": inventory_item.id, **item} for item in inventory_item_data
        ], many=True)

        if inventory_item_serializer.is_valid():
            inventory_item_serializer.save()
        else:
            inventory_item.delete()
            raise Exception(inventory_item_serializer.errors)

        return inventory_item


class AssetGroupSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    belongs_to = serializers.SerializerMethodField(read_only=True)
    belongs_to_id = serializers.CharField(write_only=True, required=False)
    total_items = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = AssetGroup
        fields = "__all__"

    def get_belongs_to(self, obj):
        if obj.belongs_to is not None:
            return AssetGroupSerializer(obj.belongs_to).data
        return None


class AssetSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    group = AssetGroupSerializer(read_only=True)
    group_id = serializers.CharField(write_only=True)
    photo = serializers.ImageField(required=False)
    # inventory_item_data = InventoryItemDataSerializer(write_only=True, many=True)

    class Meta:
        model = Asset
        fields = "__all__"

# ======================= CANAL SERIALIZERS ============================
class CanalPlusSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CanalPlus
        fields = "__all__"


class CanalPlusItemSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CanalPlusItem
        fields = "__all__"


class CanalItemAbonnementSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CanalItemAbonnement
        fields = "__all__"


class CanalItemRechargeSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CanalItemRecharge
        fields = "__all__"


class CanalItemReabonnementSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CanalItemReabonnement
        fields = "__all__"


class IncomeOutcomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeOutcome
        fields = "__all__"


class IncomeOutcomeItemSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        item = IncomeOutcomeItem.objects.create(**validated_data)
        item.save()
        return item

    class Meta:
        model = IncomeOutcomeItem
        fields = "__all__"
