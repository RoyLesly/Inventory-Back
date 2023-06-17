from numbers import Number
from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, mixins
from app_control.models import ( Asset, AssetGroup, CanalPlus, CanalPlusItem, InventoryItem, InvoiceItem, 
    MoneyTransaction, MoneyTransactionDetail, MoneyTransactionType, MoneyType, Service, ServiceItem, 
    purchase, CanalItemAbonnement, CanalItemRecharge, CanalItemReabonnement, IncomeOutcome,
    IncomeOutcomeItem, ItemPurchase, ItemSupply, ItemSale, IncomeDb, OutcomeDb,)
from app_control.serializers import (
    AssetGroupSerializer, AssetSerializer, CanalPlusItemSerializer, CanalPlusSerializer, InventoryGroup, InventoryItemSerializer, MoneyTransactionDetailSerializer, MoneyTypeSerializer, PurchaseSerializer, ServiceGroup, InventoryGroupSerializer, ServiceGroupSerializer, InventorySerializer, ServiceItemSerializer, ServiceSerializer, 
    ItemPurchaseSerializer, ItemSupplySerializer, ItemSaleSerializer, ShopSerializer, Shop, Invoice, InvoiceSerializer, 
    InventoryWithSumSerializer, ShopWithAmountSerializer, Inventory, MoneyTransactionSerializer,
    MoneyTransactionTypeSerializer, CanalItemAbonnementSerializer, CanalItemRechargeSerializer, CanalItemReabonnementSerializer, IncomeOutcomeSerializer,
    GetServiceItemSerializer, IncomeOutcomeItemSerializer, InventoryItemWithSumSerializer, 
)
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from inven_djan_api.custom_methods import IsAuthenticatedCustom
from inven_djan_api.utils import CustomPagination, get_query
from django.db.models import Count, Sum, F
from django.db.models.functions import Coalesce, TruncMonth
from user_control.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import csv
import codecs


class InventoryItemView(ModelViewSet):
    queryset = Inventory.objects.select_related("group", "created_by")
    serializer_class = InventorySerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination       # This limits to 100

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        results = self.queryset.filter(**data)

        if keyword:
            search_fields = ("code", "created_by__first_name",
                            "group__name", "name")
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        request.data.update(
            {"created_by_id": request.data["created_by_id"]},
        )
        data_validation = self.serializer_class( data=request.data )
        if data_validation.is_valid():
            data_validation.save()
            return Response({"success": {"Inventory": "Created !!!"} })
        else:
            return Response({"errors": data_validation.errors}) 

    def update(self, request, pk=None, *args, **kwargs):
        instance = Inventory.objects.get(id=request.data["id"])
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = Inventory.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class InventoryGroupView(ModelViewSet):
    queryset = InventoryGroup.objects.select_related(
        "belongs_to", "created_by").prefetch_related("inventories")
    serializer_class = InventoryGroupSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = ("created_by__id", "created_by__first_name"
                             "name", "created_by__email")
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        return results.annotate(
            total_items=Count('inventories')
        )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "ok", "data": serializer.data})
        print(serializer.errors)
        return Response({"errors": serializer.errors})


class InventoryItemPurchaseView(ModelViewSet):
    queryset = ItemPurchase.objects.all()
    serializer_class = ItemPurchaseSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() == "get":
            return self.queryset
        data = self.request.query_params.dict()
        # data.pop("created_by_id", None)
        data.pop("page", None)
        results = self.queryset.filter(**data)
        return results

class InventoryItemSupplyView(ModelViewSet):
    queryset = ItemSupply.objects.all()
    serializer_class = ItemSupplySerializer
    permission_classes = ''#''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("created_by_id", None)
        data.pop("page", None)
        results = self.queryset.filter(**data)
        return results

class InventoryItemSaleView(ModelViewSet):
    queryset = ItemSale.objects.all()
    serializer_class = ItemSaleSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("created_by_id", None)
        data.pop("page", None)
        results = self.queryset.filter(**data)
        return results


