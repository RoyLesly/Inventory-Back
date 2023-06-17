from datetime import datetime, timezone
from django.db import models
from user_control.models import CustomUser
from user_control.views import add_user_activity
from django.db.models.signals import post_save


#  XXXXXXXXXXXXXXXXXXX IVENTORY SECTION XXXXXXXXXXXXXXXXXXX
def purchase(purchaser, inventory, quantity_unit, quantity_bulk, cost_price_unit, cost_price_bulk, cost_price_total):
    ItemPurchase.objects.create(
        purpose="purchase",
        purchaser=purchaser.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        cost_price_unit=cost_price_unit,
        cost_price_bulk=cost_price_bulk,
        cost_price_total=cost_price_total,
    )
    print("PUCHASE COMPLETE LINE 26 Models")


def supply(supplier, inventory, quantity_unit, quantity_bulk, selling_price_unit, selling_price_bulk):
    ItemSupply.objects.create(
        purpose="supply",
        supplier=supplier.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        selling_price_unit=selling_price_unit,
        selling_price_bulk=selling_price_bulk,
    )


def sale(seller, inventory, quantity_unit, quantity_bulk, sold_price_unit, sold_price_bulk, sold_price_total):
    ItemSale.objects.create(
        purpose="sale",
        seller=seller.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        sold_price_unit=sold_price_unit,
        sold_price_bulk=sold_price_bulk,
        sold_price_total=sold_price_total,
    )


# def papers_used(user, inventory, quantity, ):
#     PapersUsed.objects.create(
#         user=user.first_name,
#         inventory=inventory.name,
#         quantity=quantity,
#     )

#  XXXXXXXXXXXXXXXXXXX CANAL +  SECTION XXXXXXXXXXXXXXXXXXX
def recharge(recharger, canal_plus, amount, state):
    CanalItemRecharge.objects.create(
        recharger=recharger.first_name,
        canal_plus=canal_plus.name,
        amount=amount,
        state=state,
    )

def abonnement(subscriber, canal_plus, amount, phone, decoder, state):
    CanalItemAbonnement.objects.create(
        subscriber=subscriber.first_name,
        canal_plus=canal_plus.name,
        amount=amount,
        phone=phone,
        decoder=decoder,
        state=state,
    )


def reabonnement(resubscriber, canal_plus, amount, phone, decoder, state):
    CanalItemReabonnement.objects.create(
        resubscriber=resubscriber.first_name,
        canal_plus=canal_plus.name,
        amount=amount,
        phone=phone,
        decoder=decoder,
        state=state,
    )

#  XXXXXXXXXXXXXXXXXXX ASSETS SECTION XXXXXXXXXXXXXXXXXXX
def purchase_asset(purchaser, asset, quantity, cost_price):
    AssetPurchase.objects.create(
        purchaser = purchaser.first_name,
        asset = asset.name,
        quantity = quantity,
        cost_price = cost_price,
        total = cost_price * quantity,
    )


def repair_asset(maintener, asset, diagnosis, state, recommendations, cost_price):
    AssetRepairs.objects.create(
        maintener=maintener,
        asset=asset.name,
        diagnosis=diagnosis,
        state=state,
        recommendations=recommendations,
        cost_of_repair=cost_price,
    )


def discard_asset(person, asset, reason, state, recommendations, quantity):
    AssetDiscard.objects.create(
        person=person,
        asset=asset.name,
        reason=reason,
        state=state,
        recommendations=recommendations,
        quantity=quantity,
    )

#  XXXXXXXXXXXXXXXXXXX MONEY SECTION XXXXXXXXXXXXXXXXXXX
def money_refill(purchaser, inventory, quantity_unit, quantity_bulk, cost_price_unit, cost_price_bulk, cost_price_total):
    ItemPurchase.objects.create(
        purchaser=purchaser.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        cost_price_unit=cost_price_unit,
        cost_price_bulk=cost_price_bulk,
        cost_price_total=cost_price_total,
    )
    print("PUCHASE COMPLETE LINE 26 Models")


def mtn_mobile_money(supplier, inventory, quantity_unit, quantity_bulk, selling_price_unit, selling_price_bulk):
    ItemSupply.objects.create(
        supplier=supplier.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        selling_price_unit=selling_price_unit,
        selling_price_bulk=selling_price_bulk,
    )


def orange_money(supplier, inventory, quantity_unit, quantity_bulk, selling_price_unit, selling_price_bulk):
    ItemSupply.objects.create(
        supplier=supplier.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        selling_price_unit=selling_price_unit,
        selling_price_bulk=selling_price_bulk,
    )


def mtn_credit_transfer(seller, inventory, quantity_unit, quantity_bulk, sold_price_unit, sold_price_bulk, sold_price_total):
    ItemSale.objects.create(
        seller=seller.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        sold_price_unit=sold_price_unit,
        sold_price_bulk=sold_price_bulk,
        sold_price_total=sold_price_total,
    )


