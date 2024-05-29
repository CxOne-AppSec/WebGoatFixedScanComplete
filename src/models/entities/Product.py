class Product():
    def __init__(self, id, nameproduct=None, price=None,category=None,description=None,image=None) -> None:
        self.id = id
        self.nameproduct = nameproduct
        self.price=price
        self.category=category
        self.description=description
        self.image=image
