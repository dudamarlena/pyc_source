# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/package_analyzers/manifest_xml_analyzer.py
# Compiled at: 2019-02-05 11:52:53
# Size of source mod 2**32: 1513 bytes
from .package_analyzer import PackageAnalyzer
from xml.etree.cElementTree import parse
from xml.etree.cElementTree import ParseError
import os, logging

class ManifestXmlAnalyzer(PackageAnalyzer):
    __doc__ = '\n    Analyzer plug-in that analyzes manifest.xml (rosbuild) package files.\n    '

    def analyze_file(self, path: str, dependencies: dict) -> dict:
        """
        Analyzes a manifest.xml file.
        :param path: Path to the manifest.xml file.
        :param dependencies: Dictionary containing (key: package name, value: list[dependency, dependency, ...]
        :return: updated dependencies-dictionary.
        """
        try:
            file = open(path, 'r')
            tree = parse(file)
        except ParseError:
            logging.warning('[ManifestXmlAnalyzer]: Could not parse ' + path + '; omitting file.')
            return dependencies

        element = tree.getroot()
        packagename = os.path.basename(os.path.dirname(path))
        for tag in self._settings['manifest_xml_dependency_tags']:
            for element in element.findall(tag):
                self.add_dependency(packagename, element.attrib['package'], dependencies)

    def _analyze(self, path: str) -> dict:
        packages = dict()
        filellist = self.search_files(path, 'manifest.xml')
        for filename in filellist:
            logging.info('[ManifestXmlAnalyzer]: Analyzing ' + filename)
            self.analyze_file(filename, packages)

        return packages