def orange_credit_transfer(seller, inventory, quantity_unit, quantity_bulk, sold_price_unit, sold_price_bulk, sold_price_total):
    ItemSale.objects.create(
        seller=seller.first_name,
        inventory=inventory.name,
        quantity_unit=quantity_unit,
        quantity_bulk=quantity_bulk,
        sold_price_unit=sold_price_unit,
        sold_price_bulk=sold_price_bulk,
        sold_price_total=sold_price_total,
    )


def income_db(created_by, income_outcome, total_amount, issuer, reciever, state, comments):

    IncomeDb.objects.create(
        person = created_by.first_name,
        income_outcome = income_outcome.name,
        total_amount = total_amount,
        issuer = issuer,
        reciever = reciever,
        state = state,
        reason = comments,
    )


def outcome_db(created_by, income_outcome, total_amount, issuer, reciever, state, comments):

    OutcomeDb.objects.create(
        person = created_by.first_name,
        income_outcome = income_outcome.name,
        total_amount = total_amount,
        issuer = issuer,
        reciever = reciever,
        state = state,
        reason = comments,
    )

#  ================================== IVENTORY SECTION ==================================
class InventoryGroup(models.Model):
    created_by = models.ForeignKey(CustomUser, null=True, related_name='inventory_groups', on_delete=models.SET_NULL)
    name = models.CharField(max_length=60, unique=True)
    belongs_to = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True, related_name='group_relations')
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
    name = models.CharField(max_length=30, unique=True, null=True, blank=False)
    code = models.CharField(max_length=11, unique=True, null=True, blank=True)
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
            code_length = 3 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-Inv-{zeros}{self.id}"
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
            print("Purchase Action -  line 198")
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
            if inven.available_stock < created_item.quantity:
                raise Exception("NOT ENOUGH IN STOCK")

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
                id_length = len(str(self.id))
                code_length = 5 - id_length
                zeros = "".join("0" for i in range(code_length))
                self.code = f"GLC-Inv-I-{zeros}{self.id}"
                self.save()
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
            except:
                print("Level 432 model ERROR")

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                action = f"updated inventory item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
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
        return f"{self.inventory.name} - {self.inventory.code}"


def update_inventory_item(sender, **kwargs):
    print("INVOICE CALLED UPDATED INVEN-ITEM")
    created_item = kwargs['instance']
    if kwargs['created']:
        # print("kwargs : ", kwargs)
        # print("created_item.item : ", created_item.item)
        print("created_item MMMMMMMMMMMMMMMMMMMMMMMMm")
        print(created_item)
        print(created_item.quantity)
        print(created_item.amount)
        print(created_item.total)
    
        
        test = InventoryItem.objects.create(
                created_by = created_item.invoice.created_by,
                inventory = created_item.item,
                purpose = "Sale",
                quantity = created_item.quantity,
                sold_price_unit = created_item.amount,
                sold_price_total = created_item.total,
                issue_by = "Anonym.user",
                issue_to = "Customer",
            )
        test.save()
        

post_save.connect(update_inventory, sender=InventoryItem)


class ItemPurchase(models.Model):
    purchaser = models.CharField(max_length=50, unique=False)
    purpose = models.CharField(max_length=50, unique=False)
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
    purpose = models.CharField(max_length=50, unique=False)
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
    purpose = models.CharField(max_length=50, unique=False)
    inventory = models.CharField(max_length=50, unique=False)
    quantity_unit = models.IntegerField(default='0', blank=False, null=False)
    quantity_bulk = models.IntegerField(default='0', blank=False, null=False)
    sold_price_unit = models.FloatField(default=0, blank=True)
    sold_price_bulk = models.FloatField(default=0, blank=True, null=True)
    sold_price_total = models.FloatField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        
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
    total = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        if self.item.available_shop < self.quantity:
            raise Exception(f"item with code {self.item.code} is not enough")
        print("HERRRR")
        self.item_name = self.item.name
        self.item_code = self.item.code
        self.item.available_shop -= self.quantity
        self.item.total_quantity_sold += self.quantity
        self.item.total_amount_sold += self.total
        # self.item.save()
        print("HERRRR2")
        print(
            kwargs,
            self.amount,
            self.quantity,
            self.total
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} = {self.quantity}"

post_save.connect(update_inventory_item, sender=InvoiceItem)


