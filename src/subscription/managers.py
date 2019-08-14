class SubscriptionManager:
    """
    Manager to handle the Customer subscriptions.
    """

    #def get_queryset(self):
    #    """Override get queryset to return only the customers with current subscriptions."""
    #    return super().get_queryset().exclude(subscription=None)

    def subscribe_plan(self, customer, plan):
        """Method responsible of associating a plan to a customer object."""
        if customer.subscription:
            raise ValueError('User already subscribed to a plan ({})'.format(customer.subscription))

        customer.subscription = plan
        customer.save()

        return customer.subscription

    def change_plan(self, customer, new_plan):
        """Method responsible of substituting the customer current subscription with another."""
        if not customer.subscription:
            raise ValueError('There\'s no subscription plan to update')
        if customer.subscription == new_plan:
            raise ValueError('This plan ({}) is already associated with this customer ({})'.format(new_plan, customer))

        # reset the renewal date since a new plan will be added
        customer.sub_renewal_date = None
        customer.subscription = new_plan
        customer.save()

        return True


class WebsiteManager:
    def __init__(self, *args):
        self.queryset = list(args)

    def get(self, obj):
        pass

    def add(self, *args):
        for arg in args:
            self.queryset.append(arg)

    def update(self, obj):
        pass

    def remove(self, obj):
        pass