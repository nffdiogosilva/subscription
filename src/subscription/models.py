from datetime import date, timedelta
from decimal import Decimal

from . import settings
from .utils import get_year_total_days
from .exceptions import CustomerAddWebsitePermissionDenied
from .managers import WebsiteManager


class Customer:
    """A Customer class that can have a subscription (Plan object), and manage Website instances."""

    def __init__(self, name, password, email, subscription=None, websites=None):
        """
        :param name: Customer's name
        :param password: Customer's password
        :param email: Customer's email
        :param subscription=None: Customer's subscription (a Plan object)
        :param websites=None: Customer Websites Manager. Defaults to WebsiteManager object.
        """
        self.name = name
        self.password = password
        self.email = email

        self.subscription_date = None
        self.subscription = subscription

        self.websites = websites or WebsiteManager(self)

    def __str__(self):
        return 'Customer: {}'.format(self.name)

    @property
    def subscription(self):
        return self._subscription

    @subscription.setter
    def subscription(self, subscription):
        self.subscription_date = None if not subscription else date.today()
        self._subscription = subscription

    @property
    def sub_renewal_date(self):
        """Calculates the renewal subscription date based if the user has an active subscription or not"""
        renewal_date = None

        # If there's a subscription and not renewal_date then calculate it now.
        if self.subscription and self.subscription_date:
            subscription_date = self.subscription_date
            sub_ttl_days = getattr(settings, 'SUBSCRIPTION_TTL_DAYS', get_year_total_days(subscription_date.year + 1))
            renewal_date = subscription_date + timedelta(days=sub_ttl_days)

        return renewal_date

    def can_add_website(self):
        """This method checks if user is allowed to add another website to his list or not."""
        if not self.subscription:
            raise ValueError('Customer Subscription doesn\'t exist')

        allows_infinite = self.subscription.plan_type == 'infinite'
        return allows_infinite or self.websites.count() + 1 <= self.subscription.total_websites_allowed

    def get_total_websites_allowed(self):
        """Shortcut method to access directly the subscription 'total_websites_allowed' property."""
        if self.subscription:
            return self.subscription.total_websites_allowed

    def subscribe_plan(self, plan):
        """Method responsible of setting a plan to a customer object subscription property."""
        if self.subscription:
            raise ValueError('User already subscribed to a plan ({})'.format(self.subscription))

        self.subscription = plan

        return self.subscription

    def change_plan(self, new_plan):
        """Method responsible of substituting the customer current subscription with another."""
        if not self.subscription:
            raise ValueError('There\'s no subscription plan to update')
        if self.subscription == new_plan:
            raise ValueError('This plan ({}) is already associated with the customer'.format(new_plan))

        self.subscription = new_plan
        return True


class Plan:
    """A Plan object that based on the type defines how many websites a customer can manage."""

    # Initialized a tuple, an Immutable object, 
    # to make sure that the plan types can't changed besides these three ('single', 'plus', 'infinite')
    PLAN_TYPE_CHOICES = ('single', 'plus', 'infinite')

    def __init__(self, name, price, plan_type='single', total_websites_allowed=1):
        """
        :param name: Plan's name
        :param price: Plan's price
        :param plan_type='single': Plan's type
        :param total_websites_allowed=1: Plan's property to define how many Website instances can a Customer have
        """
        self.name = name
        self.price = Decimal(price)
        self.plan_type = plan_type
        self.total_websites_allowed = total_websites_allowed

    @property
    def plan_type(self):
        return self._plan_type

    @plan_type.setter
    def plan_type(self, plan_type):
        if not plan_type in self.PLAN_TYPE_CHOICES:
            raise ValueError(
                'The plan type has to be one of these values: {}. Plan inserted: {}'.format(
                    ', '.join(self.PLAN_TYPE_CHOICES), plan_type
                )
            )

        self._plan_type = plan_type

    @property
    def total_websites_allowed(self):
        return self._total_websites_allowed

    @total_websites_allowed.setter
    def total_websites_allowed(self, total_websites_allowed):
        """Setting total_websites_allowed while making sure then plan type rules are respected"""
        if self.plan_type == 'single' and total_websites_allowed > 1:
            raise ValueError('The plan type \'single\' only allows 1 website max')
        if self.plan_type == 'plus' and total_websites_allowed > 3:
            raise ValueError('The plan type \'plus\' only allows 3 websites max')

        self._total_websites_allowed = total_websites_allowed

    def __str__(self):
        return 'Plan: {}'.format(self.plan_type)


class Website:
    """A Website class with an url and customer properties"""

    def __init__(self, url, customer=None):
        """
        :param url: Website's url
        :param customer=None: Website's Customer
        """
        self.url = url
        self.customer = customer

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, customer):
        """Setting a customer, while validanting if he's allowed to have another Website"""
        self._customer = customer

        if not customer:
            return

        if not customer.can_add_website():
            raise CustomerAddWebsitePermissionDenied(
                'Customer can\'t have more websites. Total allowed: {}'.format(customer.get_total_websites_allowed())
            )
        else:
            customer.websites.add(self)

    def __str__(self):
        return 'Website: {}'.format(self.url)
