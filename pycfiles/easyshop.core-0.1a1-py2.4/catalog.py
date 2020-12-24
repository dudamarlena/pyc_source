# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/catalog.py
# Compiled at: 2008-06-20 09:35:25
from zope import schema
from zope.interface import Interface
from zope.interface import Attribute
from zope.app.file.interfaces import IImage
from easyshop.core.config import _

class IFormatter(Interface):
    """Marker interface to mark formatter content objects.
    
    A formatter provides informations of how products of a shop/category/selector
    are displayed. The first formatter which is found is taken. Is no formatter
    is found default values are taken.
    """
    __module__ = __name__


class IFormats(Interface):
    """Provides methods to get an formater resp. formatter infos.
    """
    __module__ = __name__

    def getFormats():
        """Returns the infos of the found formatter as dict.
        """
        pass

    def setFormats(data):
        """Sets format with given data. Data has to be dictionary.
        """
        pass


class IFormatable(Interface):
    """Marker interface to mark objects as formatable.
    """
    __module__ = __name__


class ICategory(IFormatable):
    """Marker interface to mark category content objects. 

    A Category groups arbitrary Products together.
    
    Categories are visible to Customer and mainly used to structure 
    Products. A user of a shop may browse through Products via Categories.
       
    Categories may have sub-categories. 
       
    A product can have more than one category.

    categories may assigned special taxes, shipping prices, discounts and 
    similiar.
    """
    __module__ = __name__


class ICategoryManagement(Interface):
    """Provides methods to manage category content objects.
    """
    __module__ = __name__

    def getCategories():
        """Returns all categories of context as brains.
        """
        pass

    def getTopLevelCategories(self):
        """Returns the top level categories of context. 
        
        Note: The adapter for products returns real objects here (not brains), 
        because of the using of getBRefs which returns real objects. The 
        adapters for shop and categories return brains. This is inconsistent but
        needed (e.g. in the categories portlet) for speed reasons and intended 
        to change soon.
        """
        pass


class ICategoriesContainer(Interface):
    """A marker interface for categories containers.
    """
    __module__ = __name__


class IEasyShopImage(Interface):
    """Marker interface for a  image content objects.
    """
    __module__ = __name__


class IImageConversion(Interface):
    """Provides methods to convert an image. 
    """
    __module__ = __name__

    def convertImage(image):
        """Convert given image.
        """
        pass


class IImageManagement(Interface):
    """Provides methods to manage image content objects.
    """
    __module__ = __name__

    def getMainImage():
        """Return the main image.
        """
        pass

    def getImages():
        """Returns all images.
        """
        pass

    def hasImages():
        """Returns True if at least one image exists.
        """
        pass


class IProduct(Interface):
    """Products are sold in the shop.
    """
    __module__ = __name__
    description = schema.Text(title=_('Description'), description=_('A short description, which is displayed in search results'), default='', required=False)
    articleId = schema.TextLine(title=_('Article Id'), description=_('External unique id of the product'), default='', required=False)
    shortTitle = schema.TextLine(title=_('Short Title'), description=_('Short title of the product, which can be displayed in overviews'), default='', required=False)
    shortText = schema.TextLine(title=_('Short Text'), description=_('A short text of the product, which can be displayed in overviews'), default='', required=False)
    text = schema.TextLine(title=_('Text'), description=_('A text of the product, which is displayed in detailed views'), default='', required=False)
    unlimitedAmount = schema.Bool(title=_('Unlimited Amount'), description=_('If selected, the stock amount of the product is not decreased.'), default=False, required=False)
    stockAmount = schema.Float(title=_('Stock Amount'), description=_('The amount of this product in stock. This number is decreased automatically when the product has been sold.'), default=0.0, required=False)
    weight = schema.Float(title=_('Weight'), description=_('The weight of the product.'), default=0.0, required=False)
    price = schema.Float(title=_('Price'), description=_('The price of the product.'), default=0.0, required=False)
    forSale = schema.Bool(title=_('For Sale'), description=_('If selected the sale price is active and displayed additionally.'), default=False, required=False)
    salePrice = schema.Float(title=_('Sale Price'), description=_('The sale price of the product.'), default=0.0, required=False)


class IProductManagement(Interface):
    """Provides methods to handle product content objects.
    """
    __module__ = __name__

    def getAllProducts():
        """Returns all products (top and sub levels).
        """
        pass

    def getAmountOfProducts():
        """Returns the amount products.
        """
        pass

    def getProducts():
        """Returns top level products.
        """
        pass

    def getTotalAmountOfProducts():
        """Returns the amount of products of all subcategories.
        """
        pass


class IProductsContainer(Interface):
    """Marker interface for product folder content objects.
    """
    __module__ = __name__


class IProductVariant(IProduct):
    """Marker interface to mark product variant content objects.
    """
    __module__ = __name__


class IProductVariantsManagement(Interface):
    """Provides methods to manage product variants.
    """
    __module__ = __name__

    def addVariants(title, properties):
        """Adds a product variant.
        """
        pass

    def deleteVariants(ids):
        """Deletes variants with given ids.
        """
        pass

    def getDefaultVariant():
        """Returns the default product variant.
        """
        pass

    def getVariants():
        """Returns existing product variants.
        """
        pass

    def getSelectedVariant(properties):
        """Returns selected product.
        """
        pass

    def hasVariant(properties):
        """Returns True if a variant with given properties exists.
        """
        pass

    def hasVariants():
        """Returns True if context has at least one variant.
        """
        pass


class IProperty(Interface):
    """A property for various content objects.
    """
    __module__ = __name__


class IPropertyOption(Interface):
    """A property for various content objects.
    """
    __module__ = __name__


class IPropertyManagement(Interface):
    """Provides methods to manage property content objects.
    """
    __module__ = __name__

    def getOptionsForProperty(property_id):
        """Return all options of the given property id.
        """
        pass

    def getPriceForCustomer(property_id, option_name):
        """Returns the customer price of a context's property with given id and
        option name.
        
        The tax for property is the same for its product.
        """
        pass

    def getPriceGross(property_id, option_name):
        """Returns the gross price of a context's property with given id and
        option name.
        """
        pass

    def getPriceNet(property_id, option_name):
        """Returns the net price of a context's property with given id and
        option name.
        
        The tax for property is the same for its product.
        """
        pass

    def getProperties():
        """Returns all properties.
        """
        pass

    def getProperty(id):
        """Returns the property with given title.
        
        Using title, because then a property could be deleted and added
        again. This wouldn't work with id or uid.
        
        This requires, that title per property is unique. This will be done in
        edit view.
        """
        pass

    def getTitlesByIds(property_id, option_id):
        """Returns the titles of property and option with given id.
        """
        pass


class IProductSelector(IFormatable):
    """A marker interface for product selector content objects.
    """
    __module__ = __name__