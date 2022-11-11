from .common import BasicModel


class ProductInput(BasicModel):
    product_name: str = ""
    category: str = ""
    sub_category: str = ""
    price: float = 0.0
    available_units: int = 0
    description: str = ""
    
class Product(ProductInput):
    product_id: str = ""