class ServiceItemView(ModelViewSet):
    queryset = Service.objects.select_related("group", "created_by")
    serializer_class = ServiceSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD SERVICE ITEM VIEW - line 98")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        results = self.queryset.filter(**data)

        if keyword:
            search_fields = ("code", "created_by__first_name",
                             "group__name", "name")
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD SERVICE ITEM VIEW - line 55")
        user = CustomUser.objects.get(first_name=request.data["user"])
        request.data.update({"created_by_id": user.id},)
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD SERVICE ITEM VIEW - line 65")
        instance = Service.objects.get(id=request.data["id"])
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
            return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = Inventory.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class ServiceView(ModelViewSet):
    queryset = Service.objects.select_related("group", "created_by")
    serializer_class = ServiceSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD SERVICE VIEW - line 99")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = ("code", "created_by__first_name",
                             "group__name", "name",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD SERVICE VIEW - line 114")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "ok", "data": serializer.data})
        print(serializer.errors)
        return Response({"errors": serializer.errors})

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD SERVICE ITEM VIEW - line 60")
        print(request.data)
        instance = Inventory.objects.get(id=request.data["id"])
        # instance = self.get_object()
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = Service.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class ServiceGroupView(ModelViewSet):
    queryset = ServiceGroup.objects.select_related(
        "belongs_to", "created_by").prefetch_related("services")
    serializer_class = ServiceGroupSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = ("created_by__id", "created_by__first_name"
                             "name", "created_by__email")
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        return results.annotate(
            total_items=Count('services')
        )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "ok", "data": serializer.data})
        print(serializer.errors)
        return Response({"errors": serializer.errors})


class NewServiceItemView(ModelViewSet):
    # http_method_names = ('post', 'get')
    queryset = ServiceItemView.queryset
    serializer_class2 = ServiceItemSerializer
    serializer_class = GetServiceItemSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return ServiceItem.objects.all()
        print("IT IS A GET METHOD SERVICE VIEW - line 223")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = ServiceItem.objects.all().filter(**data)

        if keyword:
            search_fields = ("code", "created_by__first_name",
                             "group__name", "name",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request, pk=None, *args, **kwargs):
        print("IT IS A CREATE METHOD NewServiceView - line 224")
        new_service_items =  []
        for i in request.data:
            print("len of i", len(i))
            if len(i) < 4:
                print(request.data[i])
                if request.data[i]["total_amount"] == 0:
                    return Response({"errors": {"Total = 0 Error": "Fill All Fields For Calculation"}})
                new_service_items.append(
                    {
                        "service": request.data[i]["id"],
                        "created_by": request.data["created_by_id"],
                        "quantity": request.data[i]["quantity"],
                        "paid_amount_unit": request.data[i]["paid_amount_unit"],
                        "total_amount": request.data[i]["total_amount"],
                        "issue_to": request.data[i]["issue_to"],
                        "comments_1": request.data[i]["comments_1"],
                        "comments_2": request.data[i]["comments_2"],
                    }
                )
            print("X: -----242---------->")
        
        print("new_service_items LINE 248:", new_service_items)
        if not new_service_items:
            return Response({"errors": {"Empty Items": "Service Items cannot be empty"}})
        
        serializer = self.serializer_class2(
            data=new_service_items, many=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "ok", "data": serializer.data})
        if not serializer.is_valid():
            return Response({"errors": serializer.errors})
        return Response({"errors": "ok", "errors": "Service Items Not Added"})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")


