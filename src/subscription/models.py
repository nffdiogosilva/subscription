from datetime import date, timedelta
from decimal import Decimal

from . import settings
from .utils import get_year_total_days
from .exceptions import CustomerAddWebsitePermissionDenied
from .managers import WebsiteManager


class Customer:
    """A Customer object that can have a subscription and handle websites."""

    def __init__(self, name, password, email, subscription=None, websites=None):
        self.name = name
        self.password = password
        self.email = email
        self.subscription = subscription
        self.sub_renewal_date = self.set_renewal_date()

        self.websites = websites or WebsiteManager(self)

    def __str__(self):
        return 'Customer: {}'.format(self.name)

    def can_add_website(self):
        if not self.subscription:
            raise ValueError('Customer Subscription doesn\'t exist')

        allows_infinite = self.subscription.total_websites_allowed == 0
        return allows_infinite or self.websites.count() + 1 <= self.subscription.total_websites_allowed

    def get_total_websites_allowed(self):
        if self.subscription:
            return self.subscription.total_websites_allowed

    def set_renewal_date(self):
        """Calculates the renewal subscription date based if the user has an active subscription or not"""
        renewal_date = None

        # If there's a subscription and not renewal_date then calculate it now.
        if self.subscription:
            today = date.today()

            sub_ttl_days = getattr(settings, 'SUBSCRIPTION_TTL_DAYS', get_year_total_days(today.year + 1))
            renewal_date = today + timedelta(days=sub_ttl_days)

        return renewal_date

    def subscribe_plan(self, plan):
        """Method responsible of associating a plan to a customer object."""
        if self.subscription:
            raise ValueError('User already subscribed to a plan ({})'.format(self.subscription))

        self.subscription = plan
        self.sub_renewal_date = self.set_renewal_date()

        return self.subscription

    def change_plan(self, new_plan):
        """Method responsible of substituting the customer current subscription with another."""
        if not self.subscription:
            raise ValueError('There\'s no subscription plan to update')
        if self.subscription == new_plan:
            raise ValueError('This plan ({}) is already associated with the customer'.format(new_plan))

        self.subscription = new_plan
        # reset the renewal date since a new plan will be added
        self.sub_renewal_date = self.set_renewal_date()

        return True

    def remove_subscription(self):
        if not self.subscription:
            raise ValueError('No subscription to remove')

        self.subscription = None
        self.sub_renewal_date = None


class Plan:
    """A Plan object that based on the type defines how many websites a customer can manage."""

    # Initialized a tuple, an Immutable object, to make sure that the plan types can't changed from these 3
    PLAN_TYPE_CHOICES = ('single', 'plus', 'infinite')

    def __init__(self, name, price, plan_type='single'):
        self.name = name
        self.price = Decimal(price)
        self.plan_type = plan_type
        self.is_plan_type_valid()
        self.total_websites_allowed = self.get_total_websites_allowed_based_on_type()

    def __str__(self):
        return 'Plan: {}'.format(self.plan_type)

    def get_total_websites_allowed_based_on_type(self):
        total = None

        if self.plan_type == 'single':
            total = 1
        if self.plan_type == 'plus':
            total = 3
        if self.plan_type == 'infinite':
            total = 0

        return total

    # TODO: add test for this method
    def is_plan_type_valid(self, raise_exception=True):
        if not self.plan_type in self.PLAN_TYPE_CHOICES:
            if raise_exception:
                raise ValueError(
                    'The plan type has to be one of these values: {}. Plan inserted: {}'.format(
                        ''.join(self.PLAN_TYPE_CHOICES), self.plan_type
                    )
                )
            return False

        return True


class Website:
    """A Website object with an url and customer attributes"""

    # TODO: test again how I should add the *args and **kwargs
    def __init__(self, url, customer=None):
        self.url = url
        self.customer = customer
        # self.handle_customer_relationship()

    def __str__(self):
        return 'Website: {}'.format(self.url)

    #def handle_customer_relationship(self):
    #    if not self.customer:
    #        return
#
    #    if self.customer and not self.customer.can_add_website():
    #        raise CustomerAddWebsitePermissionDenied(
    #            'Customer can\'t have more websites. Total allowed: {}'.format(
    #                self.customer.get_total_websites_allowed()
    #            )
    #        )
#
    #    self.customer.websites.add(self)