# SERVICES SECTION =======================================================
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
        action = f"added new service group - '{self.name}'"
        if self.pk is not None:
            action = f"updated service group from - '{self.old_name}' to '{self.name}'"

        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted service group - '{self.name}'"

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

    service_cost = models.FloatField(default=0, blank=True)
    total_quantity_sold = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_amount_sold = models.PositiveIntegerField(null=True, default=0, blank=True)

    active = models.BooleanField(default=True)
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
            id_length = len(str(self.id))
            code_length = 2 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-Ser-{zeros}{self.id}"
            print(self.code)
            self.save()

        else:
            if str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                action = f"updated Service with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.created_at)[:18] == str(datetime.now(timezone.utc))[:18]:
                action = f"added new Service Item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted Service - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.name} - {self.code}"


def update_service(sender, **kwargs):
    print("LINE 628 SIGNAL CALLED", kwargs)
    created_item = kwargs['instance']
    print(created_item.total_amount, "631")

    if kwargs['created']:
        service = Service.objects.get(service_items=created_item)
        print(service.total_amount_sold)
        service.total_quantity_sold += created_item.quantity
        service.total_amount_sold += created_item.total_amount
        print(service.total_amount_sold)
        service.save()


class ServiceItem(models.Model):
    service = models.ForeignKey(Service, related_name='service_items', on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='service_items_creator', on_delete=models.SET_NULL)
    quantity = models.IntegerField(default='0', blank=False, null=False)

    paid_amount_unit = models.FloatField(default=0, null=False)
    total_amount = models.FloatField(default=0, blank=True)
    comments_1 = models.CharField(default="", max_length=250, null=True, blank=True)
    comments_2 = models.CharField(default="", max_length=250, null=True, blank=True)

    issue_to = models.CharField(max_length=50, default="", blank=True, null=True)
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        papers = ["DV Lottery Single", "Photocopy Color", "Photocopy B/W", "Printing Color", "Printing B/W", "Numero Unique"]
        if self.total_amount == "" or self.total_amount == 0:
            self.total_amount = self.paid_amount_unit * self.quantity 
        if self.service.name in papers:
            pass #raise Exception("FOUND")
        if self.service.name != "UNKNOWN":
            pass #raise Exception(self.service.name)

        if is_new:
            super().save(*args, **kwargs)
            id_length = len(str(self.id))
            code_length = 4 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-SI-{zeros}{self.id}"
            self.save()

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("Service Update Action")
                action = f"updated Service item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("Service Create Action")
                action = f"added new Service item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = "deleted Service item" + "self.service.name"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.service.name} - {self.service.code}"


post_save.connect(update_service, sender=ServiceItem)


# MONEY SECTION =======================================================================
class MoneyType(models.Model):
    name = models.CharField(max_length=20, unique=True, null=True, blank=False)
    code = models.CharField(max_length=10, unique=True, null=False, blank=True)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='MT_creator', on_delete=models.SET_NULL)
    description = models.CharField(max_length=100, blank=True, null=True)

    reorder_level = models.IntegerField(default='2', blank=True, null=True)
    total_refills = models.PositiveIntegerField(blank=True, default=0, null=True)
    available_amount = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_transactions = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_amount_cash_in = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_amount_cash_out = models.PositiveIntegerField(null=True, default=0, blank=True)

    active = models.BooleanField(default=True)
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

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


