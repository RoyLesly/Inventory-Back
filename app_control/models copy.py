from ast import arg
import code
from datetime import datetime, timezone
from distutils.command.upload import upload
from enum import unique
from random import choices
from unittest.util import _MAX_LENGTH
from urllib import request
from django.db import models
from user_control.models import CustomUser
from user_control.views import add_user_activity
from django.db.models.signals import post_save


def purchase(purchaser, inventory, quantity_unit, quantity_bulk, cost_price_unit, cost_price_bulk, cost_price_total):
    ItemPurchase.objects.create(
        purchaser=purchaser.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        cost_price_unit=cost_price_unit,
        cost_price_bulk=cost_price_bulk,
        cost_price_total=cost_price_total,
    )


def supply(supplier, inventory, quantity_unit, quantity_bulk, selling_price_unit, selling_price_bulk):
    ItemSupply.objects.create(
        supplier=supplier.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        selling_price_unit=selling_price_unit,
        selling_price_bulk=selling_price_bulk,
    )


def sale(seller, inventory, quantity_unit, quantity_bulk, sold_price_unit, sold_price_bulk, sold_price_total):
    ItemSale.objects.create(
        seller=seller.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        sold_price_unit=sold_price_unit,
        sold_price_bulk=sold_price_bulk,
        sold_price_total=sold_price_total,
    )


def recharge(recharger, canal_plus, quantity, amount, total_amount):
    ItemCanalRecharge.objects.create(
        recharger=recharger.first_name,
        canal_plus=canal_plus.name,
        quantity=quantity,
        amount=amount,
        total=total_amount,
    )


def abonnement(subscriber, canal_plus, quantity, amount, total_amount):
    ItemCanalRecharge.objects.create(
        subscriber=subscriber.first_name,
        canal_plus=canal_plus.name,
        quantity=quantity,
        amount=amount,
        total=total_amount,
    )


def reabonnement(resubscriber, canal_plus, quantity, amount, total_amount):
    ItemCanalRecharge.objects.create(
        resubscriber=resubscriber.first_name,
        canal_plus=canal_plus.name,
        quantity=quantity,
        amount=amount,
        total=total_amount,
    )


