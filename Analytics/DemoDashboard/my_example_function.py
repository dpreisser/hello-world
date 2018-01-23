
import os
import json

from vector.apps.Analytics.plugin import FilePlugin, FunctionPlugin
from vector.apps.Analytics.metrics import Metric, Grouping

from utils import getAnnotatedFiles


class ExamplePluginFile( FunctionPlugin ):

    plugin_name = "my_example_function"

    def get_tags(self):
        return ["my_example_function_plugin_enabled"]


    def initialize( self ):
        self.annotatedFiles = {}
        self.annotatedData = {}


    def setProperties( self, sourceFileName ):

        dirname = os.path.dirname( sourceFileName )
        
        for annotatedFile in self.annotatedFiles[sourceFileName]:

            try:
                stream = open( annotatedFile, "rt" )
            except IOError as what:
                print( what )
                continue

            content = stream.read()
            stream.close()

            theData = json.loads(content)

            for idx in range( len(theData["units"]) ):

                dataSet = theData["units"][idx]
                fileName = dataSet["fileName"]

                if not os.path.isabs( fileName ):
                    fileName = os.path.join( dirname, fileName )
                    fileName = os.path.normpath( fileName )

                print( "Stored with key: %s" % fileName )
                self.annotatedData[fileName] = dataSet


    def get_object_data(self, original_object, context):

        fileName = original_object["path"]
        fileName = os.path.normpath( fileName )
        print( "fileName: %s" % fileName )

        if not fileName in self.annotatedFiles.keys():

            self.annotatedFiles[fileName] = getAnnotatedFiles( fileName )
            print( self.annotatedFiles[fileName] )

            self.setProperties( fileName )

        functionName = original_object["name"]
        print( "functionName: %s" % functionName )

        numAnnotatedFiles = len( self.annotatedFiles[fileName] )
        numFunctionalRequirements = 0

        if fileName in self.annotatedData.keys():

            subroutines = self.annotatedData[fileName]["subroutines"]

            for idx in range( len(subroutines) ):
                if functionName == subroutines[idx]["name"]:
                    numFunctionalRequirements = len( subroutines[idx]["requirements"]["functional"] )
                    break

        return { "numAnnotatedFiles": numAnnotatedFiles, 
                 "numFunctionalRequirements" : numFunctionalRequirements }


class NumFunctionalRequirements(Metric):
    id = "numFunctionalRequirements"
    label = "Number of functional requirements"
    prop = "numFunctionalRequirements"
    default = 0
    granularity = "function"