def update_money_type(sender, **kwargs):
    print(kwargs)
    created_item = kwargs['instance']
    if kwargs['created']:
        try:
            money = MoneyType.objects.get(money_type_items=created_item)
        except:
            money = MoneyType.objects.get(money_refill_items=created_item)
        created_item_amount = int(created_item.amount)
        print(created_item_amount, money.total_refills)
        print(created_item_amount + money.total_refills)
            
        if (created_item.type.name == "MTN Mobile Money"):
            print("MTN Mobile Money Action ---------->  line 868")
            if (created_item.type2.name == "DEPOT / CASH IN - MTN"):
                print("MTN MoMo DEPOT ---------->  line 815")
                if money.available_amount < created_item_amount:
                    print("TRUE NOT SUFFICIENT FUNDS ----------------> 820")
                money.available_amount -= created_item_amount
                money.total_amount_cash_in += created_item_amount
            if (created_item.type2.name == "RETRAIT / CASH OUT MTN"):
                print("MTN MoMo RETRAIT -------->  line 820")
                money.available_amount += created_item_amount
                money.total_amount_cash_out += created_item_amount

            if (created_item.type2.name == "REFILL - MTN"):
                print("MTN MoMo REFILL -------->  line 820")
                money.total_refills += created_item_amount
                money.available_amount += created_item_amount

        elif (created_item.type.name == "Orange Money"):
            print("ORANGE Money Action -  line 769")
            if (created_item.type2.name == "DEPOT / CASH IN - ORANGE"):
                print("Orange Money RETRAIT ---------->  line 827")
                if money.available_amount < created_item_amount:
                    raise Exception("Insufficient FUNDS")
                money.available_amount -= created_item_amount
                money.total_amount_cash_in += created_item_amount
            if (created_item.type2.name == "RETRAIT / CASH OUT ORANGE"):
                print("Orange Money DEPOT ---------->  line 831")
                money.available_amount += created_item_amount
                money.total_amount_cash_out += created_item_amount

            if (created_item.type2.name == "REFILL - ORANGE"):
                print("Orange Money REFILL ---------->  line 831")
                money.total_refills += created_item_amount
                money.available_amount += created_item_amount

        elif (created_item.type.name == "MTN Credit Transfer"):
            print("MTN Credit Action -  line 769")
            if money.available_amount < created_item_amount:
                    raise Exception("Insufficient FUNDS")
            money.available_amount -= created_item_amount
            money.total_amount_cash_in += created_item_amount
            if (created_item.type2.name == "RETRAIT / CASH OUT ORANGE"):
                money.available_amount += created_item_amount
                money.total_amount_cash_out += created_item_amount

        elif (created_item.type.name == "Orange Credit Transfer"):
            print("ORANGE Money Action -  line 769")
            if (created_item.type2.name == "DEPOT / CASH IN - ORANGE"):
                if money.available_amount < created_item_amount:
                    raise Exception("NOT SUFFICIENT FUNDS")
                money.available_amount -= created_item_amount
                money.total_amount_cash_in += created_item_amount
            if (created_item.type2.name == "RETRAIT / CASH OUT ORANGE"):
                money.available_amount += created_item_amount
                money.total_amount_cash_out += created_item_amount

        elif (created_item.type.name == "Refill MTN Mobile Money"):
            money.available_amount += created_item_amount
        elif (created_item.type.name == "Refill Orange Money"):
            money.available_amount += created_item_amount
        money.total_transactions += 1  
        money.save()


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

    class Meta:
        ordering = ("-created_at", )

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
    STATE = (("Success", "Success"), ("Failed", "Failed"), ("Pending", "Pending"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='transaction_created_by', on_delete=models.SET_NULL)
    customer_number = models.CharField(max_length=15, unique=False, null=False, blank=False)
    customer_name = models.CharField(max_length=25, unique=False, null=False, blank=False)
    category = models.ForeignKey(MoneyType, default="1", unique=False, related_name='money_type_items', on_delete=models.SET_DEFAULT)
    type = models.ForeignKey(MoneyTransactionType, default="1", unique=False, related_name='money_transaction_type_items', on_delete=models.SET_DEFAULT)
    type2 = models.ForeignKey(MoneyTransactionDetail, default="1", unique=False, related_name='money_transaction_detail_items', on_delete=models.SET_DEFAULT)
    amount = models.CharField(max_length=6, null=False, unique=False)
    state = models.CharField(max_length=15, choices=STATE)
    balance = models.CharField(max_length=100, blank=True, null=False)
    comments = models.CharField(max_length=100, blank=True, null=True)

    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"{self.customer_number} - {self.type} - {self.type2}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)
            code_length = 3 - len(str(self.id))
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-MT-{zeros}{self.id}"
            self.save()

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("TMoney ransaction Update Action")
                action = f"updated Money transaction item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("Transaction Create Action 903")
                action = f"aNew Money Transaction Created with code - '{self.created_by}'"
                add_user_activity(self.created_by, action=action)
            super().save(*args, **kwargs)


class MoneyRefill(models.Model):
    STATE = (("Success", "Success"), ("Failed", "Failed"), ("Pending", "Pending"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='money_refill_created_by', on_delete=models.SET_NULL)
    money_type = models.ForeignKey(MoneyType, default="1", unique=False, related_name='money_refill_items', on_delete=models.SET_DEFAULT)
    # type = models.ForeignKey(MoneyTransactionType, default="1", unique=False, related_name='money_refill_type_items', on_delete=models.SET_DEFAULT)
    # type2 = models.ForeignKey(MoneyTransactionDetail, default="1", unique=False, related_name='money_refill_type_items', on_delete=models.SET_DEFAULT)
    type = models.CharField(default="Refill", editable=False, max_length=7, unique=False, blank=True)
    code = models.CharField(max_length=10, unique=True, null=False, blank=True)
    amount = models.IntegerField(null=False, unique=False)
    comments = models.CharField(max_length=100, blank=True, null=True)

    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.money_type.name} -{self.type} - {self.amount}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)
            code_length = 4 - len(str(self.id))
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-MR-{zeros}{self.id}"
            self.save()

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("Money Refill Update Action")
                action = f"Updated Money Refill with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("Transaction Create Action 903")
                action = f"Money Refill Created with code - '{self.created_by}'"
                add_user_activity(self.created_by, action=action)
            super().save(*args, **kwargs)


def update_money_transaction(sender, **kwargs):
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
        
post_save.connect(update_money_type, sender=MoneyRefill)