class InventoryGroup(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name='inventory_groups', on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=60, unique=True)
    belongs_to = models.ForeignKey(
        'self', null=True, on_delete=models.SET_NULL, related_name='group_relations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.name

    def save(self, *args, **kwargs):
        action = f"added new group - '{self.name}'"
        if self.pk is not None:
            action = f"updated group from - '{self.old_name}' to '{self.name}'"

        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted group - '{self.name}'"

        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Inventory(models.Model):
    ACTIVE_STATUS = (("Active", "Active"), ("In-Active", "In-Active"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='inventory_creator', on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, unique=True, null=True, blank=False)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    group = models.ForeignKey(InventoryGroup, related_name='inventories', null=True, on_delete=models.SET_NULL)

    reorder_level = models.IntegerField(default='2', blank=True, null=True)
    cost_price_unit = models.FloatField(default=0, blank=True)
    cost_price_bulk = models.FloatField(default=0, blank=True, null=True)
    selling_price_unit = models.FloatField(default=0, blank=True)
    selling_price_bulk = models.FloatField(default=0, blank=True)
    total = models.PositiveIntegerField(blank=True, default=0, null=True)
    available_stock = models.PositiveIntegerField(null=True, default=0, blank=True)
    available_shop = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_quantity_sold = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_amount_sold = models.PositiveIntegerField(null=True, default=0, blank=True)

    active = models.CharField(default="Active", max_length=9, choices=ACTIVE_STATUS)
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        print(is_new)

        if is_new:
            super().save(*args, **kwargs)
            print("HERE")

            id_length = len(str(self.id))
            code_length = 5 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC{zeros}{self.id}"
            print(self.code)
            self.save()

        else:
            if str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("False Not same Update 130 Models")
                action = f"updated inventory with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("True same update 134 Model")
                action = f"added new inventory Item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.created_at)[:18] == str(datetime.now(timezone.utc))[:18]:
                print("True same 139 Model")
                action = f"added new inventory Item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted Inventory item - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.name} - {self.code}"


def update_inventory(sender, **kwargs):
    print(kwargs)
    created_item = kwargs['instance']
    if kwargs['created']:
        inven = Inventory.objects.get(inventory_items=created_item)
        if (created_item.purpose == "Purchase"):
            print("Purchase Action -  line 166")
            inven.total += created_item.quantity
            inven.available_stock += created_item.quantity
            if inven.reorder_level != "" or inven.reorder_level != 0:
                inven.reorder_level = created_item.reorder_level
            if inven.cost_price_unit != 0 or inven.cost_price_unit != "" or inven.cost_price_unit != None:
                inven.cost_price_unit = created_item.cost_price_unit
            if (inven.cost_price_bulk != 0 or inven.cost_price_bulk != "" or inven.cost_price_bulk != None):
                inven.cost_price_bulk = created_item.cost_price_bulk            
            inven.save()

        elif (kwargs['instance'].purpose == "Supply"):
            print("Supply Action")
            inven.available_shop += created_item.quantity
            inven.available_stock -= created_item.quantity
            if inven.reorder_level != "" or inven.reorder_level != 0:
                inven.reorder_level = created_item.reorder_level
            if inven.selling_price_unit != 0 or inven.selling_price_unit != "" or inven.selling_price_unit != None:
                inven.selling_price_unit = created_item.selling_price_unit
            if  inven.selling_price_bulk != 0 or inven.selling_price_bulk != "" or inven.selling_price_bulk != None:
                inven.selling_price_bulk = created_item.selling_price_bulk
            if inven.available_shop <= 0:
                inven.active = "In-Active"
            inven.save()
        
        elif (kwargs['instance'].purpose == "Sale"):
            print("Sale Action")
            print(inven.available_shop)
            inven.available_shop -= created_item.quantity
            inven.total_quantity_sold += created_item.quantity
            inven.total_amount_sold += created_item.quantity * created_item.sold_price_unit
            print(inven.available_shop)
            print(inven.reorder_level)
            if inven.available_shop < inven.reorder_level:
                print("Update Active status = 0 193 models")
                inven.active = "In-Active"
            inven.save()
        

PURPOSE = (('Purchase', 'Purchase'), ('Supply', 'Supply'), ('Sale', 'Sale'))
class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, related_name='inventory_items', on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='inventory_items_creator', on_delete=models.SET_NULL)
    purpose = models.CharField(max_length=15, blank=False, choices=PURPOSE)

    quantity = models.IntegerField(default='0', blank=False, null=False)
    reorder_level = models.IntegerField(default='1', blank=True, null=True)

    cost_price_unit = models.FloatField(default=0, blank=True)
    cost_price_bulk = models.FloatField(default=0, blank=True, null=True)
    cost_price_total = models.FloatField(default=0, blank=True)
    selling_price_unit = models.FloatField(default=0, blank=True)
    selling_price_bulk = models.FloatField(default=0, blank=True, null=True)
    sold_price_unit = models.FloatField(default=0, blank=True)
    sold_price_bulk = models.FloatField(default=0, blank=True, null=True)
    sold_price_total = models.FloatField(default=0, blank=True)

    supply_by = models.CharField(max_length=50, blank=True, null=True)
    supply_to = models.CharField(max_length=50, default="", blank=True, null=True)

    recieved_by = models.CharField(max_length=50, blank=True, null=True)
    recieved_from = models.CharField(max_length=50, default="", blank=True, null=True)

    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, default="", blank=True, null=True)
    
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            try:
                super().save(args, kwargs)
                print("Level 277 model OK")
                id_length = len(str(self.id))
                code_length = 6 - id_length
                zeros = "".join("0" for i in range(code_length))
                self.code = f"GLC{zeros}{self.id}"
                self.save()
                print("Level 283 model OK Models -- SAVED")
                if self.sold_price_total == "" or self.sold_price_total == 0:
                    self.sold_price_total = self.sold_price_unit * self.quantity
                
                if self.purpose == "Purchase":
                    if (self.cost_price_total != 0 or self.cost_price_total != None):
                        total_amount_purchase = self.cost_price_total
                    else:
                        total_amount_purchase = self.quantity * self.cost_price_unit
                    purchase(self.created_by, self.inventory, self.quantity,
                        self.quantity, self.cost_price_unit, self.cost_price_bulk,
                        total_amount_purchase
                    )
                    print("SALE Line 296: CREATED ---------------------------",)
                
                if self.purpose == "Supply":
                    supply(self.created_by, self.inventory, self.quantity,
                        self.quantity, self.selling_price_unit, self.selling_price_bulk,
                    )
                    print("SUPPLY Line 302 : CREATED ---------------------------",)

                if self.purpose == "Sale":
                    print("SALE ACTION")
                    total_amount_sold = self.quantity * self.sold_price_unit
                    sale(self.created_by, self.inventory, self.quantity,
                        self.quantity, self.sold_price_unit, self.sold_price_unit,
                        total_amount_sold
                    )
                    print("SALE Line 311: CREATED ---------------------------",)
            except:
                print("Level 285 model ERROR")

        else:
            print("Level 3")
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("Inventory Update Action")
                action = f"updated inventory item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("Inventory Create Action")
                action = f"added new inventory item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
                        
            self.cost_price_total = self.quantity * self.cost_price_unit 
            super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        created_by = self.created_by
        # action = f"deleted Inventory item - '{self.inventory.name}'"
        action = "deleted Inventory item" + "self.inventory.name"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        # return f"{self.inventory.name} - {self.code}"
        return f"{self.inventory.name} - {self.inventory.code}"


