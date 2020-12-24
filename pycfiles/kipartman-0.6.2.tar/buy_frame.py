# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/buy_frame.py
# Compiled at: 2018-07-16 12:07:24
from dialogs.dialog_buy import DialogBuy
from frames.order_options_dialog import OrderOptionsDialog
from currency.currency import Currency
from configuration import Configuration
import rest, helper.tree
from basket.basket import Basket
import os
from frames.edit_wish_frame import EditWishFrame
from helper.exception import print_stack
import wx
from bom.bom import Bom
configuration = Configuration()
currency = Currency()
view_all = True
wish_parts = []

class DataModelBomProduct(helper.tree.TreeItem):

    def __init__(self, bom, quantity):
        super(DataModelBomProduct, self).__init__()
        self.bom = bom
        self.quantity = quantity

    def GetValue(self, col):
        vMap = {0: self.bom.filename, 
           1: str(self.quantity)}
        return vMap[col]

    def GetAttr(self, col, attr):
        if os.path.isfile(self.bom.filename) == False:
            attr.SetColour('red')
            return True
        return False


class DataModelBomPart(helper.tree.TreeItem):

    def __init__(self, bom_products, bom_part):
        super(DataModelBomPart, self).__init__()
        self.bom_products = bom_products
        self.bom_part = bom_part
        self.build_equivalent_parts()

    def build_equivalent_parts(self):
        self.equivalent_parts = []
        if self.bom_part.childs is None:
            return
        else:
            to_add = []
            added = {}
            for child in self.bom_part.childs:
                to_add.append(child)

            for child in to_add:
                if added.has_key(child.id) == False:
                    self.equivalent_parts.append(child)
                    added[child.id] = child
                    if child.childs:
                        for c in child.childs:
                            to_add.append(c)

            return

    def is_equivalent(self, part):
        to_explore = []
        if self.bom_part.childs is None:
            return False
        else:
            for child in self.bom_part.childs:
                to_explore.append(child)

            while len(to_explore) > 0:
                child = to_explore[0]
                if child.id == part.id:
                    return True
                to_explore.remove(child)
                if child.childs:
                    for c in child.childs:
                        to_explore.append(c)

            return False

    def stock(self):
        stock = 0
        for storage in self.bom_part.storages:
            stock = stock + storage.quantity

        for equivalent_part in self.equivalent_parts:
            for storage in equivalent_part.storages:
                stock = stock + storage.quantity

        return stock

    def provisioning(self):
        global wish_parts
        provisioning = 0
        for partobj in wish_parts:
            if partobj.part.id == self.bom_part.id or self.is_equivalent(partobj.part):
                provisioning = provisioning + partobj.buy_items(partobj.matching_offer())

        return provisioning

    def num_components(self):
        num_components = 0
        for bom_product in self.bom_products:
            num_components = num_components + bom_product.bom.NumComponents(self.bom_part)

        return num_components

    def needed(self):
        needed = 0
        for bom_product in self.bom_products:
            needed = needed + bom_product.quantity * bom_product.bom.NumComponents(self.bom_part)

        needed = needed - self.stock()
        if needed < 0:
            needed = 0
        return needed

    def GetValue(self, col):
        vMap = {0: str(self.bom_part.id), 
           1: self.bom_part.name, 
           2: str(self.num_components()), 
           3: str(self.needed()), 
           4: str(int(self.stock())), 
           5: str(int(self.provisioning())), 
           6: self.bom_part.description, 
           7: self.bom_part.comment}
        return vMap[col]

    def GetAttr(self, col, attr):
        if col == 5:
            if self.provisioning() < self.needed():
                attr.SetColour('red')
                attr.Bold = True
            else:
                attr.SetColour('green')
            return True
        return False


class TreeManagerBomParts(helper.tree.TreeManager):

    def __init__(self, tree_view):
        super(TreeManagerBomParts, self).__init__(tree_view)

    def FindBomPart(self, bom_part_id):
        for data in self.data:
            if data.bom_part.id == bom_part_id:
                return data

        return

    def AppendBomPart(self, bom_product, bom_part):
        bom_partobj = self.FindBomPart(bom_part.id)
        if bom_partobj is None:
            bom_partobj = DataModelBomPart([bom_product], bom_part)
            self.AppendItem(None, bom_partobj)
        else:
            bom_partobj.bom_products.append(bom_product)
            self.UpdateItem(bom_partobj)
        return


