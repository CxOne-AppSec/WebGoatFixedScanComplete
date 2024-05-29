from database.db import get_connection
from .entities.Product import Product
import logging

class ProductModel():
    @classmethod
    def add_product(self,product):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO products (id, nameproduct, price, category, description,image) VALUES (%s,%s,%s,%s,%s,%s) ", 
                    (product.id,product.nameproduct,product.price,product.category,product.description,product.image))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_product_by_id(self,id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                id=tuple(map(str, id.split(', ')))
                cursor.execute(
                 "SELECT id, nameproduct, price, category, description,image FROM products WHERE id=%s",(id))
                row = cursor.fetchone()
                resultset=None
                if row!=None:
                    resultset= Product(row[0],row[1],row[2],row[3],row[4],row[5])
            connection.close()
            return resultset
        except Exception as ex:
            raise Exception(ex)
  
    @classmethod     
    def get_product_by_names(self,name):
        try:
            name=tuple(map(str, name.split(', ')))
            connection = get_connection()
            products=[]
            with connection.cursor() as cursor:
                cursor.execute(
                 "SELECT * FROM products WHERE strpos(LOWER(nameproduct),%s)> 0 OR strpos(UPPER(nameproduct),%s)> 0",(name,name))
                resultset = cursor.fetchall()
                for row in resultset:
                    product = Product(row[0], row[1], row[2], row[3], row[4], row[5])
                    products.append(product)
            connection.close()
            return products
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_products_by_name(self,name):
        try:
            connection = get_connection()
            Products = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT  nameproduct, price, category, description, image FROM products WHERE name=%s",(name))
                resultset = cursor.fetchall()

                for row in resultset:
                    product = Product(None,row[0], row[1], row[2], row[3], row[4])
                    Products.append(product)
            connection.close()
            return Products
        except Exception as ex:
            raise Exception(ex)
            
    @classmethod
    def get_products(self):
        try:
            connection = get_connection()
            Products = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT  id,nameproduct, price, category, description, image FROM products ORDER BY Id ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    product = Product(row[0], row[1], row[2], row[3], row[4], row[5])
                    Products.append(product)
            connection.close()
            return Products
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def update_product(self,product):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE products SET nameproduct=%s, price=%s, category=%s, description=%s,image=%s WHERE id =%s ",(product.nameproduct,product.price,product.category,product.description,product.image,product.id))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def delete_product(self,id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                id=tuple(map(str, id.split(', ')))
                cursor.execute("DELETE FROM products WHERE id =%s", (id))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)