post_save.connect(update_money_type, sender=MoneyTransaction)
# ========================================================================

# CANAL PLUS SECTION =====================================================
class CanalPlus(models.Model):
    ACTIVE_STATUS = (("Active", "Active"), ("In-Active", "In-Active"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='canal_created_by', on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, unique=True, null=True, blank=False)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    total = models.PositiveIntegerField(blank=True, default=0, null=True)
    available_balance = models.PositiveIntegerField(blank=True, default=0, null=True)
    total_amount_recharged = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_amount_subscribed = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_amount_resubscribed = models.PositiveIntegerField(null=True, default=0, blank=True)

    reorder_level = models.IntegerField(default='20000', blank=True, null=True)
    export_to_csv = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"{self.name} - {self.total} - {self.available_balance}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            super().save(*args, **kwargs)
            id_length = len(str(self.id))
            code_length = 3 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-CP-{zeros}{self.id}"
            self.save()

        else:
            if str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("False Not same Update 1103 Models")
                action = f"updated canal_plus with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                print("True same update 975 Model")
                action = f"added new canal_plus Item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)
            elif str(self.created_at)[:18] == str(datetime.now(timezone.utc))[:18]:
                print("True same 980 Model")
                action = f"added new canal_plus Item with code - '{self.code}'"
                add_user_activity(self.created_by, action=action)
                super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted Canal Plus item - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.name} - {self.code}"


def update_canal_plus(sender, **kwargs):
    print("LINE 997 SIGNAL CALLED", kwargs)
    created_item = kwargs['instance']
    if kwargs['created']:
        canal = CanalPlus.objects.get(canal_plus_items=created_item)
        if (created_item.purpose == "Recharge"):
            canal.total += created_item.total_amount
            canal.available_balance += created_item.total_amount
            canal.total_amount_recharged += created_item.total_amount
            if canal.reorder_level != "" or canal.reorder_level != 0:
                canal.reorder_level = canal.reorder_level
            canal.save()

        elif (kwargs['instance'].purpose == "Abonnement"):
            print("Abonnement Action")
            canal.total_amount_subscribed += created_item.total_amount
            if canal.reorder_level != "" or canal.reorder_level != 0:
                canal.reorder_level = created_item.reorder_level
            if canal.available_balance <= 10000:
                canal.active = False
            canal.save()
        
        elif (kwargs['instance'].purpose == "Reabonnement"):
            print("Reabonnement Action")
            print(canal.available_balance)
            print(canal.total)
            if canal.available_balance != 0:
                canal.available_balance -= created_item.total_amount
            else:
                canal.available_balance = created_item.total_amount
            if canal.reorder_level != "" or canal.reorder_level != 0:
                canal.reorder_level = canal.reorder_level
            canal.total_amount_resubscribed += created_item.total_amount
            canal.save()
        

PURPOSE = (('Recharge', 'Recharge'), ('Abonnement', 'Abonnement'), ('Reabonnement', 'Reabonnement'))
STATE = (("Success", "Success"), ("Pending", "Pending"), ("Fail","Fail"))
class CanalPlusItem(models.Model):
    canal_plus = models.ForeignKey(CanalPlus, related_name='canal_plus_items', on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, null=True, related_name='canal_plus_items_creator', on_delete=models.SET_NULL)
    purpose = models.CharField(max_length=15, blank=False, choices=PURPOSE)
    phone = models.IntegerField(default='0', blank=False, null=False)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    decoder_number = models.IntegerField(default='0', blank=False, null=False)
    
    amount = models.IntegerField(default='0', blank=False, null=False)
    quantity = models.IntegerField(default='1', blank=False, null=False)
    total_amount = models.IntegerField(default='0', blank=True, null=False)
    state = models.CharField(max_length=25, blank=True, choices=STATE, default="Success")
    comments = models.CharField(max_length=50, blank=True, unique=False, null=True)
    reorder_level = models.IntegerField(default='20000', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.total_amount = int(self.quantity) * int(self.amount)

        if is_new:
            print("LINE 1193 NEW CPI")
            super().save(*args, **kwargs)
            print("Line 1195 model OK <------------------")
            code_length = 4 - len(str(self.id))
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-CPI-{zeros}{self.id}"
            print("Line 1199 Code ------->", self.code)
            self.save()

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("1090 CanalPlus Update Action")
                action = f"updated CanalPlus item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("1207 CanalPlus Create Action")
                
                print("Level 1209 model <-------------------")
            
                if self.purpose == "Recharge":
                    print("Recharge ACTION")
                    recharge( self.created_by, self.canal_plus, self.amount, self.state )
                    print("Recharge 1214: CREATED ---------------------------",)
                    action = f"added Canal Recharge with code - '{self.created_by.first_name}'"
                    add_user_activity(self.created_by, action=action)

                if self.purpose == "Abonnement":
                    print("Abonnement ACTION")
                    abonnement(self.created_by, self.canal_plus, self.amount, 
                        self.phone, self.decoder_number, self.state
                    )
                    print("Abonnement 1221: CREATED ---------------------------",)
                    action = f"added Canal Abonnement with code - '{self.created_by.first_name}'"
                    add_user_activity(self.created_by, action=action)
                
                if self.purpose == "Reabonnement":
                    print("Reabonnement ACTION")
                    if self.canal_plus.available_balance < self.amount:
                        raise Exception("Not Enough Funds")
                    reabonnement(self.created_by, self.canal_plus, self.amount, 
                        self.phone, self.decoder_number, self.state
                    )
                    action = f"added Canal Reabonnement with code - '{self.created_by.first_name}'"
                    add_user_activity(self.created_by, action=action)
                    print("Recharge 1228: CREATED ---------------------------",)

                action = f"added new CanalPlus item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)                        
            super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = "deleted CanalPlus item" + "self.canal_plus.name"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.canal_plus.name} - {self.canal_plus.code}"


