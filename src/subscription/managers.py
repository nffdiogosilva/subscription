from .exceptions import CustomerAddWebsitePermissionDenied, ObjectDoesNotExist


class WebsiteManager:
    """Class responsible of handling Customer "crud" operations regarding Website object."""

    def __init__(self, customer):
        self.customer = customer
        # TODO: use an iterator (yield) instead of the a list?
        self.queryset = []

    def get(self, obj):
        try:
            position = self.queryset.index(obj)
        except ValueError:
            raise ObjectDoesNotExist('Website doesn\'t exist on the Customer websites list')

        return self.queryset[position]

    def add(self, *args):
        for arg in args:
            if self.customer.can_add_website():
                self.queryset.append(arg)
                arg.customer = self.customer
            else:
                raise CustomerAddWebsitePermissionDenied(
                    'Customer can\'t have more websites. Total allowed: {}'.format(
                        self.customer.get_total_websites_allowed()
                    )
                )

    def update(self, obj, **kwargs):
        for attr_name, value in kwargs.items():
            setattr(obj, attr_name, value)

    def remove(self, obj):
        try:
            self.queryset.remove(obj)
            obj.customer = None
        except ValueError:
            raise ObjectDoesNotExist('Website doesn\'t exist on the Customer websites list')

    def all(self):
        return self.queryset

    def count(self):
        return len(self.queryset)