def update_inventory_item(sender, **kwargs):
    print("INVOICE CALLED UPDATED INVEN ITEM")
    created_item = kwargs['instance']
    print("344:--------", created_item)
    if kwargs['created']:
        print("kwargs : ", kwargs)
        print("created_item.item : ", created_item.item)
        print("created_item.invoice.created_by : ", created_item.invoice.created_by)
        print("created_item.quantity : ", created_item.quantity)
        print("created_item.amount : ", created_item.amount)
        print("created_item.amount/created_item.quantity : ", created_item.amount/created_item.quantity)
        # print("created_item : ", kwargs)
        
        test = InventoryItem.objects.create(
                created_by = created_item.invoice.created_by,
                inventory = created_item.item,
                purpose = "Sale",
                quantity = created_item.quantity,
                sold_price_unit = created_item.amount/created_item.quantity,
                sold_price_total = created_item.amount,
                issue_by = "Anonym.user",
                issue_to = "Customer",
            )
        test.save()
        

post_save.connect(update_inventory, sender=InventoryItem)


class ItemPurchase(models.Model):
    purchaser = models.CharField(max_length=50, unique=False)
    inventory = models.CharField(max_length=50, unique=False)
    quantity_unit = models.IntegerField(default='0', blank=False, null=False)
    quantity_bulk = models.IntegerField(default='0', blank=False, null=True)
    cost_price_unit = models.FloatField(default=0, blank=True)
    cost_price_bulk = models.FloatField(default=0, blank=True, null=True)
    cost_price_total = models.FloatField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.purchaser} Purchased {self.inventory} on {self.created_at}"


class ItemSupply(models.Model):
    supplier = models.CharField(max_length=50, unique=False)
    inventory = models.CharField(max_length=50, unique=False)
    quantity_unit = models.IntegerField(default='0', blank=False, null=False)
    quantity_bulk = models.IntegerField(default='0', blank=False, null=True)
    selling_price_unit = models.FloatField(default=0, blank=True)
    selling_price_bulk = models.FloatField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.supplier} Supplied {self.inventory} on {self.created_at}"


class ItemSale(models.Model):
    seller = models.CharField(max_length=50, unique=False)
    inventory = models.CharField(max_length=50, unique=False)
    quantity_unit = models.IntegerField(default='0', blank=False, null=False)
    quantity_bulk = models.IntegerField(default='0', blank=False, null=False)
    sold_price_unit = models.FloatField(default=0, blank=True)
    sold_price_bulk = models.FloatField(default=0, blank=True, null=True)
    sold_price_total = models.FloatField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.seller} Sold {self.inventory} on {self.created_at}"


