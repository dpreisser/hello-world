
import os

from vector.apps.Analytics.plugin import FunctionPlugin
from vector.apps.Analytics.metrics import Metric, Grouping


class ExamplePlugin(FunctionPlugin):

    plugin_name = "my_example"

    def initialize( self ):
        self.myDict = {}
        self.charMetricsFile = os.path.join( "C:\\", "Demo", "Dashboard", "lab_source_code", "manager_diner", "char_metrics.txt" )

    def readData( self ):

        fileStream = open( self.charMetricsFile, "rt" )

        line = fileStream.readline()
        while( line ):
            components = line.split( ":" )
            components[0].strip()
            components[1].strip()
            self.myDict[components[0]] = int( components[1] )
            line = fileStream.readline()

        fileStream.close()

        print( self.myDict )

    def get_object_data(self, original_object, context):

        self.charMetricsFile = os.path.join( context["vcm_dir"][0], "char_metrics.txt" )

        if 0 == len( self.myDict.keys() ):
            self.readData()

        name = original_object["name"]
        return { "value": self.myDict.get(name,0) }

    def get_tags(self):
        return ["my_example_plugin_enabled"]


class NumCharsFunc(Metric):
    id = "numCharsFunc"
    label = "Number of characters in a function"
    prop = "value"
    default = 0
    granularity = "function"


class AvgNumCharsFunc(Metric):
    id = "avgNumCharsFunc"
    label = "Average number of characters per function"
    metafunc = "divide"
    components = ( "numCharsFunc", "count" )
    default = 0
    granularity = "function"


class ComplexityGrouping(Grouping):
    id = "group_complexity"
    label = "Group according to cyclomatic complexity"
    default = "-1"

    def get_group(self, obj):
        complexity = Metric.complexity.calculate(obj)
        if complexity > 10:
            return ">10"
        elif complexity > 9:
            return "9-10"
        elif complexity > 8:
            return "8-9"
        elif complexity > 7:
            return "7-8"
        elif complexity > 6:
            return "6-7"
        elif complexity > 5:
            return "5-6"
        elif complexity > 4:
            return "4-5"
        elif complexity > 3:
            return "3-4"
        elif complexity > 2:
            return "2-3"
        elif complexity > 1:
            return "1-2"
        else:
            return "0-1"
