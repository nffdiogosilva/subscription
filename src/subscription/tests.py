from datetime import date
from decimal import Decimal
from unittest import mock, TestCase

from .exceptions import CustomerAddWebsitePermissionDenied
from .models import Customer, Plan, Website


class CustomerTestCase(TestCase):
    def setUp(self):
        self.customer = Customer('foo', 'bar', 'foo@bar.com')
        self.default_plan = Plan('Single', 49.0, 'single')
        self.old_plan = Plan('Plus', 99.0, 'plus')
        self.new_plan = Plan('Infinite', 249.0, 'infinite')

    def test_customer_can_subscribe_plan(self):
        """Test a customer is eligible to subscribe to a plan"""

        # First assert that the current customer doesn't have any plan associated with it.
        self.assertIsNone(self.customer.subscription)

        subscribed_plan = self.customer.subscribe_plan(self.default_plan)
        # Assert that the created plan is the same as the subscribed plan
        self.assertEqual(self.default_plan, subscribed_plan)

        # Assert that the subscribed plan is the same as the plan associated with the customer
        self.assertEqual(self.customer.subscription, subscribed_plan)

    def test_customer_can_change_plan(self):
        """Test a customer is eligible to change between plans"""

        # Trying to change a plan to a customer that doesn't yet have a plan should raise an exception
        with self.assertRaises(ValueError):
            self.customer.change_plan(self.new_plan)

        # Add a plan to a user
        self.customer.subscribe_plan(self.old_plan)
        self.assertEqual(self.customer.subscription, self.old_plan)

        # Trying to change to the same plan should raise an exception
        with self.assertRaises(ValueError):
            self.customer.change_plan(self.old_plan)

        # Assert, at last, that a customer can change a plan to a new one
        self.assertTrue(self.customer.change_plan(self.new_plan))
        self.assertEqual(self.customer.subscription, self.new_plan)

    #def test_customer_renewal_date_updates_when_plan_updates(self):
    #    pass

    def test_customer_renewal_date_has_one_year_time_value(self):
        """Test that the subscription renewal date has a one year timestamp"""

        # assert different years (test from 2000 until 2020)
        years = range(1999, 2021)
        today = date.today()
        for year in years:
            # For more information about mocking a date object,
            # please read: https://docs.python.org/3/library/unittest.mock-examples.html#partial-mocking
            with mock.patch('subscription.models.date') as mock_date:
                mock_date.today.return_value = date(year, today.month, today.day)
                mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

                # Check, that the user has not yet a subscription or a renewal_date
                self.assertIsNone(self.customer.subscription)
                self.assertIsNone(self.customer.sub_renewal_date)
                self.customer.subscribe_plan(self.default_plan)

                expected_renewal_date = date(year + 1, today.month, today.day)
                self.assertEqual(self.customer.sub_renewal_date, expected_renewal_date)

                # reset customer subscription and subscription renewal_date for next test
                self.customer.remove_subscription()

    # TODO: test what happens when the renewal date is surpassed (the subscription should be canceled)

    def test_customer_website_crud_operations(self):
        """Test Website object crud operations, made by Customer object"""
        customer_with_plan = Customer('foo', 'bar', 'foo@bar.com', Plan('Single', 49.0, 'single'))
        # import pdb ; pdb.set_trace()
        website = Website('https://example.com')
        #website = mixer.blend(Website, customer=None)

        # Adding operation
        customer_with_plan.websites.add(website)
        # Assert that the website now is in the customer list websites
        self.assertTrue(website in customer_with_plan.websites.all())
        # Assert also that the website has a reference to the same customer
        self.assertEqual(website.customer, customer_with_plan)

        # Update operation
        website_old_url = website.url
        customer_with_plan.websites.update(website, url='https://foo.bar')
        self.assertNotEqual(website_old_url, customer_with_plan.websites.get(website).url)

        # Remove operation
        customer_with_plan.websites.remove(website)
        self.assertFalse(website in customer_with_plan.websites.all())
        self.assertIsNone(website.customer)


class PlanTestCase(TestCase):
    def setUp(self):
       self.customer = Customer('foo', 'bar', 'foo@bar.com')
    
       self.single_plan = Plan('Single', 49.0, 'single')
       self.plus_plan = Plan('Plus', 99.0, 'plus')
       self.infinite_plan = Plan('Infinite', 249.0, 'infinite')

       self.website1 = Website('https://foo.bar', customer=None)
       self.website2 = Website('https://foobar.bar', customer=None)
       self.website3 = Website('https://bar.foo', customer=None)
       self.website4 = Website('https://bar.foo', customer=None)

    def test_total_allowed_based_on_plan(self):
        """Test that the total websites allowed attribute is always based on the plan type, by default"""
        self.assertEqual(self.single_plan.total_websites_allowed, 1)
        self.assertEqual(self.plus_plan.total_websites_allowed, 3)
        self.assertEqual(self.infinite_plan.total_websites_allowed, 0)

    # TODO: test also that the plan type is only one of those three (or create a Plan_type Model, this way you can add different plans in the future)
    def test_plan_type_single_allow_only_one_website(self):
        """Test that the plan with type single can only have one website"""
        self.customer.subscribe_plan(self.single_plan)
        
        # Allows adding one website, with no issue.
        self.customer.websites.add(self.website1)
        self.assertEqual(self.customer.websites.count(), 1)
        
        # The 2nd one is expected to raise an Exception
        with self.assertRaises(CustomerAddWebsitePermissionDenied):
            self.customer.websites.add(self.website2)

    def test_plan_type_plus_allow_3_websites(self):
        """Test that the plan with type plus can only have max 3 websites"""
        self.customer.subscribe_plan(self.plus_plan)
        
        # Allows adding, with no issue, 3 websites.
        self.customer.websites.add(self.website1, self.website2, self.website3)
        self.assertEqual(self.customer.websites.count(), 3)
        
        # The 4th one is expected to raise an Exception
        with self.assertRaises(CustomerAddWebsitePermissionDenied):
            self.customer.websites.add(self.website4)

    def test_plan_type_infinite_allow_unlimited_websites(self):
        """Test that the plan with type infinite can have multiple websites"""

        self.customer.subscribe_plan(self.infinite_plan)
        # Can change this value to tests if you can add even more websites
        TOTAL_WEBSITES = 100000 # it stresses with one million objects....An iterator would be better
        websites_to_test = []
        for i in range(0, TOTAL_WEBSITES):
            # TODO: TEST that if a customer is initialized on the website site constructor, than it needs to check the customer relantionship
            websites_to_test.append(Website('https://foo{}.bar'.format(i), customer=None))
        
        # Adding 100 websites, with no issue.
        self.customer.websites.add(*websites_to_test)
        self.assertEqual(self.customer.websites.count(), TOTAL_WEBSITES)