class MoneyItemView(ModelViewSet):
    queryset = MoneyTransaction.objects.select_related("category", "created_by")
    serializer_class = MoneyTransactionSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD MONEY ITEM VIEW - line 167")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        print("1---------------------------")
        if keyword:
            search_fields = ("created_by", "category",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
            print(results)
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD MONEY ITEM VIEW - line 191")
        user = CustomUser.objects.get(first_name=request.data["user"])
        category = MoneyType.objects.get(id=request.data["category"])
        type = MoneyTransactionType.objects.get(id=request.data["type"])
        type2 = MoneyTransactionDetail.objects.get(id=request.data["type2"])
        request.data.update({
            "created_by_id": user.id, 
            "category_id": category.id, 
            "type_id": type.id,
            "type2_id": type2.id
        })
        serializer = self.serializer_class(data = request.data)
        if (type2.name == "DEPOT / CASH IN - MTN" or type2.name == "DEPOT / CASH IN - ORANGE"):
            if (category.available_amount < int(request.data["amount"])):
                raise Exception("NOT ENOUGH FUNDS")
        if serializer.is_valid():
            return super().create(request, *args, **kwargs)
        else:
             print(serializer.errors)
             raise Exception(serializer.errors)

        
        # hostname = socket.gethostname()
        # print("HostNAME", hostname)
        # ip_address2 = socket.gethostbyname(hostname)
        # print(ip_address2)


    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 60")
        print(request.data)
        instance = MoneyTransaction.objects.get(id=request.data["id"])
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class MoneyCategoryView(ModelViewSet):
    queryset = MoneyType.objects.all()
    serializer_class = MoneyTypeSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD MONEY CATEGORY VIEW - line 381")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        if keyword:
            #search_fields = ("created_by", "category",)
            query = get_query(keyword,) # search_fields
            results = results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD MONEY TYPE VIEW - line 268")
        user = CustomUser.objects.get(first_name=request.data["user"])
        print(request.data)
        
        try:
            value = int(MoneyType.objects.all().last().code[6:]) + 1
            last = "GLC-MT00" + str(value).zfill(2)
        except:
            last ="GLC-MT0001"
        request.data.update(
            {
                "code": last,
                "created_by": user.id
            }
        )
        print(request.data)
        request.data.pop("user")

        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 60")
        print(request.data)
        instance = MoneyTransaction.objects.get(id=request.data["id"])
        # instance = self.get_object()
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class MoneyTransactionTypeView(ModelViewSet):
    queryset = MoneyTransactionType.objects.select_related("money_type", "created_by")
    serializer_class = MoneyTransactionTypeSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self,):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD MONEY Transaction Type VIEW - line 337")
        data = self.request.query_params.dict()
        print(data)

        results = self.queryset
        
        print("1---------------------------")
        if data["categoryID"]:
            results = self.queryset.filter(money_type=data["categoryID"])
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD TRANSACTION TYPE VIEW - line 346")
        user = CustomUser.objects.get(first_name=request.data["user"])
        request.data.update(
            {"created_by_id": user.id},
        )
        try:
            trans = MoneyTransactionType.objects.filter(money_type=request.data["id"])
            return trans
        except:
            pass

        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 355")
        print(request.data)
        instance = MoneyTransaction.objects.get(id=request.data["id"])
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class MoneyTransactionDetailView(ModelViewSet):
    queryset = MoneyTransactionDetail.objects.select_related("created_by")
    serializer_class = MoneyTransactionDetailSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self,):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD MONEY Transaction Detail GET VIEW - line 409")
        data = self.request.query_params.dict()
        print(data)
        results = self.queryset
        if data["typeID"]:
            results = self.queryset.filter(type=data["typeID"])
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD TRANSACTION DETAIL CREATE VIEW - line 346")
        user = CustomUser.objects.get(first_name=request.data["user"])
        request.data.update(
            {"created_by_id": user.id},
        )
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 355")
        print(request.data)
        instance = MoneyTransaction.objects.get(id=request.data["id"])
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class AssetGroupView(ModelViewSet):
    queryset = AssetGroup.objects.select_related(
        "belongs_to", "created_by").prefetch_related("assets")
    serializer_class = AssetGroupSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = ("created_by__first_name",
                             "name", "created_by__email")
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        return results.annotate(
            total_items=Count('assets')
        )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "ok", "data": serializer.data})
        return Response({"errors": serializer.errors})


class AssetItemView(ModelViewSet):
    queryset = Asset.objects.select_related("group", "created_by")
    serializer_class = AssetSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD MONEY ITEM VIEW - line 500")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        print("1---------------------------")
        if keyword:
            search_fields = ("created_by", "group",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
            print(results)
        print("2---------------------------")
        print(results)
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD ASSET ITEM VIEW - line 637")
        user = CustomUser.objects.get(first_name=request.data["user"])
        request.data.update(
            {"created_by_id": user.id,},
        )
        print(request.data)
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return super().create(request, *args, **kwargs)
        else:
            print(serializer.errors)
            raise Exception(serializer.errors)

        

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 60")
        print(request.data)
        instance = Asset.objects.get(id=request.data["id"])
        # instance = self.get_object()
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class ShopView(ModelViewSet):
    queryset = Shop.objects.select_related("created_by")
    serializer_class = ShopSerializer
    # permission_classes = ''#(IsAuthenticatedCustom, )
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = ("created_by__first_name",
                             "name", "created_by__email")
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        return results

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.data["created_by_id"]})
        data_validation = self.serializer_class( data=request.data )
        if data_validation.is_valid():
            super().create(request, *args, **kwargs)
            return Response({"success": {"Shop": "Created !!!"} })
        else:
            return Response({"errors": data_validation.errors }) 

    def update(self, request, pk=None, *args, **kwargs):
        instance = Shop.objects.get(id=request.data["id"])
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def delete(self, request, pk=None, *args, **kwargs):
        instance = Shop.objects.get(id=request.data["id"])

        try:
            Shop.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class PurchaseView(ModelViewSet):
    http_method_names = ('post',)
    queryset = InventoryItemView.queryset
    serializer_class2 = InventoryItemSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination


    def create(self, request, pk=None, *args, **kwargs):
        inventory_items =  []
        for i in request.data:
            if i.isnumeric():
                inventory_items.append(
                    {
                        "inventory": request.data[i]["id"],
                        "created_by": CustomUser.objects.get(id=request.data["created_by_id"]).id,
                        "purpose": request.data[i]["purpose"],
                        "quantity": int(request.data[i]["qty"]),
                        "cost_price_unit": int(request.data[i]["amount"]),
                        "cost_price_total": request.data[i]["total"],
                        "recieved_by": CustomUser.objects.get(id=request.data["created_by_id"]).id,
                        "recieved_from": "Market",
                        "reorder_level": 1,
                    }
                )
        
        if not inventory_items:
            raise Exception("Inventory Items cannot be empty")
        
        data_validation = self.serializer_class2( data=inventory_items, many=True )
        
        if data_validation.is_valid():
            data_validation.save()
            return Response({"success": {"Inventory Purchase": "Added To Stock !!!"} })
        else:
            return Response({"errors": {"Errors": data_validation.errors} })  

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")


