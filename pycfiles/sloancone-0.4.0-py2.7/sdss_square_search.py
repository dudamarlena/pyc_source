# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sloancone/sdss_square_search.py
# Compiled at: 2020-05-06 13:40:52
"""
*A first pass square search of SDSS using the conesearch radius as the diameter of the (on sky) square*

:Author:
    David Young

.. todo::
    
"""
from __future__ import print_function
from builtins import str
from future import standard_library
standard_library.install_aliases()
from builtins import object
import sys, os, re, readline, glob, urllib.request, urllib.parse, urllib.error, string, json
from docopt import docopt
from fundamentals import tools, times
from astrocalc.coords import unit_conversion, separations, translate

class sdss_square_search(object):
    """
    *The worker class for the sdss_square_search module*

    **Key Arguments**

    ``log`` -- logger
    - ``ra`` -- ra in sexigesimal or decimal degrees
    - ``dec`` -- dec in sexigesimal or decimal degrees
    - ``searchRadius`` -- search radius in arcsecs
    

    .. todo::
    """

    def __init__(self, log, ra, dec, searchRadius, galaxyType=False):
        self.log = log
        log.debug("instansiating a new 'sdss_square_search' object")
        self.ra = ra
        self.dec = dec
        self.searchRadius = searchRadius
        self.galaxyType = galaxyType
        self.sdssUrl = 'http://skyserver.sdss3.org/public/en/tools/search/x_sql.aspx'
        converter = unit_conversion(log=log)
        self.ra = float(converter.ra_sexegesimal_to_decimal(ra=self.ra))
        self.dec = float(converter.dec_sexegesimal_to_decimal(dec=self.dec))
        self._calculate_search_limits()
        self._build_sql_query()
        return

    def close(self):
        del self
        return

    def get(self):
        """
        *get the results from the the sdss square search*

        **Return**

        - ``sdss_square_search``
        

        .. todo::
        """
        self.log.debug('starting the ``get`` method')
        self._execute_sql_query()
        self._append_separations_to_results()
        self._generate_sdss_object_name()
        self.log.debug('completed the ``get`` method')
        return self.results

    def _calculate_search_limits(self):
        """
        *calculate search limits for the square search*

        **Key Arguments**

        # -
        

        **Return**

        - None
        

        .. todo::
        """
        self.log.debug('starting the ``_calculate_search_limits`` method')
        self.ra1, self.dec1 = translate(log=self.log, ra=self.ra, dec=self.dec, northArcsec=-self.searchRadius, eastArcsec=-self.searchRadius).get()
        self.ra2, self.dec2 = translate(log=self.log, ra=self.ra, dec=self.dec, northArcsec=self.searchRadius, eastArcsec=self.searchRadius).get()
        self.log.debug('completed the ``_calculate_search_limits`` method')

    def _build_sql_query(self):
        """
        *build sql query for the sdss square search*

        **Key Arguments**

        # -
        

        **Return**

        - None
        

        .. todo::
        """
        self.log.debug('starting the ``_build_sql_query`` method')
        ra1, ra2, dec1, dec2 = (
         self.ra1, self.ra2, self.dec1, self.dec2)
        if self.galaxyType == 'all':
            self.sqlQuery = '\n                SELECT p.objiD, p.ra, p.dec, s.z as specz, s.zerr as specz_err, z.z as photoz, z.zerr as photoz_err, p.type\n                    FROM PhotoObjAll p\n                    LEFT JOIN SpecObjAll AS s ON s.bestobjid = p.objid\n                    LEFT JOIN Photoz AS z ON z.objid = p.objid \n                    WHERE (p.ra between %(ra1)s and %(ra2)s) and (p.dec between %(dec1)s and %(dec2)s) and p.clean = 1 and p.type = 3\n            ' % locals()
        elif self.galaxyType == 'specz':
            self.sqlQuery = '\n                SELECT p.objiD, p.ra, p.dec, s.z as specz, s.zerr as specz_err, p.type\n                    FROM PhotoObjAll p, SpecObjAll s\n                    WHERE (s.bestobjid = p.objid) and (p.ra between %(ra1)s and %(ra2)s) and (p.dec between %(dec1)s and %(dec2)s) and p.type = 3\n            ' % locals()
        elif self.galaxyType == 'photoz':
            self.sqlQuery = '\n                SELECT p.objiD, p.ra, p.dec, z.z as photoz, z.zerr as photoz_err, p.type\n                    FROM PhotoObjAll p, Photoz z\n                    WHERE (z.objid = p.objid) and (p.ra between %(ra1)s and %(ra2)s) and (p.dec between %(dec1)s and %(dec2)s) and p.clean = 1 and p.type = 3\n            ' % locals()
        elif self.galaxyType == False or not self.galaxyType:
            self.sqlQuery = '\n                SELECT p.objiD, p.ra, p.dec, s.z as specz, s.zerr as specz_err, z.z as photoz, z.zerr as photoz_err, p.type\n                    FROM PhotoObjAll p\n                    LEFT JOIN SpecObjAll AS s ON s.bestobjid = p.objid\n                    LEFT JOIN Photoz AS z ON z.objid = p.objid \n                    WHERE (p.ra between %(ra1)s and %(ra2)s) and (p.dec between %(dec1)s and %(dec2)s) and p.clean = 1 and (p.type = 3 or p.type = 6)\n            ' % locals()
        self.sqlQuery = self.sqlQuery.strip()
        self.log.debug('completed the ``_build_sql_query`` method')
        return

    def _execute_sql_query(self):
        """
        *execute sql query using the sdss API*

        **Key Arguments**

        # -
        

        **Return**

        - None
        

        .. todo::
        """
        self.log.debug('starting the ``_execute_sql_query`` method')
        params = urllib.parse.urlencode({'cmd': self.sqlQuery, 'format': 'json'})
        results = urllib.request.urlopen(self.sdssUrl + '?%s' % params)
        ofp = sys.stdout
        results = results.read()
        if str(results).startswith('ERROR'):
            ofp = sys.stderr
            ofp.write(string.rstrip(line) + os.linesep)
        try:
            results = json.loads(results)[0]
        except:
            results = results.replace(': ,', ': "NULL",')
            regex = re.compile('"photoz_err"\\:\\s*(\\n\\s*})')
            newString = regex.sub('"photoz_err": "NULL"\\g<1>', results)
            results = newString
            results = json.loads(results)[0]

        self.results = results['Rows']
        self.log.debug('completed the ``_execute_sql_query`` method')

    def _append_separations_to_results(self):
        """
        *append angular separations to results*

        **Key Arguments**

        # -
        

        **Return**

        - None
        

        .. todo::
        """
        self.log.debug('starting the ``_append_separations_to_results`` method')
        for row in self.results:
            if 'ra' not in row:
                print(row)
                exit(0)
            calculator = separations(log=self.log, ra1=self.ra, dec1=self.dec, ra2=row['ra'], dec2=row['dec'])
            angularSeparation, northSep, eastSep = calculator.get()
            row['separation_arcsec'] = angularSeparation
            row['separation_north_arcsec'] = northSep
            row['separation_east_arcsec'] = eastSep

        self.log.debug('completed the ``_append_separations_to_results`` method')
        return

    def _generate_sdss_object_name(self):
        """
        *generate sdss object names for the results*

        **Key Arguments**

        # -
        

        **Return**

        - None
        

        .. todo::
        """
        self.log.debug('starting the ``_generate_sdss_object_name`` method')
        converter = unit_conversion(log=self.log)
        for row in self.results:
            raSex = converter.ra_decimal_to_sexegesimal(ra=row['ra'], delimiter=':')
            decSex = converter.dec_decimal_to_sexegesimal(dec=row['dec'], delimiter=':')
            raSex = raSex.replace(':', '')[:9]
            decSex = decSex.replace(':', '')[:9]
            sdssName = 'SDSS J%(raSex)s%(decSex)s' % locals()
            row['sdss_name'] = sdssName
            wordType = [
             'unknown', 'cosmic_ray', 'defect', 'galaxy',
             'ghost', 'knownobj', 'star', 'trail', 'sky', 'notatype']
            numberType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            row['type'] = wordType[row['type']]

        self.log.debug('completed the ``_generate_sdss_object_name`` method')
        return


if __name__ == '__main__':
    main()