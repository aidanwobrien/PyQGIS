"""
Model exported as python.
Name : Conservation Area Connectivity
Group : 
With QGIS : 31601
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsExpression
import processing


class ConservationAreaConnectivity(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('PropertyBoundary', 'Property Boundary', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('MPaCoverage', '500-1000m PA Coverage', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(12, model_feedback)
        results = {}
        outputs = {}

        # 500m Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 500,
            'END_CAP_STYLE': 0,
            'INPUT': parameters['PropertyBoundary'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': 'ProtectedAreas_EntireStudyArea_2020_83ca49f3_adb0_4ae3_8442_0648b877483e',
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:32617'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # 1000m Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 1000,
            'END_CAP_STYLE': 0,
            'INPUT': parameters['PropertyBoundary'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # 500-1000m buffer
        alg_params = {
            'INPUT': outputs['MBuffer']['OUTPUT'],
            'OVERLAY': outputs['MBuffer']['OUTPUT'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MBuffer'] = processing.run('native:symmetricaldifference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # 500m Clip
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OVERLAY': outputs['MBuffer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MClip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # 500m Calculation
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': '500m_Acres',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 1,
            'FORMULA': 'value = (($geom.area())/10000) * 2.4715',
            'GLOBAL': '',
            'INPUT': outputs['MClip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MCalculation'] = processing.run('qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # 500m dropped
        alg_params = {
            'COLUMN': QgsExpression('(\'ARN;GEO_UPD_DT;EFF_DATE;Area;FID_StudyA;Area_Acres;Score_Plan;Score_Arch;Score_ANSI;Score_Gree;Score_PA;Score_CWS;Score_Ripa;Score_PSW;Score_Wetl;Total_Scor;Score_Spec;Shape_Leng;Shape_Area;Priority;OGF_ID;IDENT;TYPE_C;REG_OFFICE;POLARIS_ID;STATE_C;Owner;For_Score;NatShore_S;Kettle_Sco;LA_Score;Score_100a;PropArea;layer;path;OBJECTID;OFFICIAL_N;Shape_Le_1\')').evaluate(),
            'INPUT': outputs['MCalculation']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MDropped'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # 500-1000m Clip
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OVERLAY': outputs['MBuffer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MClip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # 500-1000m Calculation
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': '500-1000m-Acres',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 1,
            'FORMULA': 'value = (($geom.area())/10000) * 2.4715',
            'GLOBAL': '',
            'INPUT': outputs['MClip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MCalculation'] = processing.run('qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # 1000m dropped
        alg_params = {
            'COLUMN': QgsExpression('(\'ARN;GEO_UPD_DT;EFF_DATE;Area;FID_StudyA;Area_Acres;Score_Plan;Score_Arch;Score_ANSI;Score_Gree;Score_PA;Score_CWS;Score_Ripa;Score_PSW;Score_Wetl;Total_Scor;Score_Spec;Shape_Leng;Shape_Area;Priority;OGF_ID;IDENT;TYPE_C;REG_OFFICE;POLARIS_ID;STATE_C;Owner;For_Score;NatShore_S;Kettle_Sco;LA_Score;Score_100a;PropArea;layer;path;OBJECTID;OFFICIAL_N;Shape_Le_1\')').evaluate(),
            'INPUT': outputs['MCalculation']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MDropped'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Merge vector layers
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['MDropped']['OUTPUT'],outputs['MDropped']['OUTPUT']],
            'OUTPUT': parameters['MPaCoverage']
        }
        outputs['MergeVectorLayers'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['MPaCoverage'] = outputs['MergeVectorLayers']['OUTPUT']
        return results

    def name(self):
        return 'Conservation Area Connectivity'

    def displayName(self):
        return 'Conservation Area Connectivity'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return ConservationAreaConnectivity()