class DataModelEquivalentPart(helper.tree.TreeItem):

    def __init__(self, equivalent_part):
        super(DataModelEquivalentPart, self).__init__()
        self.equivalent_part = equivalent_part

    def stock(self):
        stock = 0
        for storage in self.equivalent_part.storages:
            stock = stock + storage.quantity

        return stock

    def GetValue(self, col):
        vMap = {0: str(self.equivalent_part.id), 
           1: self.equivalent_part.name, 
           2: str(self.stock()), 
           3: self.equivalent_part.description, 
           4: self.equivalent_part.comment}
        return vMap[col]


class DataModelEquivalentPartContainer(helper.tree.TreeContainerItem):

    def __init__(self, part):
        super(DataModelEquivalentPartContainer, self).__init__()
        self.part = part

    def GetValue(self, col):
        if col == 0:
            return self.part.name
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col == 0:
            attr.Bold = True
            return True
        return False


class DataModelDistributorContainer(helper.tree.TreeContainerItem):

    def __init__(self, distributor):
        super(DataModelDistributorContainer, self).__init__()
        self.distributor = distributor

    def GetValue(self, col):
        if col == 0:
            return self.distributor.name
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col == 0:
            attr.Bold = True
            return True
        return False


class DataModelOffer(helper.tree.TreeItem):

    def __init__(self, offer, bom_partobj):
        super(DataModelOffer, self).__init__()
        self.offer = offer
        self.bom_partobj = bom_partobj

    def item_price(self):
        return self.converted_unit_price()[0] * self.offer.quantity

    def converted_unit_price(self):
        res = [
         self.offer.unit_price, self.offer.currency]
        try:
            return [
             currency.convert(self.offer.unit_price, self.offer.currency, configuration.base_currency), configuration.base_currency]
        except:
            print_stack()
            return res

    def buy_packages(self):
        buy_packages = int(self.bom_partobj.needed() / self.offer.packaging_unit)
        if divmod(self.bom_partobj.needed(), self.offer.packaging_unit)[1] > 0:
            buy_packages = buy_packages + 1
        if buy_packages * self.offer.packaging_unit < self.offer.quantity:
            buy_packages = self.offer.quantity / self.offer.packaging_unit
        return buy_packages

    def buy_items(self):
        return self.buy_packages() * self.offer.packaging_unit

    def buy_price(self):
        return self.buy_items() * self.converted_unit_price()[0]

    def GetValue(self, col):
        converted_unit_price = self.converted_unit_price()
        vMap = {0: str(int(self.buy_items())), 
           1: str(self.buy_price()), 
           2: str(int(self.offer.packaging_unit)), 
           3: str(int(self.offer.quantity)), 
           4: str(self.item_price()), 
           5: str(converted_unit_price[0]), 
           6: converted_unit_price[1], 
           7: self.offer.sku}
        return vMap[col]


class DataModelWishPart(helper.tree.TreeItem):

    def __init__(self, part, distributor, sku, quantity):
        super(DataModelWishPart, self).__init__()
        self.part = part
        self.distributor = distributor
        self.quantity = quantity
        self.sku = sku

    def converted_unit_price(self, offer):
        res = [
         offer.unit_price, offer.currency]
        try:
            return [
             currency.convert(offer.unit_price, offer.currency, configuration.base_currency), configuration.base_currency]
        except:
            print_stack()
            return res

    def buy_packages(self, offer):
        quantity = self.quantity
        if quantity < offer.packaging_unit:
            quantity = offer.packaging_unit
        if quantity < offer.quantity:
            quantity = offer.quantity
        buy_packages = int(quantity / offer.packaging_unit)
        if divmod(quantity, offer.packaging_unit)[1] > 0:
            buy_packages = buy_packages + 1
        return buy_packages

    def buy_items(self, offer):
        return self.buy_packages(offer) * offer.packaging_unit

    def buy_price(self, offer):
        return self.buy_items(offer) * self.converted_unit_price(offer)[0]

    def matching_offer(self):
        matching_offer = None
        for offer in self.distributor.offers:
            if offer.sku == self.sku:
                if matching_offer is None:
                    matching_offer = offer
                if self.buy_price(offer) < self.buy_price(matching_offer) and self.buy_items(offer) >= self.quantity:
                    matching_offer = offer

        return matching_offer

    def GetValue(self, col):
        matching_offer = self.matching_offer()
        vMap = {0: self.part.name, 
           1: self.distributor.name, 
           2: self.sku, 
           3: str(matching_offer.packaging_unit), 
           4: str(int(self.buy_items(matching_offer))), 
           5: str(self.buy_price(matching_offer)), 
           6: str(self.converted_unit_price(matching_offer)[1]), 
           7: self.part.description}
        return vMap[col]


