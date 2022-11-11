import os
from datetime import timedelta

import jwt
from db.product import *
from fastapi import APIRouter, Depends, HTTPException
from models import ProductInput
from passlib.hash import argon2
from starlette.responses import JSONResponse

from .utils import get_current_user, get_current_user_admin

router = APIRouter(tags=["Product"])


@router.get("/all")
def get_all_available_products(token: str = Depends(get_current_user)):
    return db_get_all_products()


@router.post("/")
def add_product(input: ProductInput, token: str = Depends(get_current_user_admin)):
    print("In Add Product")
    return db_add_product(Product.parse_obj(input))


@router.put("")
def update_product_count(input: dict, token: str = Depends(get_current_user_admin)):
    if input["product_id"] in [None, ""]:
        raise HTTPException(400,"Product Id is required")
    product = db_get_product_with_id(input["product_id"])
    if product==None:
        raise HTTPException(400,"Product Not Found")
    any_update = False
    for k,v in input.items():
        p_value = product.__getattribute__(k)
        if type(p_value)!=type(v):
            raise HTTPException(400,"Type mismatch for "+k)
        if p_value!=v:
            product.__setattr__(k,v)
            any_update=True
    if not any_update:
        raise HTTPException(302, "Not Modified")
    else:
        res = db_update_product(product)
        if res[1]!=200:
            raise HTTPException(res[1],res[0])
        else:
            return res[0]


@router.put("/units")
def add_available_units(
    product_id: str, new_units: int, token: str = Depends(get_current_user_admin)
):
    res = db_add_units(product_id, new_units)
    if res[1]!=200:
        raise HTTPException(res[1],res[0])
    else:
        return res[0]


@router.put("/description")
def update_description(
    product_id: str, description: str, token: str = Depends(get_current_user_admin)
):
    res =  db_update_description(product_id, description)
    if res[1]!=200:
        raise HTTPException(res[1],res[0])
    else:
        return res[0]


@router.put("/price")
def update_price(
    product_id: str, new_price: float, token: str = Depends(get_current_user_admin)
):
    res =  db_update_price(product_id, new_price)
    if res[1]!=200:
        raise HTTPException(res[1],res[0])
    else:
        return res[0]
