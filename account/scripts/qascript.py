from account.models import User
from order.models import Cart , CartItem , Order , OrderItem
from product.models import Product 
from vendor.models import Vendor , VendorProduct


def run():
    print('script running')


    # Get all customers (is_customer=True).
    # customers = User.objects.filter(is_customer=True)
    # print(customers)


    # Retrieve all products.
    

    # List all vendor products for a given vendor.

    # Find all carts created after a specific date.

    # Get the cart for a specific user.

    # List all items in a given cart.

    # Get all orders for a specific user.

    # Retrieve all order items related to a given order.

    # Find all products that are out of stock.

    # Get a user’s email from their cart.

    # Retrieve all orders with status “Pending”.

    # Get a list of all vendor names.

    # Find all vendor products with more than 10% discount.

    # List all products offered by a specific vendor.

    # Find all users located in a specific city.

    # Retrieve a product by name.

    # Get the price of a specific vendor's product.

    # Check if a specific user has a cart.

    # List all users who have placed at least one order.

    # Count how many products each vendor is selling.

    # Get the total number of products.

    # Count the number of cart items in a cart.

    # Check if a specific product is in any vendor’s catalog.

    # Get all users who are vendors and not customers.

    # Retrieve all orders created within the last 7 days.

    # Find all vendor products for a product named "Laptop".

    # Retrieve all cart items where quantity is greater than 2.

    # List all orders with total_price > 1000.

    # Annotate users with their number of orders.

    # Annotate each vendor with their number of products.

    # Get the average price of products sold by each vendor.

    # Get the total revenue from all orders.

    # For each order, list its total price and number of items.

    # For each cart, list the total quantity of items.

    # Find orders that include a product named “iPhone”.

    # Retrieve all orders containing items with more than 10% discount.

    # List vendors who sell more than one product.

    # Retrieve all carts that have more than 3 items.

    # Get all vendor products ordered at least once.

    # Find all vendor products not ordered yet.

    # List products offered by more than one vendor.

    # Get all orders with at least one item quantity > 5.

    # Retrieve the user who placed the highest number of orders.

    # For each vendor, show the minimum and maximum product price.

    # Retrieve all products sold at a discounted price.

    # Calculate the discounted price of each vendor product.

    # Annotate each product with the total quantity sold.

    # Find users who have not placed any orders.

    # Get the latest order for each user.

    # Retrieve all users who have more than one cart item.

    # Find the total quantity of each product sold.

    # Get all orders placed by users in a specific location.

    # Find all products that have never been added to a cart.

    # List all orders that contain a product with zero stock.

    # Retrieve all vendor products with a price lower than the product base price.

    # Get all users who added the same product multiple times in their cart.

    # Find the average discounted price across all vendor products.

    # List all products with more than 2 vendor listings.

    # Create a queryset to find top 5 products by quantity sold.

    # Get top 3 vendors by revenue (based on order items).

    # Annotate each order with the number of unique products.

    # Find orders where the total quantity of items is more than 10.

    # Use F() expressions to increase price of all vendor products by 5%.

    # Use F() expressions to find vendor products where vendor price < product price.

    # Use Q() to find users who are either vendors or located in "New York".

    # Use annotate() and filter() to find users with more than 3 orders.

    # Get all vendor products where discount is between 10% and 50%.

    # Annotate each user with their total order value.

    # Calculate revenue per vendor.

    # Use Subquery to get the latest order of each user.

    # Use OuterRef to get the first cart item per cart.

    # Filter carts where at least one item is from a specific vendor.

    # List all order items where the original product price > price_at_purchase.

    # Get all vendors who have products in user carts.

    # Filter users who have ordered products from more than one vendor.

    # Annotate each cart with the total value using .annotate() and F().

    # Filter out orders that contain a specific product using exclude().

    # List vendors who have never had their products ordered.

    # Find the most common product in all carts.

    # Find users who added the same product to cart and ordered it.

    # Annotate each product with number of vendors offering it.

    # Create a queryset to find abandoned carts (carts with items but no orders).

    # Annotate vendor products with total quantity sold.

    # List orders where all items come from a single vendor.

    # Group and count orders by their status.

    # Use Case and When to annotate order status groups (e.g., is_pending).

    # Annotate vendor with their average discount offered.

    # Use a Subquery to annotate products with their lowest vendor price.

    # Prefetch all vendor products and their orders for a specific vendor.

    # Prefetch orders and related order items efficiently.

    # Optimize cart detail view with select_related and prefetch_related.

    # Calculate total cart value in ORM using annotate() and Sum.

    # Use F() to compare fields in VendorProduct (e.g., discount vs. price).

    # Use Exists to find users who have at least one order.

    # Use Exists to find products in at least one cart.

    # Create a report of vendors with the number of orders containing their products.

    # Annotate each order item with savings (product.price - price_at_purchase).

    # Use conditional expressions to mark order items as “Discounted” or “Full Price”.




