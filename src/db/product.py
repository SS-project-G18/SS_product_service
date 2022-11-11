from uuid import uuid4

from models import Product

from . import products_db


def db_get_product_with_id(product_id: str):
    res = products_db.find_one({"product_id": product_id})
    if res!=None:
        return Product.parse_obj(res)
    return None

def db_get_all_products():
    res = products_db.find({})
    return [Product.parse_obj(x) for x in res]

def db_add_product(input: Product):
    input.product_id = "p-"+uuid4().__str__()
    while db_get_product_with_id(input.product_id)!=None:
        input.product_id = "p-"+uuid4().__str__()
    products_db.insert_one(input.dict())
    return input.product_id

def db_add_units(product_id: str, new_units: int):
    res = products_db.update_one({"product_id": product_id},{
        "$inc": {
            "available_units": new_units
        }
    })
    if res.matched_count==0:
        return "Not Found", 400
    elif res.matched_count==1 and res.modified_count==0:
        return "Not Modified", 302
    else:
        return "Success", 200
    
def db_update_price(product_id: str, new_price: float):
    res = products_db.update_one({"product_id": product_id},{
        "$set": {
            "price": new_price
        }
    })
    if res.matched_count==0:
        return "Not Found", 400
    elif res.matched_count==1 and res.modified_count==0:
        return "Not Modified", 302
    else:
        return "Success", 200
    

def db_update_description(product_id: str, new_description: str):
    res = products_db.update_one({"product_id": product_id},{
        "$set": {
            "description": new_description
        }
    })
    if res.matched_count==0:
        return "Not Found", 400
    elif res.matched_count==1 and res.modified_count==0:
        return "Not Modified", 302
    else:
        return "Success", 200

def db_update_product(input: Product):
    res = products_db.update_one({"product_id": input.product_id},{
        "$set": {
            "category": input.category,
            "sub_category": input.sub_category,
            "price": input.price,
            "available_units": input.available_units,
            "product_name": input.product_name,
            "description": input.description
        }
    })
    if res.matched_count==0:
        return "Not Found", 400
    elif res.matched_count==1 and res.modified_count==0:
        return "Not Modified", 302
    else:
        return "Success", 200
    