class InvoiceView(ModelViewSet):
    queryset = Invoice.objects.select_related( "created_by", "shop").prefetch_related("invoice_items")
    serializer_class = InvoiceSerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        print("invoice view -- NOT GET METHOD")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        results = self.queryset.filter(**data)

        if keyword:
            search_fields = ("created_by__first_name",
                             "shop__name", "created_by__email")
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        data_validation = self.serializer_class( data=request.data )
        if data_validation.is_valid():
            super().create(request, *args, **kwargs)
            return Response({"success": {"Invoice": "Created !!!"} })
        else:
            return Response({"errors": data_validation.errors}) 


class SupplyView(ModelViewSet):
    http_method_names = ('post',)
    queryset = InventoryItemView.queryset
    serializer_class2 = InventoryItemSerializer
    serializer_class = InventorySerializer
    permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination


    def create(self, request, pk=None, *args, **kwargs):
        inventory_items =  []      
        for i in request.data:
            if i.isnumeric():
                inventory_items.append(
                    {
                        "inventory": request.data[i]["id"],
                        "created_by": CustomUser.objects.get(id=request.data["created_by_id"]).id,
                        "purpose": request.data[i]["purpose"],
                        "quantity": int(request.data[i]["qty"]),
                        "selling_price_unit": int(request.data[i]["selling_price_unit"]),
                        "selling_price_bulk": request.data[i]["selling_price_bulk"],
                        "supply_by": CustomUser.objects.get(id=request.data["created_by_id"]).first_name,
                        "supply_to": "Shop",
                        "reorder_level": 1,
                    }
                )
        
        if not inventory_items:
            return Response(
                {"errors": {"Empty": "Inventory Items cannot be empty !!!"} }
            )
        
        data_validation = self.serializer_class2( data=inventory_items, many=True )
        if data_validation.is_valid():
            data_validation.save()
            return Response({"success": {"Inventory Supply": "Added To Shop !!!"} })
        else:
            return Response({"errors": data_validation.errors})            


    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")


class SummaryView(ModelViewSet):
    http_method_names = ('get', )
    permission_classes = ''#(IsAuthenticatedCustom, )
    queryset = InventoryItemView.queryset

    def list(self, request, *args, **kwargs):
        total_inventoryItem = self.queryset.filter(
            available_shop__gt=0).count()
        total_inventoryItem_os = self.queryset.filter(
            available_shop__lt=1).count()
        total_group = InventoryGroupView.queryset.count()
        total_shop = ShopView.queryset.count()
        total_users = CustomUser.objects.filter(is_superuser=False).count()

        return Response({
            "total_inventory": total_inventoryItem,
            "total_group": total_group,
            "total_shop": total_shop,
            "total_users": total_users,
            "total_inventory_os": total_inventoryItem_os,
        })


