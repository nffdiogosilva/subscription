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
            if not arg.customer:
                # This attribute (customer) set, if valid, will invoke again this .add method
                arg.customer = self.customer
            else:
                self.queryset.append(arg)

    def update(self, obj, **kwargs):
        for attr_name, value in kwargs.items():
            setattr(obj, attr_name, value)

    def remove(self, obj):
        try:
            obj.customer = None
            self.queryset.remove(obj)
        except ValueError:
            raise ObjectDoesNotExist('Website doesn\'t exist on the Customer websites list')

    def all(self):
        return self.queryset

    def count(self):
        return len(self.queryset)