class Shop(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name='shops', on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.name

    def save(self, *args, **kwargs):
        action = f"added new shop - '{self.name}'"
        if self.pk is not None:
            action = f"updated shop from - '{self.old_name}' to '{self.name}'"

        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted shop - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    created_by = models.ForeignKey( CustomUser, null=True, related_name='invoices', on_delete=models.SET_NULL)
    shop = models.ForeignKey( Shop, related_name='sale_shop', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.shop

    def save(self, *args, **kwargs):
        action = "Created new invoice"
        #action = f"{self.created_by} Created new invoice"
        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)
        print("models invoice save function =====LINE 456 MODELS======")

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted invoice - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="invoice_items", on_delete=models.CASCADE)
    item = models.ForeignKey( Inventory, null="s", related_name="inventory_invoices", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=20, null=True)
    item_code = models.CharField(max_length=20, null=True)
    quantity = models.PositiveIntegerField()
    amount = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        if self.item.available_shop < self.quantity:
            raise Exception(f"item with code {self.item.code} is not enough")

        self.item_name = self.item.name
        self.item_code = self.item.code

        self.amount = self.quantity * self.item.selling_price_unit
        self.item.available_shop -= self.quantity
        self.item.total_quantity_sold += self.quantity
        self.item.total_amount_sold += self.amount
        self.item.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} = {self.quantity}"

post_save.connect(update_inventory_item, sender=InvoiceItem)


class ServiceGroup(models.Model):
    created_by = models.ForeignKey(CustomUser, null=True, related_name='service_groups', on_delete=models.SET_NULL)
    name = models.CharField(max_length=60, unique=True)
    belongs_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='group_relations')
    belongs_to_shop = models.ForeignKey(Shop, null=True, blank=True, on_delete=models.SET_NULL, related_name='shop_relations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.name

    def save(self, *args, **kwargs):
        action = f"added new group - '{self.name}'"
        if self.pk is not None:
            action = f"updated group from - '{self.old_name}' to '{self.name}'"

        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted group - '{self.name}'"

        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return self.name


class Service(models.Model):
    ACTIVE_STATUS = (("Active", "Active"), ("In-Active", "In-Active"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='services_creator', on_delete=models.SET_NULL)
    name = models.CharField(max_length=20, unique=True, null=True, blank=False)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    group = models.ForeignKey(ServiceGroup, related_name='services', null=True, on_delete=models.SET_NULL)

    cost_price_unit = models.FloatField(default=0, blank=True)
    cost_price_bulk = models.FloatField(default=0, blank=True, null=True)
    paid_price_unit = models.FloatField(default=0, blank=True)
    paid_price_bulk = models.FloatField(default=0, blank=True)
    total = models.PositiveIntegerField(blank=True, default=0, null=True)
    total_quantity_sold = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_amount_sold = models.PositiveIntegerField(null=True, default=0, blank=True)

    active = models.CharField(default="Active", max_length=9, choices=ACTIVE_STATUS)
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        print(is_new)

        if is_new:
            super().save(*args, **kwargs)
            print("HERE")

            id_length = len(str(self.id))
            code_length = 4 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC{zeros}{self.id}"
            print(self.code)
            self.save()

        else:
            if str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("False Not same Update 130 Models")
                action = f"updated Service with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("True same update 134 Model")
                action = f"added new Service Item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.created_at)[:18] == str(datetime.now(timezone.utc))[:18]:
                print("True same 139 Model")
                action = f"added new Service Item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted Service item - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.name} - {self.code}"


class ServiceItem(models.Model):
    service = models.ForeignKey(Service, related_name='service_items', on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='service_items_creator', on_delete=models.SET_NULL)
    quantity = models.IntegerField(default='0', blank=False, null=False)

    sold_price_unit = models.FloatField(default=0, null=False)
    sold_price_bulk = models.FloatField(default=0, blank=True, null=True)
    sold_price_total = models.FloatField(default=0, blank=True)
    comments = models.CharField(default="", max_length=250, null=True, blank=True)

    issue_to = models.CharField(max_length=50, default="", blank=True, null=True)
    
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)

            id_length = len(str(self.id))
            code_length = 4 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC{zeros}{self.id}"
            self.save()

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("Service Update Action")
                action = f"updated inventory item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("Service Create Action")
                action = f"added new service item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)

                if self.sold_price_total == "" or self.sold_price_total == 0:
                    self.sold_price_total = self.sold_price_unit * self.quantity

                total_amount_sold = self.quantity * self.sold_price_unit
                        
            self.cost_price_total = self.quantity * self.cost_price_unit 
            super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        created_by = self.created_by
        # action = f"deleted Inventory item - '{self.inventory.name}'"
        action = "deleted Service item" + "self.service.name"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.service.name} - {self.service.code}"


