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

        # Assert that the subscribed plan is the same as the plan associated with the customer
        self.assertEqual(self.customer.subscription, subscribed_plan)

    def test_customer_can_not_subscribe_plan(self):
        """Tests that a user can not subscribe to a plan if he already subscribed before"""
        
        subscribed_plan = self.customer.subscribe_plan(self.default_plan)
        # Assert that the user has subscribed to a plan
        self.assertEqual(self.customer.subscription, subscribed_plan)

        with self.assertRaises(ValueError):
            self.customer.subscribe_plan(self.new_plan)

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

    # def test_customer_renewal_date_updates_when_plan_updates(self):
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
                self.customer.subscription = None

    def test_customer_website_crud_operations(self):
        """Test Website object crud operations, made by Customer object"""
        customer_with_plan = Customer('foo', 'bar', 'foo@bar.com', Plan('Single', 49.0, 'single'))
        website = Website('https://example.com')

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

    def test_customer_can_not_add_website_if_no_subscription(self):
        # self.customer = Customer('foo', 'bar', 'foo@bar.com')
        self.assertIsNone(self.customer.subscription)

        with self.assertRaises(ValueError):
            self.customer.websites.add(Website('https://foo.bar'))


class PlanTestCase(TestCase):
    def setUp(self):
        self.customer = Customer('foo', 'bar', 'foo@bar.com')

        self.single_plan = Plan('Single', 49.0, 'single', total_websites_allowed=1)
        self.plus_plan = Plan('Plus', 99.0, 'plus', total_websites_allowed=3)
        self.infinite_plan = Plan('Infinite', 249.0, 'infinite')

        self.website1 = Website('https://foo.bar', customer=None)
        self.website2 = Website('https://foobar.bar', customer=None)
        self.website3 = Website('https://bar.foo', customer=None)
        self.website4 = Website('https://bar.foo', customer=None)

    def test_total_allowed_based_on_plan(self):
        """Test that the total websites allowed attribute is always based on the plan type, by default"""
        self.assertEqual(self.single_plan.total_websites_allowed, 1)
        self.assertEqual(self.plus_plan.total_websites_allowed, 3)

    def test_plan_type_value(self):
        """Test that NO plan, with plan type different than 'single', 'plus' and 'infinite', can be initialized"""
        with self.assertRaises(ValueError):
            Plan('Plan1', 99.0, plan_type='foo')
            Plan('Plan1', 99.0, plan_type='bar')
            Plan('Plan1', 99.0, plan_type='foobar')

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
        TOTAL_WEBSITES = 100000  # it stresses with one million objects....An iterator would be better
        websites_to_test = []
        for i in range(0, TOTAL_WEBSITES):
            websites_to_test.append(Website('https://foo{}.bar'.format(i), customer=None))

        self.customer.websites.add(*websites_to_test)
        self.assertEqual(self.customer.websites.count(), TOTAL_WEBSITES)


class WebsiteTestCase(TestCase):
    def setUp(self):
        # Valid customer with no websites associated with.
        self.valid_customer = Customer('foo', 'bar', 'foo@bar.com', Plan('TestPlan', 0, plan_type='single'))

        # Invalid customer because already has a website associated with it one and a plan type 'single',
        # He's not supposed to have more than 1 website
        self.invalid_customer = Customer('bar', 'foo', 'barfoo@.com', Plan('TestPlan', 0, plan_type='single'))
        self.invalid_customer.websites.add(Website('https://foo.bar'))

    def test_website_can_initialize_valid_customer(self):
        """Test that an association is created on both objects, when a Website object is initialized"""
        self.assertEqual(self.valid_customer.websites.count(), 0)
        website = Website('https://bar.foo', self.valid_customer)

        self.assertEqual(self.valid_customer.websites.count(), 1)
        self.assertEqual(website.customer, self.valid_customer)

    def test_website_does_not_initialize_with_invalid_customer(self):
        """Tests that no more relation can be created between Customer and Website, if Customer doesn't have permissions to add more websites"""

        self.assertEqual(self.invalid_customer.websites.count(), 1)

        with self.assertRaises(CustomerAddWebsitePermissionDenied):
            website = Website('https://example.com', self.invalid_customer)
            self.assertNone(website.customer)

        self.assertEqual(self.invalid_customer.websites.count(), 1)