class SalePerformanceView(ModelViewSet):
    http_method_names = ('get', )
    permission_classes = ''#(IsAuthenticatedCustom, )
    queryset = InventoryItem.objects.all().filter(purpose="Sale")
    # queryset = InventoryItemView.queryset

    def list(self, request, *args, **kwargs):
        data = request.query_params.dict()
        total = data.get('total', None)
        query = self.queryset

        def first_day(x):
            date = datetime(int(x[0:4]), int(x[5:7]), int(x[8:10]) - 1).date()
            first_day_of_next_month = (date.replace(day=1) + timedelta(days=32)).replace(day=1)
            return first_day_of_next_month
        try:
            start = data['0']
            end = data['1']
        except:
            raise Exception("No Date or Invalid Date Sent")
        def validate(date_string):
            try: 
                n = datetime.strptime(date_string, '%Y-%m-%d')
                return date_string
            except ValueError:
                return first_day(date_string)
        end = validate(end)

        if not total:
            if start:
                # query = query.filter(
                #     inventory_items__create_at__range=[start_date, end_date]
                # )
                print("XXXXXXXXXXXXXXXXXX MY NAME XXXXXXXXXXXXXXXXXXXXXXXXX")
                query = query.filter(
                    created_at__gte=start, created_at__lte=end
                    # inventory_items__created_at__gte=start, inventory_items__created_at__lte=end
                )
                print(query, "QUERY 1024 -----------------------------")

        items = query.annotate(
            sum_of_item=Coalesce(
                Sum("quantity"), 0
            ),
        ).order_by("-sum_of_item")[0:12]

        response_data = InventoryItemWithSumSerializer(items, many=True).data

        return Response(response_data)


class SaleByShopView(ModelViewSet):
    http_method_names = ('get', )
    permission_classes = ''#(IsAuthenticatedCustom, )
    queryset = InventoryItemView.queryset

    def list(self, request, *args, **kwargs):
        query_data = request.query_params.dict()
        total = query_data.get('total', None)
        monthly = query_data.get('monthly', None)
        query = ShopView.queryset

        if not total:
            start_date = query_data.get("start_date", None)
            end_date = query_data.get("end_date", None)

            if start_date:
                query = query.filter(
                    sale_shop__create_at__range=[start_date, end_date]
                )
        if monthly:
            shops = query.annotate(month=TruncMonth('created_at')).values(
                'months', 'name').annotate(amount_total=Sum(
                    F("sale_shop__invoice_items__quantity") *
                    F("sale_shop__invoice_items__amount")
                ))
        else:
            shops = query.annotate(amount_total=Sum(
                F("sale_shop__invoice_items__quantity") *
                F("sale_shop__invoice_items__amount")
            )).order_by("-amount_total")
        response_data = ShopWithAmountSerializer(shops, many=True).data
        print("saleby shop ==========================================")
        print(response_data)
        return Response(response_data)


class InventoryCSVLoaderView(ModelViewSet):
    http_method_names = ('post',)
    permission_classes = ''#(IsAuthenticatedCustom, )
    serializer_class = InventorySerializer
    queryset = InventoryItemView.queryset

    def create(self, request, *args, **kwargs):
        try:
            data = request.FILES['data']
        except:
            raise Exception("You Need to provide Inventory CSV 'data")
        print(data)

        inventory_items = []
        try:
            print("here")
            csv_reader = csv.reader(codecs.iterdecode(data, 'utf-8'))
            for row in csv_reader:
                print(row, "ROWS===================")
                if (len(row[0]) > 3):
                    continue
                inventory_items.append(
                    {
                        "group_id": row[0],
                        "name": row[1],
                        "description": row[2],
                        "total": row[3],
                        "available_stock": row[3],
                        "cost_price_unit": row[4],
                        "created_by_id": CustomUser.objects.get(first_name=request.data["user"]).id
                    }
                )
            print(inventory_items)
        except csv.Error as e:
            print("CSV ERROR")
            raise Exception(e)

        if not inventory_items:
            raise Exception("CSV file cannot be empty")

        data_validation = self.serializer_class(
            data=inventory_items, many=True)
        if data_validation.is_valid():
            for row in csv_reader:
                print(row, "ROWS===================")
                if (len(row[0]) > 3):
                    continue
                purchase(
                    purchaser=CustomUser.objects.get(first_name=request.data["user"]),
                    inventory=Inventory.objects.get(name=str(row[1])),
                    quantity_unit=row[3],
                    quantity_bulk=0,
                    cost_price_unit=row[4],
                    cost_price_bulk=0,
                    cost_price_total= int(row[3]) * int(row[4]),
                )
            data_validation.save()
            print("SAVED")


        else:
            # print("Not Valid xxxxxxxxxxxxxxx", data_validation.errors)
            print("LINE 1109 Not Valid xxxxxxxxxxxxx")
            raise Exception("Data Errors, Items May Exist Already !!!")

        return Response(
            {"success": "Inventory Items Added Successfully !!!"}
        )


class UploadView(ModelViewSet):
    queryset = Inventory.objects.order_by('-created_at')
    serializer_class = InventorySerializer
    # permission_classes = ''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = ("created_by__first_name",
                             "shop__name", "created_by__email")
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        return results

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)