def update_canal_plus_item(sender, **kwargs):
    print("INVOICE CALLED UPDATED INVEN ITEM")
    created_item = kwargs['instance']
    print("344:--------", created_item)
    if kwargs['created']:
        
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
        

post_save.connect(update_canal_plus, sender=CanalPlusItem)


class CanalItemRecharge(models.Model):
    recharger = models.CharField(max_length=50, unique=False)
    canal_plus = models.CharField(max_length=50, unique=False)
    state = models.CharField(max_length=50)
    amount = models.FloatField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.recharger} Recharged {self.canal_plus} on {self.created_at}"


class CanalItemAbonnement(models.Model):
    subscriber = models.CharField(max_length=50, unique=False)
    canal_plus = models.CharField(max_length=50, unique=False)
    state = models.CharField(max_length=50, default="Success")
    amount = models.FloatField(default=0, blank=True, null=True)
    phone = models.IntegerField(default=0, blank=True)
    decoder = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.subscriber} Sold {self.canal_plus} on {self.created_at}"


class CanalItemReabonnement(models.Model):
    resubscriber = models.CharField(max_length=50, unique=False)
    canal_plus = models.CharField(max_length=50, unique=False)
    state = models.CharField(max_length=50)
    amount = models.FloatField(default=0, blank=True)
    phone = models.IntegerField(default=0, blank=True)
    decoder = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.resubscriber} Sold {self.canal_plus} on {self.created_at}"

# =============================================================================

