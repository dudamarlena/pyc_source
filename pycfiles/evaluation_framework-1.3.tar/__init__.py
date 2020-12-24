# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marpel/Scrivania/github/Evaluation-Framework/evaluation_framework/__init__.py
# Compiled at: 2020-01-21 09:44:15
from evaluation_framework.manager import FrameworkManager
from evaluation_framework.txt_dataManager import DataManager as txt_dataManager
from evaluation_framework.hdf5_dataManager import DataManager as hdf5_dataManager
from evaluation_framework.evaluationManager import EvaluationManager
import evaluation_framework.Classification.classification_model, evaluation_framework.Classification.classification_taskManager, evaluation_framework.Clustering.clustering_model, evaluation_framework.Clustering.clustering_taskManager, evaluation_framework.DocumentSimilarity.documentSimilarity_model, evaluation_framework.DocumentSimilarity.documentSimilarity_taskManager, evaluation_framework.EntityRelatedness.entityRelatedness_model, evaluation_framework.EntityRelatedness.entityRelatedness_taskManager, evaluation_framework.Regression.regression_model, evaluation_framework.Regression.regression_taskManager, evaluation_framework.SemanticAnalogies.semanticAnalogies_model, evaluation_framework.SemanticAnalogies.semanticAnalogies_taskManager