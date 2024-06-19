import stripe

from config.settings import API_KEY_STRIPE

stripe.api_key = API_KEY_STRIPE


def create_stripe_product(product):
    """Создание продукта в Stripe"""

    return stripe.Product.create(name=product)


def create_stripe_price(price, product):
    """Создание цены в Stripe"""

    # print(price)
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(price * 100),
        product_data={"name": product},
    )


def create_stripe_session(price):
    """Создание сессии в Stripe"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",  # https в документации
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def get_stripe_session_result(session_id):
    """Получение результата оплаты в Stripe"""

    # print(stripe.checkout.Session.retrieve(session_id))
    return stripe.checkout.Session.retrieve(session_id)
