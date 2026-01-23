import stripe
import helpers.billing
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings

import helpers

user = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUPS = True  # Or False, depending on your requirement

SUBSCRIPTION_PERMISSIONS = [
    ("advanced", "Advanced Perm"),
    ("pro", "Pro Perm"),
    ("basic", "Basic Perm"),
]

class Subscription(models.Model):
    """
    Subscription = Stripe Product
    """
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(
        Permission,
        limit_choices_to={
            "content_type__app_label": "subscriptions",
            "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSIONS],
        },
    )
    stripe_customer_id = models.CharField(max_length=120, blank=True, null=True)
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        permissions = [
            ("advanced", "Advanced Perm"),
            ("pro", "Pro Perm"),
            ("basic", "Basic Perm"),
        ]
    def save(self, *args, **kwargs):
        print("SAVE CALLED")

        super().save(*args, **kwargs)

        if not self.stripe_product_id:
            print("CREATING STRIPE PRODUCT")
            stripe_id = helpers.billing.create_product(
                name=self.name,
                metadata={"subscription_id": self.id},
                raw=False
            )
            print("STRIPE ID:", stripe_id)
            self.stripe_product_id = stripe_id
            super().save(update_fields=["stripe_product_id"])



class SubscriptionPrice(models.Model):
    """
    Subscription Price Plan = Stripe Product
    """
    class IntervalChoices(models.TextChoices):
        MONTHLY = "month", "Monthly"
        YEARLY = "year", "Yearly"
        
        
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=120, blank=True, null=True)
    interval = models.CharField(max_length=50, default=IntervalChoices.MONTHLY, choices=IntervalChoices.choices)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=10.00)
    
    
    @property
    def stripe_currecy(self):
        return "usd"
    
    @property
    def stripe_price(self):
        #Remove Decimal
        return int(self.price * 100)  # in cents
    @property
    def product_stripe_id(self):
        if self.subscription:
            return self.subscription.stripe_product_id
        return None
    
    def save(self, *args, **kwargs):
        if (not self.stripe_customer_id and self.subscription is not None):
            stripe_id = helpers.billing.create_price(
            currency=self.stripe_currecy,
            unit_amount=1000,
            interval=self.interval,
            product=self.product_stripe_id,
            metadata={
                "subscription_plan_price_id": self.id,
            },
            raw=False
            )
            self.stripe_customer_id = stripe_id
        super().save(*args, **kwargs)
        
        
class UserSubscription(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list("id", flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = subs_qs.values_list("groups__id", flat=True)
        subs_groups_set = set(subs_groups)
        #groups_ids = groups.values_list("id", flat=True)
        current_groups = user.groups.all().values_list("id", flat=True)
        groups_ids_set = set(groups_ids)
        current_groups_set = set(current_groups) - subs_groups_set
        final_group_ids = list(groups_ids_set | current_groups_set)
        user.groups.set(final_group_ids)


post_save.connect(user_sub_post_save, sender=UserSubscription)