class CanalPlusView(ModelViewSet):
    queryset = CanalPlus.objects.all()
    serializer_class = CanalPlusSerializer
    permission_classes = ''#''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD Canal ITEM VIEW - line 1152")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        print("1---------------------------")
        if keyword:
            search_fields = ("created_by", "purpose",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
            print(results)
        print("2---------------------------")
        print(results)
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD CANAL ITEM VIEW - line 1171")
        user = CustomUser.objects.get(first_name=request.data["user"])
        request.data.update(
            {"created_by_id": user.id,},
        )
        serializer = self.serializer_class(data = request.data)
        print(request.data)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return super().create(request, *args, **kwargs)
        else:
            print(serializer.errors)
            raise Exception(serializer.errors)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 60")
        print(request.data)
        instance = Asset.objects.get(id=request.data["id"])
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class CanalItemView(ModelViewSet):
    queryset = CanalPlusItem.objects.all()
    serializer_class = CanalPlusItemSerializer
    permission_classes = ''#''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        if keyword:
            search_fields = ("created_by", "purpose",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
            print(results)
        return results

    def create(self, request, *args, **kwargs):
        print(request.data)
        userId = CustomUser.objects.get(id=request.data["created_by_id"]).id
        request.data.update( {"created_by_id": userId,}, )
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            return super().create(request, *args, **kwargs)
        else:
            print(serializer.errors)
            raise Exception(serializer.errors)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 60")
        print(request.data)
        instance = Asset.objects.get(id=request.data["id"])
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class GetCanalAbonnementView(ModelViewSet):
    queryset = CanalItemAbonnement.objects.all()
    serializer_class = CanalItemAbonnementSerializer
    permission_classes = ''#''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        data.pop("created_by_id", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        if keyword:
            search_fields = ("created_by", "purpose",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD CANAL ITEM VIEW - line 1242")
        user = CustomUser.objects.get(first_name=request.data["user"])
        print("LINE 1244 ------------------->",request.data)
        request.data.update( {"created_by_id": user.id,}, )
        serializer = self.serializer_class(data = request.data)
        print(request.data)
        if serializer.is_valid():
            print(request.data)
            return super().create(request, *args, **kwargs)
        else:
            print(serializer.errors)
            raise Exception(serializer.errors)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 60")
        print(request.data)
        instance = Asset.objects.get(id=request.data["id"])
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class GetCanalRechargeView(ModelViewSet):
    queryset = CanalItemRecharge.objects.all()
    serializer_class = CanalItemRechargeSerializer
    permission_classes = ''#''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        data.pop("created_by_id", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        print("1---------------------------")
        if keyword:
            search_fields = ("created_by", "purpose",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        user = CustomUser.objects.get(first_name=request.data["user"])
        request.data.update( {"created_by_id": user.id,}, )
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            print(request.data)
            return super().create(request, *args, **kwargs)
        else:
            print(serializer.errors)
            raise Exception(serializer.errors)

    def update(self, request, pk=None, *args, **kwargs):
        instance = Asset.objects.get(id=request.data["id"])
        serializer = self.serializer_class(
            instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})


    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class GetCanalReabonnementView(ModelViewSet):
    queryset = CanalItemReabonnement.objects.all()
    serializer_class = CanalItemReabonnementSerializer
    permission_classes = ''#''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("created_by_id", None)
        data.pop("page", None)
        keyword = data.pop("keyword", None)
        results = self.queryset.filter(**data)
        if keyword:
            print(keyword)
            search_fields = ("amount", "phone", "purpose",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        user = CustomUser.objects.get(first_name=request.data["user"])
        request.data.update( {"created_by_id": user.id,}, )
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            print(request.data)
            return super().create(request, *args, **kwargs)
        else:
            print(serializer.errors)
            raise Exception(serializer.errors)

    def update(self, request, pk=None, *args, **kwargs):
        instance = Asset.objects.get(id=request.data["id"])
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class GetIncomeOutcomeView(ModelViewSet):
    queryset = IncomeOutcome.objects.all()
    serializer_class = IncomeOutcomeSerializer
    permission_classes = ''#''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD INC-OUT ITEM VIEW - line 1365")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        if keyword:
            search_fields = ("created_by", "purpose",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD INC-OUT ITEM VIEW - line 1518")
        user = CustomUser.objects.get(first_name=request.data["user"])
        print("LINE 1244 ------------------->",request.data)
        request.data.update( {"created_by_id": user.id,}, )
        serializer = self.serializer_class(data = request.data)
        print(request.data)
        if serializer.is_valid():
            print(request.data)
            return super().create(request, *args, **kwargs)
        else:
            print(serializer.errors)
            raise Exception(serializer.errors)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 60")
        print(request.data)
        instance = IncomeOutcome.objects.get(id=request.data["id"])
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class GetIncomeOutcomeDetailView(ModelViewSet):
    queryset = IncomeOutcomeItem.objects.all()
    serializer_class = IncomeOutcomeItemSerializer
    permission_classes = ''#''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        if keyword:
            search_fields = ("created_by", "purpose",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        print("results ----------", results)
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD INC-OUT ITEM VIEW - line 1518")
        user = CustomUser.objects.get(first_name=request.data["user"])
        print("LINE 1244 ------------------->",request.data)
        request.data.update( {"created_by_id": user.id,}, )
        serializer = self.serializer_class(data = request.data)
        print(request.data)
        if serializer.is_valid():
            print(request.data)
            return super().create(request, *args, **kwargs)
        else:
            print(serializer.errors)
            raise Exception(serializer.errors)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 60")
        print(request.data)
        instance = IncomeOutcome.objects.get(id=request.data["id"])
        print(instance)
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        # print(serializer)
        if serializer.is_valid():
            print("Is VALID")
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            print(serializer.errors)
        return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = MoneyTransaction.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class GetIncomeOutcomeItemView(ModelViewSet):
    queryset = IncomeOutcomeItem.objects.all()
    serializer_class = IncomeOutcomeItemSerializer
    permission_classes = ''#''#(IsAuthenticatedCustom, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset
        print("IT IS A GET METHOD INC-OUT ITEM VIEW - line 1365")
        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)
        if keyword:
            search_fields = ("created_by", "purpose",)
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        print("IT IS A CREATE METHOD INC-OUT ITEM VIEW - line 1518")
        user = CustomUser.objects.get(first_name=request.data["user"])
        print("LINE 1588 ------------------->",request.data)
        request.data.pop("user")
        request.data.update( {"created_by": user.id,}, )
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            return super().create(request, *args, **kwargs)
        else:
            raise Exception(serializer.errors)

    def update(self, request, pk=None, *args, **kwargs):
        print("IT IS A UPDATE METHOD MONEY ITEM VIEW - line 60")
        instance = IncomeOutcome.objects.get(id=request.data["id"])
        serializer = self.serializer_class(
            instance=instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Updated", "data": serializer.data})
        else:
            raise Exception(serializer.errors)
        # return Response({"status": "Error", "data": request.data})

    def patial_update(self, request, pk=None, * args, **kwargs):
        print("PARTIAL UPDATE")

    def delete(self, request, pk=None, *args, **kwargs):
        instance = IncomeOutcomeItem.objects.get(id=request.data["id"])

        try:
            instance.delete()
            return Response({"status": "Deleted", "data": request.data})
        except:
            print("Error")
            return Response({"status": "Error", "data": request.data})


class MegaSummaryOneView(ModelViewSet):
    http_method_names = ('get', )
    permission_classes = ''#(IsAuthenticatedCustom, )
    queryset_invoice_item = InvoiceItem.objects.all()
    queryset_service_item = ServiceItem.objects.all()
    queryset_inventory_item = InventoryItem.objects.all()
    queryset_income_outcome_item = IncomeOutcome.objects.all()
    queryset_income_item = IncomeDb.objects.all()
    queryset_outcome_item = OutcomeDb.objects.all()
    queryset_canal_reabo_item = CanalItemReabonnement.objects.all()
    queryset_canal_abonn_item = CanalItemAbonnement.objects.all()
    queryset_canal_recha_item = CanalItemRecharge.objects.all()
    queryset_money_transaction = MoneyTransaction.objects.all()


    def list(self, request, *args, **kwargs):
        if self.request.method.lower() != "get":
            raise Exception("Method Not Allow - ONLY GET METHOD ALLOWED")
        data = self.request.query_params.dict()
        # print("data=====> :  ", data)
        def first_day(x):
            date = datetime(int(x[0:4]), int(x[5:7]), int(x[8:10]) - 1).date()
            first_day_of_next_month = (date.replace(day=1) + timedelta(days=32)).replace(day=1)
            return first_day_of_next_month
        try:
            start = data['0']
            end = data['1']
        except:
            raise Exception("No Date or Invalid Date Sent")
        def validate(date_string):
            try: 
                n = datetime.strptime(date_string, '%Y-%m-%d')
                return date_string
            except ValueError:
                return first_day(date_string)
        end = validate(end)
        
        try:
            other = data['2']
        except:
            other = ""

        print("QUERIES ======xxxxxxxxxxxx")
        # print(start, " ", end)
        invoice_items = self.queryset_invoice_item.filter(
             created_at__gte=start, created_at__lt=end)
        service_items = self.queryset_service_item.filter(
             created_at__gte=start, created_at__lt=end)
        inventory_items = self.queryset_inventory_item.filter(
             created_at__gte=start, created_at__lt=end)
        income_items = self.queryset_income_item.filter(
             created_at__gte=start, created_at__lt=end)
        outcome_items = self.queryset_outcome_item.filter(
             created_at__gte=start, created_at__lt=end)
        canal_abonn_items = self.queryset_canal_abonn_item.filter(
             created_at__gte=start, created_at__lt=end)
        canal_reabo_items = self.queryset_canal_reabo_item.filter(
             created_at__gte=start, created_at__lt=end)
        canal_recha_items = self.queryset_canal_recha_item.filter(
             created_at__gte=start, created_at__lt=end)
        print("RESULTS HERE")
        total_invoice_amt = 0
        total_service_amt = 0
        total_purchase = 0
        total_sale = 0
        total_income = 0
        total_outcome = 0
        total_canal_reabo = 0
        total_canal_abonn = 0
        total_canal_recha = 0
        if invoice_items:
            for item in invoice_items:
                total_invoice_amt += item.total
        if service_items:
            for item in service_items:
                total_service_amt += item.total_amount

        if inventory_items:
            for item in inventory_items:
                if (item.purpose == "Purchase"):
                    total_purchase += item.cost_price_total
                elif (item.purpose == "Sale"):
                    total_sale += item.sold_price_total
        if income_items:
            for item in income_items:
                total_income += item.total_amount
        if outcome_items:
            for item in outcome_items:
                total_outcome += item.total_amount
        if canal_abonn_items:
            for item in canal_abonn_items:
                total_canal_abonn += item.amount
        if canal_reabo_items:
            for item in canal_reabo_items:
                total_canal_reabo += item.amount
        if canal_recha_items:
            for item in canal_recha_items:
                total_canal_recha += item.amount
        else:
            pass
        print(total_sale)
        response = {
            "total_invoice_amount": total_invoice_amt,
            "total_service_amount": total_service_amt,
            "total_purchase_amount": (total_purchase),
            "total_sale_amount": (total_sale),
            "total_income_amount": (total_income),
            "total_outcome_amount": (total_outcome),
            "total_canal_abonn_amount": (total_canal_abonn),
            "total_canal_reabo_amount": (total_canal_reabo),
            "total_canal_recha_amount": (total_canal_recha),

            "total_service_count": service_items.count(),
            "total_purchase_count": (total_purchase),
            "total_invoice_items_count": (invoice_items.count()),
            "total_invoice_count": invoice_items.count(),
            "total_income_count": income_items.count(),
            "total_outcome_count": outcome_items.count(),
            "total_service_items_count": (service_items.count()),
            "total_inventory_items_count": (inventory_items.count()),
            "total_canal_abonn_count": (canal_abonn_items.count()),
            "total_canal_reabo_count": (canal_reabo_items.count()),
            "total_canal_recha_count": (canal_recha_items.count()),
        }
        # print(response)

        return Response(response)


class MegaSummaryTwoView(ModelViewSet):
    http_method_names = ('get', )
    permission_classes = ''#(IsAuthenticatedCustom, )
    queryset_inventory_item = InventoryItem.objects.all()
    queryset_service_item = ServiceItem.objects.all()
    queryset_money_transaction = MoneyTransaction.objects.all()


    def list(self, request, *args, **kwargs):
        if self.request.method.lower() != "get":
            raise Exception("Method Not Allow - ONLY GET METHOD ALLOWED")
        data = self.request.query_params.dict()
        # print("PARAM: ===>  1726 ", data)
        try:
            start = data['0']
            end = data['1']
        except:
            raise Exception("No Date or Invalid Date Sent")
        try:
            other = data['2']
        except:
            other = ""

        test = self.queryset_inventory_item.filter(
             created_at__gte=start, created_at__lte=end).count()
        # total_inventoryItem_os = self.queryset.filter(
        #     available_shop__lt=1).count()
        # total_group = InventoryGroupView.queryset.count()
        # total_shop = ShopView.queryset.count()
        # total_users = CustomUser.objects.filter(is_superuser=False).count()

        return Response({
            "test": 1,
            # "total_inventory": total_inventoryItem,
            # "total_group": total_group,
            # "total_shop": total_shop,
            # "total_users": total_users,
            # "total_inventory_os": total_inventoryItem_os,
        })