class Product:
    def __init__(
        self, id: str, name: str, price: str, tax_price: str, arrival: str, url: str
    ) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.tax_price = tax_price
        self.arrival = arrival
        self.url = url


class ProductDetail:
    def __init__(
        self, product: Product, category: str, description: str, image_url: str
    ) -> None:
        self.product = product
        self.category = category
        self.description = description
        self.image_url = image_url

    def to_list(self):
        return [
            self.product.id,
            self.product.name,
            self.category,
            self.description,
            self.product.price,
            self.product.tax_price,
            self.product.arrival,
            self.product.url,
        ]