class MoneyType(models.Model):
    name = models.CharField(max_length=20, unique=True, null=True, blank=False)
    code = models.CharField(max_length=10, unique=True, null=False, blank=True)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='MT_creator', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)
            print("SAVED MODEL 647")

        else:
            if str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("False Not same Update 130 Models")
                action = f"updated money money_type with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("True same update 134 Model")
                action = f"added new money_type item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.created_at)[:18] == str(datetime.now(timezone.utc))[:18]:
                print("True same 139 Model")
                action = f"added new money_type item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} - {self.code}"


class MoneyTransactionType(models.Model):
    name = models.CharField(max_length=25, unique=True)
    code = models.CharField(max_length=10, unique=False, null=False, blank=True)
    money_type = models.ForeignKey(MoneyType, related_name='money_type', on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='MTT_creator', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        print(is_new)

        if is_new:
            super().save(*args, **kwargs)
            code_length = 4 - len(str(self.id))
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-TT{zeros}{self.id}"
            print(self.code)
            self.save()

        else:
            if str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("False Not same Update 130 Models")
                action = f"updated money transaction_type with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("True same update 134 Model")
                action = f"added new transaction_type item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.created_at)[:18] == str(datetime.now(timezone.utc))[:18]:
                print("True same 139 Model")
                action = f"added new transaction_type item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.code}"


class MoneyTransactionDetail(models.Model):
    name = models.CharField(max_length=25, unique=False)
    detail = models.CharField(max_length=25, unique=False)
    code = models.CharField(max_length=10, unique=False, null=False, blank=True)
    category = models.ForeignKey(MoneyType, default="1", related_name='MTD_category', on_delete=models.SET_DEFAULT)
    type = models.ForeignKey(MoneyTransactionType, default="1", related_name='MTD_type', on_delete=models.SET_DEFAULT)
    created_by = models.ForeignKey(CustomUser, default="1", related_name='MTD_creator', on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)
            code_length = 3 - len(str(self.id))
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-MTD{zeros}{self.id}"
            print(self.code)
            self.save()

        else:
            if str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("False Not same Update 130 Models")
                action = f"updated money transaction_detail with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            
            elif str(self.created_at)[:18] == str(datetime.now(timezone.utc))[:18]:
                print("True same 139 Model")
                action = f"added new transaction_detail with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.code}"


class MoneyTransaction(models.Model):
    TYPE = (("Depot", "Depot"), ("Retrait", "Retrait"), ("Other", "Other"))
    STATE = (("Success", "Success"), ("Failed", "Failed"), ("Pending", "Pending"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='transaction_created_by', on_delete=models.SET_NULL)
    customer_number = models.CharField(max_length=15, unique=False, null=False, blank=False)
    customer_name = models.CharField(max_length=15, unique=False, null=False, blank=False)
    category = models.ForeignKey(MoneyType, default="1", unique=False, related_name='transaction_category', on_delete=models.SET_DEFAULT)
    type = models.ForeignKey(MoneyTransactionType, default="1", unique=False, related_name='transaction_type', on_delete=models.SET_DEFAULT)
    type2 = models.ForeignKey(MoneyTransactionDetail, default="1", unique=False, related_name='transaction_detail', on_delete=models.SET_DEFAULT)
    Amount = models.CharField(max_length=6, null=False, unique=False)
    state = models.CharField(max_length=15, choices=STATE)
    balance = models.CharField(max_length=100, blank=True, null=False)
    comments = models.CharField(max_length=100, blank=True, null=True)

    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_number} - {self.type} - {self.type2}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            print("NEW1")
            super().save(*args, **kwargs)
            print(self.id)
            code_length = 3 - len(str(self.id))
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-MT{zeros}{self.id}"
            print(self.code)
            self.save()

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("Transaction Update Action")
                action = f"updated transaction item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("Transaction Create Action 791")
                print(self.created_by)
                # action = f"added new service item with code - '{self.created_by.first_name}'"
                action = f"added new service item with code - '{self.created_by}'"
                add_user_activity(self.created_by, action=action)
            print("args")
            print(args)
            super().save(*args, **kwargs)


class AssetGroup(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name='asset_groups', on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=60, unique=True)
    belongs_to = models.ForeignKey(
        'self', null=True, on_delete=models.SET_NULL, related_name='group_relations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.name

    def save(self, *args, **kwargs):
        action = f"added new asset group - '{self.name}'"
        if self.pk is not None:
            action = f"updated asset group from - '{self.old_name}' to '{self.name}'"

        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted group - '{self.name}'"

        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return self.name


class Asset(models.Model):
    PHYSICAL_STATE= (("Good", "Good"), ("Bad", "Bad"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='asset_creator', on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, unique=True, null=True, blank=False)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    group = models.ForeignKey(AssetGroup, related_name='assets', null=True, on_delete=models.SET_NULL)

    reorder_level = models.IntegerField(default='2', blank=True, null=True)
    cost_price_unit = models.FloatField(default=0, blank=True)
    number = models.PositiveIntegerField(blank=True, default=0, null=True)
    
    physical_state = models.CharField(default="Active", max_length=9, choices=PHYSICAL_STATE)
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)

            id_length = len(str(self.id))
            code_length = 5 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC{zeros}{self.id}"
            self.save()

        else:
            if str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("False Not same Update 869 Models")
                action = f"updated Asset with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("True same update 874 Model")
                action = f"added new Asset Item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.created_at)[:18] == str(datetime.now(timezone.utc))[:18]:
                print("True same 879 Model")
                action = f"added new Asset Item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted Asset item - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.name} - {self.code}"


class CanalPlus(models.Model):
    STATE = (("Success", "Success"), ("Failed", "Failed"), ("Pending", "Pending"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='canal_created_by', on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, unique=True, null=True, blank=False)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    total = models.PositiveIntegerField(blank=True, default=0, null=True)
    available_balance = models.PositiveIntegerField(blank=True, default=0, null=True)
    total_amount_sold = models.PositiveIntegerField(null=True, default=0, blank=True)

    reorder_level = models.IntegerField(default='20000', blank=True, null=True)
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.total} - {self.available_balance}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            print("NEW Line 919")
            super().save(*args, **kwargs)
            code_length = 3 - len(str(self.id))
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-CP{zeros}{self.id}"
            self.save()

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("Canal Plus Update Action 958")
                action = f"updated canal Plus item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("Canal Plus Create Action 969")
                action = f"added new canal plus with code - '{self.created_by}'"
                add_user_activity(self.created_by, action=action)
            super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted Canal Plus - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

def update_canal_plus(sender, **kwargs):
    print("CalledLine 975: ", kwargs)
    created_item = kwargs['instance']
    print(created_item.purpose)
    if kwargs['created']:
        canal = CanalPlus.objects.get(canal_plus_items=created_item)
        if (created_item.purpose == "Recharge"):
            print("TRUE LINE 981")
            print(canal)
            print("TRUE LINE 983")

            canal.total += created_item.total_amount
            if canal.reorder_level != "" or canal.reorder_level != 0:
                canal.reorder_level = canal.reorder_level
            canal.available_balance += created_item.total_amount
            # canal.total_amount_sold += canal.total_amount_sold 
            canal.save()

        elif (kwargs['instance'].purpose == "Abonnement"):
            print("Abonnement Action")
            canal.available_shop += created_item.quantity
            canal.available_stock -= created_item.quantity
            if canal.reorder_level != "" or canal.reorder_level != 0:
                canal.reorder_level = created_item.reorder_level
            if canal.available_shop <= 0:
                canal.active = "In-Active"
            canal.save()
        
        elif (kwargs['instance'].purpose == "Reabonnement"):
            print("Reabonnement Action")
            print(canal.available_shop)
            # canal.total += created_item.total_amount
            if canal.reorder_level != "" or canal.reorder_level != 0:
                canal.reorder_level = canal.reorder_level
            canal.available_balance -= created_item.total_amount
            canal.total_amount_sold += created_item.total_amount
            canal.save()


PURPOSE = (('Recharge', 'Recharge'), ('Abonnement', 'Abonnement'), ('Reabonnement', 'Reabonnement'))
class CanalPlusItem(models.Model):
    canal_plus = models.ForeignKey(CanalPlus, related_name='canal_plus_items', on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='canal_plus_items_creator', on_delete=models.SET_NULL)
    purpose = models.CharField(max_length=15, blank=False, choices=PURPOSE)

    amount = models.IntegerField(default='0', blank=False, null=False)
    quantity = models.IntegerField(default='1', blank=False, null=False)
    total_amount = models.IntegerField(default='0', blank=False, null=False)
    comments = models.CharField(max_length=25, unique=True, null=True, blank=False)
    reorder_level = models.IntegerField(default='20000', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            try:
                print("args LINE 1042:", args)
                super().save(args, kwargs)
                id_length = len(str(self.id))
                code_length = 7 - id_length
                zeros = "".join("0" for i in range(code_length))
                self.code = f"GLC-CPI{zeros}{self.id}"
                self.save()
            except:
                print("Level 1050 model ERROR")

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("CanalPlus Update Action")
                action = f"updated canal_plus item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("Inventory Create Action")
                action = f"added new canal_plus item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)

                if self.total_amount == "" or self.total_amount == 0:
                    self.total_amount = self.amount * self.quantity
                
                if self.purpose == "Recharge":
                    t = self.quantity * self.amount
                    if (self.total_amount != 0 or self.cost_price_total != None):
                        total_amount_recharge = self.total_amount
                    else:
                        total_amount_recharge = t
                    recharge(self.created_by, self.canal_plus, self.quantity,
                        self.amount, total_amount_recharge
                    )
                
                if self.purpose == "Supply":
                    supply(self.created_by, self.inventory, self.quantity,
                        self.quantity, self.selling_price_unit, self.selling_price_bulk,
                    )

                if self.purpose == "Sale":
                    total_amount_sold = self.quantity * self.sold_price_unit
                    sale(self.created_by, self.inventory, self.quantity,
                        self.quantity, self.sold_price_unit, self.sold_price_unit,
                        total_amount_sold
                    )
                        
            # self.total_amount = self.quantity * self.amount 
            super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        created_by = self.created_by
        # action = f"deleted Inventory item - '{self.inventory.name}'"
        action = "deleted Canal_plus item" + "self.inventory.name"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        # return f"{self.inventory.name} - {self.code}"
        return f"{self.canal_plus.name} - {self.canal_plus.code}"

post_save.connect(update_canal_plus, sender=CanalPlusItem)


class ItemCanalRecharge(models.Model):
    recharger = models.CharField(max_length=50, unique=False)
    canal_plus = models.CharField(max_length=50, unique=False)
    quantity = models.IntegerField(default='0', blank=False, null=False)
    amount = models.FloatField(default=0, blank=True)
    total = models.FloatField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.recharger} Recharged {self.canal_plus} on {self.created_at}"


class ItemCanalAbonnement(models.Model):
    subscriber = models.CharField(max_length=50, unique=False)
    canal_plus = models.CharField(max_length=50, unique=False)
    quantity = models.IntegerField(default='0', blank=False, null=False)
    amount = models.FloatField(default=0, blank=True)
    total = models.FloatField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.subscriber} Subscribed {self.canal_plus} on {self.created_at}"


class ItemCanalReabonnement(models.Model):
    resubscriber = models.CharField(max_length=50, unique=False)
    canal_plus = models.CharField(max_length=50, unique=False)
    quantity = models.IntegerField(default='0', blank=False, null=False)
    amount = models.FloatField(default=0, blank=True)
    total = models.FloatField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.resubscriber} Resubscribed {self.canal_plus} on {self.created_at}"