# ASSETS SECTION ==============================================================
class AssetGroup(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name='asset_groups', on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=60, unique=True)
    belongs_to = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='group_relations'
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
    name = models.CharField(max_length=30, unique=True, null=True, blank=False)
    code = models.CharField(max_length=11, unique=True, null=True, blank=True)
    description_1 = models.CharField(max_length=100, blank=True, null=True)
    description_2 = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    group = models.ForeignKey(AssetGroup, related_name='assets', null=True, on_delete=models.SET_NULL)

    repairs = models.IntegerField(default='0', blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    available_quantity = models.IntegerField(default='0', blank=True, null=True)
    reorder_level = models.IntegerField(default='1', blank=True, null=True)
    cost_price = models.FloatField(default=0, blank=True)
    total = models.PositiveIntegerField(blank=True, default=0, null=True)
    
    physical_state = models.BooleanField(default=True)
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
            code_length = 3 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-Ass-{zeros}{self.id}"
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


class AssetAccessory(models.Model):
    created_by = models.ForeignKey(CustomUser, null=True, related_name='asset_accessory_creator', on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, unique=True, null=True, blank=False)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    asset = models.ForeignKey(Asset, related_name='assets', null=True, on_delete=models.SET_NULL)
    description_1 = models.CharField(max_length=100, blank=True, null=True)
    condition = models.BooleanField(default=True)


def update_asset(sender, **kwargs):
    created_item = kwargs['instance']
    if kwargs['created']:
        asset = Asset.objects.get(asset_items=created_item)
        if (created_item.purpose == "Purchase"):
            asset.quantity += created_item.quantity
            asset.available_quantity += created_item.quantity
            asset.physical_state = created_item.physical_state
            asset.reorder_level = created_item.reorder_level
            asset.cost_price = created_item.cost_price
            asset.total = created_item.cost_price * created_item.quantity
            asset.save()

        elif (kwargs['instance'].purpose == "Repair"):
            print("Repair Asset Action 1230")
            asset.physical_state = created_item.physical_state
            asset.repairs += 1
            asset.save()
        
        elif (kwargs['instance'].purpose == "Discard"):
            print("Discard Asset Action 1236")
            asset.physical_state = False
            if asset.available_quantity < created_item.quantity:
                pass
                # return Error
            else:
                asset.available_quantity -= created_item.quantity
            asset.save()
 

class AssetItem(models.Model):
    PHYSICAL_STATE= (("Good", "Good"), ("Bad", "Bad"))
    ASSET_PURPOSE= (("Purchase", "Purchase"), ("Repair", "Repair"), ("Discard","Discard"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='asset_item_creator', on_delete=models.SET_NULL)
    asset = models.ForeignKey(Asset, related_name='asset_items', on_delete=models.CASCADE)
    purpose = models.CharField(max_length=15, blank=False, choices=ASSET_PURPOSE)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    maintener_discarder = models.CharField(max_length=20, unique=False, null=True, blank=True)
    diagnosis_reason = models.CharField(max_length=150, unique=False, null=True, blank=True)
    state = models.CharField(max_length=10, default="Good", choices=PHYSICAL_STATE)
    recommendations = models.CharField(max_length=150, unique=False, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    reorder_level = models.IntegerField(default='2', blank=True, null=True)
    cost_price = models.FloatField(default=0, blank=True)
    quantity = models.PositiveIntegerField(blank=True, default=1, null=True)
    total_amount = models.PositiveIntegerField(blank=True, default=0, null=True)
    
    physical_state = models.BooleanField(default=True)
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.total_amount = self.quantity * self.cost_price 

        if is_new:
            super().save(args, kwargs)
            print("Line 1478 model OK <------------------")
            id_length = len(str(self.id))
            code_length = 4 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-ASI{zeros}{self.id}"
            print("Line 14835 Code ------->", self.code)
            self.save()
            print("Level 1485 model <-------------------")
            
            if self.purpose == "Purchase":
                print("Recharge ACTION")
                purchase_asset( self.created_by, self.asset, self.quantity, self.cost_price )
                print("Purchase Asset 1490: CREATED ---------------------------",)
            
            if self.purpose == "Repair":
                print("Repair ACTION")
                repair_asset(self.maintener_discarder, self.asset, self.diagnosis_reason, 
                    self.state, self.recommendations, self.cost_price
                )
                print("Repair 1497: CREATED ---------------------------",)
            
            if self.purpose == "Discard":
                print("1295 Discard ACTION")
                discard_asset(self.maintener_discarder, self.asset, self.diagnosis_reason, 
                    self.state, self.recommendations, self.quantity
                )
                print("Discard 1504: CREATED ---------------------------",)

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("1240 Asset Update Action")
                action = f"updated CanalPAssetlus item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("1518 Asset Create Action")
                action = f"added new Asset item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)                        
            super().save(*args, **kwargs)



    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted Asset item - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.asset.name} - {self.code}"


def update_asset_item(sender, **kwargs):
    print("INVOICE_ASSET CALLED UPDATED ASSET ITEM")
    created_item = kwargs['instance']
    print("344:--------", created_item)
    if kwargs['created']:
        
        test = AssetItem.objects.create(
                created_by = created_item.invoice.created_by,
                asset = created_item.item,
                purpose = "Sale",
                quantity = created_item.quantity,
                sold_price_unit = created_item.amount/created_item.quantity,
                sold_price_total = created_item.amount,
                issue_by = "Anonym.user",
                issue_to = "Customer",
            )
        test.save()
  

post_save.connect(update_asset, sender=AssetItem)


class AssetPurchase(models.Model):
    purchaser = models.CharField(max_length=50, unique=False)
    asset = models.CharField(max_length=50, unique=False)
    quantity = models.IntegerField(default='0', blank=False, null=False)
    cost_price = models.FloatField(default=0, blank=True)
    total = models.FloatField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.purchaser} Purchased {self.asset} on {self.created_at}"


class AssetRepairs(models.Model):
    maintener = models.CharField(max_length=50, unique=False)
    asset = models.CharField(max_length=50, unique=False)
    diagnosis = models.CharField(max_length=50, unique=False)
    cost_of_repair = models.IntegerField(unique=False)
    state = models.CharField(max_length=50, unique=False)
    recommendations = models.CharField(max_length=50, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.maintener} Repaired {self.asset} on {self.created_at}"


class AssetDiscard(models.Model):
    person = models.CharField(max_length=50, unique=False)
    asset = models.CharField(max_length=50, unique=False)
    quantity = models.IntegerField(unique=False)
    reason = models.CharField(max_length=50, unique=False)
    state = models.CharField(max_length=50, unique=False)
    recommendations = models.CharField(max_length=50, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.person} Threw {self.asset} on {self.created_at}"


class IncomeOutcome(models.Model):
    created_by = models.ForeignKey(CustomUser, null=True, related_name='income_outcome_creator', on_delete=models.SET_NULL)
    name = models.CharField(max_length=30, unique=True, null=True, blank=False)
    code = models.CharField(max_length=11, unique=True, null=True, blank=True)
    number_of_transactions = models.IntegerField(default='0', blank=True, null=True)
    income_transactions = models.IntegerField(default='0', blank=True, null=True)
    outcome_transactions = models.IntegerField(default='0', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)
            code_length = 2 - len(str(self.id))
            zeros = "".join("0" for i in range(code_length))
            self.code = f"GLC-Inc-Out-{zeros}{self.id}"
            self.save()

        else:
            if str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                add_user_activity(self.created_by, action=f"updated INC-OUT with code - '{self.code}'")
                super().save(*args, **kwargs)
            elif str(self.updated_at)[:18] != str(datetime.now(timezone.utc))[:18]:
                add_user_activity(self.created_by, action=f"added new INC-OUT Item with code - '{self.code}'")
                super().save(*args, **kwargs)
            elif str(self.created_at)[:18] == str(datetime.now(timezone.utc))[:18]:
                add_user_activity(self.created_by, action=f"added new INC-OUT Item with code - '{self.code}'")
                super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted Inc-Out item - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.name} - {self.code}"


