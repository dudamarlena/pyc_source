# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: vigilancemeteo/vigilance.py
# Compiled at: 2018-03-18 04:50:54
from lxml import etree

class ZoneAlerte:
    """Une classe pour décrir les alertes météo d'un département Français.

    Each zone is defined by:
    - a departement number
    - a list of alert
    - date of the last update
    """
    listeCouleursAlerte = [
     'Vert', 'Jaune', 'Orange', 'Rouge']
    listeTypesAlerte = ['Vent violent', 'Pluie-innodation', 'Orages',
     'Inondation', 'Neige-verglas', 'Canicule',
     'Grand-froid', 'Avalanches', 'Vagues-submersion']

    def __init__(self, departement):
        """Class construcutor."""
        self.departement = self._valideDepartement(departement)
        self.dateMiseAJour = None
        self.listeAlertes = {}
        for type in ZoneAlerte.listeTypesAlerte:
            self.listeAlertes[type] = 'Vert'

        return

    def miseAJourEtat(self):
        """update state of alert in zone."""
        tree = etree.parse('http://vigilance.meteofrance.com/data/NXFR33_LFPW_.xml')
        departement = tree.xpath("/CV/DV[attribute::dep='" + self.departement + "']")
        couleur = int(departement.get('coul'))
        for risque in tree.xpath("/CV/DV[attribute::dep='" + self.departement + "']/risque"):
            type = int(risque.get('val'))
            self._miseAJourAlerte(type, listeCouleursAlerte[couleur])

        self.dateMiseAJour = 'Date'

    def _miseAJourAlerte(self, type, couleur):
        """Add one alert to the list."""
        self.listeAlerte[type] = couleur

    @staticmethod
    def _valideDepartement(departement):
        """Check departement value.

        In source XML departement 92, 93  and 94 doesn't exist.
        Need to use departement 75 instead
        """
        equivalence75 = [
         '92', '93', '94']
        departementValide = departement
        if departement in equivalence75:
            departementValide = '75'
        return departementValide