class TreeManagerDistributors(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerDistributors, self).__init__(tree_view, *args, **kwargs)


class BuyFrame(DialogBuy):

    def __init__(self, parent):
        super(BuyFrame, self).__init__(parent)
        self.tree_boms_manager = helper.tree.TreeManager(self.tree_boms, context_menu=self.menu_boms)
        self.tree_boms_manager.AddTextColumn('Path')
        self.tree_boms_manager.AddTextColumn('Production count')
        self.tree_boms_manager.OnSelectionChanged = self.onTreeBomsSelectionChanged
        self.tree_bom_parts_manager = TreeManagerBomParts(self.tree_bom_parts)
        self.tree_bom_parts_manager.AddIntegerColumn('Id')
        self.tree_bom_parts_manager.AddTextColumn('Name')
        self.tree_bom_parts_manager.AddIntegerColumn('Components')
        self.tree_bom_parts_manager.AddIntegerColumn('Needed')
        self.tree_bom_parts_manager.AddIntegerColumn('Stock')
        self.tree_bom_parts_manager.AddIntegerColumn('Provisioning')
        self.tree_bom_parts_manager.AddTextColumn('Description')
        self.tree_bom_parts_manager.AddTextColumn('Comment')
        self.tree_equivalent_parts_manager = helper.tree.TreeManager(self.tree_part_equivalents)
        self.tree_equivalent_parts_manager.AddIntegerColumn('Id')
        self.tree_equivalent_parts_manager.AddTextColumn('Name')
        self.tree_equivalent_parts_manager.AddIntegerColumn('Stock')
        self.tree_equivalent_parts_manager.AddTextColumn('Description')
        self.tree_equivalent_parts_manager.AddTextColumn('Comment')
        self.tree_distributors_manager = TreeManagerDistributors(self.tree_distributors, context_menu=self.menu_prices)
        self.tree_distributors_manager.AddIntegerColumn('Amount To Buy')
        self.tree_distributors_manager.AddFloatColumn('Buy Price')
        self.tree_distributors_manager.AddIntegerColumn('Packaging Unit')
        self.tree_distributors_manager.AddIntegerColumn('Quantity')
        self.tree_distributors_manager.AddFloatColumn('Price')
        self.tree_distributors_manager.AddFloatColumn('Price per Item')
        self.tree_distributors_manager.AddTextColumn('Currency')
        self.tree_distributors_manager.AddTextColumn('SKU')
        self.tree_wish_parts_manager = helper.tree.TreeManager(self.tree_wish_parts)
        self.tree_wish_parts_manager.AddTextColumn('Part')
        self.tree_wish_parts_manager.AddTextColumn('Distributor')
        self.tree_wish_parts_manager.AddTextColumn('SKU')
        self.tree_wish_parts_manager.AddIntegerColumn('Packaging Unit')
        self.tree_wish_parts_manager.AddFloatColumn('Amount')
        self.tree_wish_parts_manager.AddFloatColumn('Buy Price')
        self.tree_wish_parts_manager.AddTextColumn('Currency')
        self.tree_wish_parts_manager.AddTextColumn('Description')
        self.basket = Basket()
        self.update_state()

    def load(self):
        self.loadBoms()
        self.loadBomParts()
        self.loadPartEquivalents()
        self.loadDistributors()
        self.update_state()

    def refresh(self):
        self.refreshBomParts()

    def update_state(self):
        if self.basket is None:
            self.menu_basket_save.Enable(False)
            self.menu_basket_save_as.Enable(False)
        else:
            self.menu_basket_save.Enable(True)
            self.menu_basket_save_as.Enable(True)
        item = self.tree_boms.GetSelection()
        if item.IsOk():
            self.spin_quantity.Enable(True)
            self.menu_boms_remove.Enable(True)
        else:
            self.spin_quantity.Enable(False)
            self.menu_boms_remove.Enable(False)
        return

    def refreshBomParts(self):
        self.update_state()
        for data in self.tree_bom_parts_manager.data:
            self.tree_bom_parts_manager.UpdateItem(data)

    def loadBoms(self):
        self.tree_boms_manager.ClearItems()
        for bom_quantity in self.basket.boms:
            bom = Bom()
            bom.LoadFile(self.basket.boms[bom_quantity].path)
            quantity = self.basket.boms[bom_quantity].quantity
            self.tree_boms_manager.AppendItem(None, DataModelBomProduct(bom, quantity))

        return

    def loadBomParts(self):
        self.tree_bom_parts_manager.ClearItems()
        for bom_file in self.basket.boms:
            bom_product = self.basket.boms[bom_file]
            try:
                bom_product.load()
            except Exception as e:
                print_stack()
                print format(e)

            for bom_part in bom_product.bom.Parts():
                full_part = rest.api.find_part(bom_part.id, with_childs=True, with_storages=True)
                self.tree_bom_parts_manager.AppendBomPart(bom_product, full_part)

    def loadPartEquivalents(self):
        self.tree_equivalent_parts_manager.ClearItems()
        item = self.tree_bom_parts.GetSelection()
        part = None
        if item.IsOk() == False:
            return
        else:
            part = self.tree_bom_parts_manager.ItemToObject(item).bom_part
            part = rest.api.find_part(part.id, with_childs=True, with_storages=True)
            if part.childs is None:
                return
            to_add = []
            added = {}
            for child in part.childs:
                to_add.append(child)

            for child in to_add:
                if added.has_key(child.id) == False:
                    self.tree_equivalent_parts_manager.AppendItem(None, DataModelEquivalentPart(child))
                    added[child.id] = child
                    if child.childs:
                        for c in child.childs:
                            to_add.append(c)

            self.tree_part_equivalents.SelectAll()
            return

    def loadWhishParts(self):
        pass

    def loadTotalPrice(self):
        total = 0
        for data in self.tree_wish_parts_manager.data:
            total = total + data.buy_price(data.matching_offer())

        self.text_total_price.SetValue(str(total))
        self.static_total_price.SetLabel(configuration.base_currency)

    def loadDistributors(self):
        global view_all
        parts = []
        self.tree_distributors_manager.ClearItems()
        item = self.tree_bom_parts.GetSelection()
        if item.IsOk() == False:
            return
        else:
            bom_part = self.tree_bom_parts_manager.ItemToObject(item).bom_part
            bom_part = rest.api.find_part(bom_part.id, with_distributors=True, with_storages=True)
            parts.append(bom_part)
            for item in self.tree_part_equivalents.GetSelections():
                if item.IsOk():
                    equivalent_part = self.tree_equivalent_parts_manager.ItemToObject(item).equivalent_part
                    equivalent_part = rest.api.find_part(equivalent_part.id, with_distributors=True, with_storages=True)
                    parts.append(equivalent_part)

            self.tree_distributors_manager.ClearItems()
            for part in parts:
                partobj = DataModelEquivalentPartContainer(part)
                self.tree_distributors_manager.AppendItem(None, partobj)
                for distributor in part.distributors:
                    if distributor.allowed:
                        distributorobj = DataModelDistributorContainer(distributor)
                        self.tree_distributors_manager.AppendItem(partobj, distributorobj)
                        if view_all:
                            self.loadAllOffers(bom_part, distributorobj)
                        else:
                            self.loadBestOffers(bom_part, distributorobj)

            return

    def loadAllOffers(self, bom_part, distributorobj):
        for offer in distributorobj.distributor.offers:
            offerobj = DataModelOffer(offer, self.tree_bom_parts_manager.FindBomPart(bom_part.id))
            self.tree_distributors_manager.AppendItem(distributorobj, offerobj)

    def loadBestOffers(self, bom_part, distributorobj):
        bom_partobj = self.tree_bom_parts_manager.FindBomPart(bom_part.id)
        quantity = bom_partobj.needed()
        best_offers = {}
        for offer in distributorobj.distributor.offers:
            if best_offers.has_key(offer.sku) == False:
                best_offers[offer.sku] = offer
            offerobj = DataModelOffer(offer, bom_partobj)
            best_offerobj = DataModelOffer(best_offers[offer.sku], bom_partobj)
            if offer.quantity <= quantity and offerobj.buy_price() < best_offerobj.buy_price():
                best_offers[offer.sku] = offer

        for sku in best_offers:
            self.tree_distributors_manager.AppendItem(distributorobj, DataModelOffer(best_offers[sku], bom_partobj))

    def needed_bom_parts(self):
        parts = []
        print 'Needed bom parts: '
        for bom_part in self.tree_bom_parts_manager.data:
            if bom_part.provisioning() < bom_part.needed():
                print (
                 '-', bom_part.bom_part.id, 'provisionning:', bom_part.provisioning(), 'needed:', bom_part.needed())
                parts.append(rest.api.find_part(bom_part.bom_part.id, with_distributors=True, with_offers=True, with_childs=True, with_storages=True))

        return parts

    def get_distributor_matching_offers(self, bom_part, equivalent_parts, distributor, quantity):
        sku_best_offer = {}
        for part_id in equivalent_parts:
            part = equivalent_parts[part_id]
            if part.distributors:
                for d in part.distributors:
                    if d.name == distributor.name:
                        for offer in d.offers:
                            offerobj = DataModelOffer(offer, self.tree_bom_parts_manager.FindBomPart(bom_part.id))
                            if sku_best_offer.has_key(offer.sku) == False:
                                sku_best_offer[offer.sku] = [
                                 part, offer]
                            if offer.quantity <= quantity and offerobj.buy_price() < DataModelOffer(sku_best_offer[offer.sku][1], self.tree_bom_parts_manager.FindBomPart(bom_part.id)).buy_price():
                                sku_best_offer[offer.sku] = [
                                 part, offer]

        return sku_best_offer

    def get_distributor_best_offer(self, bom_part, equivalent_parts, distributor, quantity):
        sku_best_offer = self.get_distributor_matching_offers(bom_part, equivalent_parts, distributor, quantity)
        best_offer_part = None
        best_offer_offer = None
        for sku in sku_best_offer:
            if best_offer_offer is None:
                best_offer_part, best_offer_offer = sku_best_offer[sku]
            sku_best_offer_part, sku_best_offer_offer = sku_best_offer[sku]
            if DataModelOffer(sku_best_offer_offer, bom_part).item_price() < DataModelOffer(best_offer_offer, bom_part).item_price():
                best_offer_part, best_offer_offer = sku_best_offer[sku]

        return [
         best_offer_part, best_offer_offer]

    def get_equivalent_parts(self, part):
        parts = {}
        to_add = [
         part]
        while len(to_add) > 0:
            part = rest.api.find_part(to_add.pop().id, with_distributors=True, with_childs=True, with_storages=True)
            if parts.has_key(part.id) == False:
                parts[part.id] = part
            if part.childs:
                for child in part.childs:
                    to_add.append(child)

        return parts

    def add_wishes_best_offers(self, distributors):
        bom_parts = self.needed_bom_parts()
        for bom_part in bom_parts:
            equivalent_parts = self.get_equivalent_parts(bom_part)
            quantity = self.tree_bom_parts_manager.FindBomPart(bom_part.id).needed()
            print ('-', bom_part.name, quantity)
            best_offer = None
            best_part = None
            best_distributor = None
            for distributor in distributors:
                if distributor.allowed:
                    part, distributor_best_offer = self.get_distributor_best_offer(bom_part, equivalent_parts, distributor, quantity)
                    if best_offer is None:
                        best_offer = distributor_best_offer
                        best_part = part
                        best_distributor = distributor
                    if distributor_best_offer:
                        best_offerobj = DataModelOffer(best_offer, self.tree_bom_parts_manager.FindBomPart(bom_part.id))
                        distributor_best_offerobj = DataModelOffer(distributor_best_offer, self.tree_bom_parts_manager.FindBomPart(bom_part.id))
                        if distributor_best_offerobj.buy_price() < best_offerobj.buy_price():
                            best_offer = distributor_best_offer
                            best_part = part
                            best_distributor = distributor

            if best_offer:
                distributor = None
                for d in best_part.distributors:
                    if d.name == best_distributor.name:
                        distributor = d

                if distributor:
                    self.tree_wish_parts_manager.AppendItem(None, DataModelWishPart(best_part, distributor, best_offer.sku, DataModelOffer(best_offer, self.tree_bom_parts_manager.FindBomPart(bom_part.id)).buy_items()))

        self.refresh()
        self.loadTotalPrice()
        return

    def onMenuBasketOpenSelection(self, event):
        if self.basket.saved == False:
            res = wx.MessageDialog(self, '%s modified, save it?' % self.basket.filename, 'File not saved', wx.YES_NO | wx.ICON_QUESTION).ShowModal()
            if res == wx.ID_YES:
                self.onToolSaveBasketClicked(event)
        dlg = wx.FileDialog(self, message='Choose a basket file', defaultDir=os.getcwd(), defaultFile='', wildcard='Kipartman basket (*.basket)|*.basket', style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            self.basket.LoadFile(dlg.GetPath())
            self.load()

    def onMenuBasketSaveSelection(self, event):
        if self.basket.filename is None:
            self.onMenuBasketSaveAsSelection(event)
        else:
            self.basket.Save()
        return

    def onMenuBasketSaveAsSelection(self, event):
        path = os.getcwd()
        dlg = wx.FileDialog(self, message='Save a basket file', defaultDir=path, defaultFile='new', wildcard='Kipartman basket (*.basket)|*.basket', style=wx.FD_SAVE | wx.FD_CHANGE_DIR)
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            try:
                self.basket.ClearWishes()
                for wishobj in self.tree_wish_parts_manager.data:
                    self.basket.AddWish(wishobj.distributor, wishobj.sku, wishobj.quantity, wishobj.converted_unit_price(wishobj.matching_offer()))

                self.basket.SaveFile(filename)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error saving %s' % filename, wx.OK | wx.ICON_ERROR)

    def onMenuBomsAddSelection(self, event):
        dlg = wx.FileDialog(self, message='Choose a bom file', defaultDir=os.getcwd(), defaultFile='', wildcard='Kipartman bom (*.bom)|*.bom', style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            self.basket.AddBom(dlg.GetPath(), 1)
            self.load()

    def onMenuBomsRemoveSelection(self, event):
        item = self.tree_boms.GetSelection()
        if item.IsOk():
            bom_productobj = self.tree_boms_manager.ItemToObject(item)
        else:
            return
        res = wx.MessageDialog(self, "Remove BOM '%s'?" % bom_productobj.bom_quantity.path, 'Remove BOM', wx.YES_NO | wx.ICON_QUESTION).ShowModal()
        if res == wx.ID_YES:
            self.basket.RemoveBom(bom_productobj.bom_quantity.path)
            self.tree_boms_manager.DeleteItem(None, bom_productobj)
            self.load()
        return

    def onSpinQuantityCtrl(self, event):
        item = self.tree_boms.GetSelection()
        if item.IsOk():
            bom_productobj = self.tree_boms_manager.ItemToObject(item)
        else:
            return
        bom_productobj.quantity = self.spin_quantity.GetValue()
        self.basket.boms[bom_productobj.bom.filename].quantity = self.spin_quantity.GetValue()
        self.tree_boms_manager.UpdateItem(bom_productobj)
        self.loadBomParts()
        self.loadDistributors()

    def onTreeBomsSelectionChanged(self, event):
        self.update_state()
        item = self.tree_boms.GetSelection()
        if item.IsOk():
            bom_productobj = self.tree_boms_manager.ItemToObject(item)
        else:
            return
        self.spin_quantity.SetValue(bom_productobj.bom_quantity.quantity)

    def onToolDistributorsViewAllPrices(self, event):
        global view_all
        view_all = not self.tool_distributors_view_all_prices.IsToggled()
        self.loadDistributors()

    def onToolDistributorsCollapseAll(self, event):
        self.tree_distributors_manager.CollapseAll()

    def onToolDistributorsExpandAll(self, event):
        self.tree_distributors_manager.ExpandAll()

    def onMenuItemPriceAddSelection(self, event):
        event.Skip()

    def onMenuItemPricesSelectBestpriceSelection(self, event):
        best_offer = None
        for data in self.tree_distributors_manager.data:
            if isinstance(data, DataModelOffer):
                if best_offer is None:
                    best_offer = data
                if data.buy_price() < best_offer.buy_price():
                    best_offer = data

        self.tree_distributors_manager.Select(best_offer)
        return

    def onMenuItemPricesAutomaticOrderSelection(self, event):
        global wish_parts
        options_dlg = OrderOptionsDialog(self)
        options_dlg.ShowModal()
        options = options_dlg.options
        if options is None:
            return
        else:
            if options['clean']:
                self.tree_wish_parts_manager.ClearItems()
            wish_parts = self.tree_wish_parts_manager.data
            if options['best_distributor']:
                self.add_wishes_best_distributor(options['allowed_distributors'])
            else:
                self.add_wishes_best_offers(options['allowed_distributors'])
            return

    def onTreeBomPartsSelectionChanged(self, event):
        self.loadPartEquivalents()
        self.loadDistributors()