def update_income_outcome(sender, **kwargs):
    created_item = kwargs['instance']
    if kwargs['created']:
        in_out = IncomeOutcome.objects.get(inc_out_items=created_item)
        in_out.number_of_transactions += 1
        if (created_item.purpose == "Income"):
            print("Income Action -  line 1727")
            in_out.income_transactions += 1
            in_out.save()

        elif (kwargs['instance'].purpose == "Outcome"):
            print("Outcome 1727")
            in_out.outcome_transactions += 1
            in_out.save()
        

class IncomeOutcomeItem(models.Model):
    PURPOSE= (("Income", "Income"), ("Outcome", "Outcome"))
    STATE= (("Good", "Good"), ("Bad", "Bad"))
    created_by = models.ForeignKey(CustomUser, null=True, related_name='income_outcome_item_creator', on_delete=models.SET_NULL)
    income_outcome = models.ForeignKey(IncomeOutcome, related_name='inc_out_items', on_delete=models.CASCADE)
    purpose = models.CharField(max_length=15, blank=False, choices=PURPOSE)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    issuer = models.CharField(max_length=20, unique=False, null=True, blank=True)
    reciever = models.CharField(max_length=25, unique=False, null=True, blank=True)
    comments = models.CharField(max_length=150, unique=False, null=True, blank=True)
    state = models.CharField(max_length=10, default="Good", choices=STATE)
    total_amount = models.PositiveIntegerField(blank=True, default=0, null=True)
    export_to_csv = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)
            print("Line 1761 model OK <------------------")
            zeros = "".join("0" for i in range(4 - len(str(self.id))))
            self.code = f"GLC-I/O-Item{zeros}{self.id}"
            self.save()
            print("Level 1765 model <-------------------")
            
            if self.purpose == "Income":
                print("Income ACTION")
                income_db( self.created_by, self.income_outcome, self.total_amount, self.issuer, self.reciever, self.state, self.comments )
            
            if self.purpose == "Outcome":
                print("Outcome ACTION")
                outcome_db( self.created_by, self.income_outcome, self.total_amount, self.issuer, self.reciever, self.state, self.comments )

        else:
            if str(self.created_at)[:19] != str(datetime.now(timezone.utc))[:19]:
                print("1779 INC/OUT Update Action")
                action = f"updated income_outcome item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)
            else:
                print("1783 Income-Outcome Item Create Action")
                action = f"added new Income-Outcome item with code - '{self.created_by.first_name}'"
                add_user_activity(self.created_by, action=action)                        
            super().save(*args, **kwargs)



    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted Income-Outcome item - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.income_outcome.name} - {self.code}"


post_save.connect(update_income_outcome, sender=IncomeOutcomeItem)


class IncomeDb(models.Model):
    person = models.CharField(max_length=50, unique=False)
    income_outcome = models.CharField(max_length=50, unique=False)
    total_amount = models.PositiveIntegerField(unique=False)
    issuer = models.CharField(max_length=50, unique=False)
    reciever = models.CharField(max_length=50, unique=False)
    state = models.CharField(max_length=50, unique=False)
    reason = models.CharField(max_length=250, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.person} Recieved {self.income_outcome} on {self.created_at}"


class OutcomeDb(models.Model):
    person = models.CharField(max_length=50, unique=False)
    income_outcome = models.CharField(max_length=50, unique=False)
    total_amount = models.PositiveIntegerField(unique=False)
    issuer = models.CharField(max_length=50, unique=False)
    reciever = models.CharField(max_length=50, unique=False)
    state = models.CharField(max_length=50, unique=False)
    reason = models.CharField(max_length=250, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.person} Gives {self.income_outcome} on {self.created_at}"

# ================================================================================
