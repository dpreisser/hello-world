
import os
import json
from copy import deepcopy

from vector.apps.Analytics.plugin import FilePlugin, FunctionPlugin
from vector.apps.Analytics.metrics import Metric, Grouping

from utils import getAnnotatedFiles


class ExamplePluginFile( FilePlugin ):

    plugin_name = "my_example_file"

    def get_tags(self):
        return ["my_example_file_plugin_enabled"]


    def initialize( self ):

        self.initialized = False

        self.using_get_object_data = True

        self.annotatedFiles = {}
        self.annotatedData = {}

    
    def init( self, context ):

        self.annotationRoot = context.get( "annotationRoot", os.getcwd() )
        self.annotationDirectories = context.get( "annotationDirectories", [] )
        self.extensionMarker = context.get( "extensionMarker", "." )
        self.extension = context.get( "extension", "" )

        self.initialized = True


    def setProperties( self, sourceFileName ):

        dirname = os.path.dirname( sourceFileName )
        
        for annotatedFile in self.annotatedFiles[sourceFileName]:

            if not os.path.isabs(annotatedFile):

                if len(self.annotationDirectories) > 0:
                    annotationDir = self.annotationDirectories[0]
                else:
                    annotationDir = ""

                annotationDir = os.path.join( self.annotationRoot, annotationDir )
                annotatedFile = os.path.join( annotationDir, annotatedFile )
                annotatedFile = os.path.normpath( annotatedFile )

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

                if self.using_get_object_data and ( not os.path.isabs(fileName) ):
                    fileName = os.path.join( dirname, fileName )
                    fileName = os.path.normpath( fileName )

                print( "Add to annotatedData: %s" % fileName )
                self.annotatedData[fileName] = dataSet


    # Rename as an effective way of commenting out.
    def get_data_1( self, context ):

        if not self.initialized:
            self.init( context )

        dataList = []

        for annotationDir in self.annotationDirectories:

            if not os.path.isabs( annotationDir ):
                annotationDir = os.path.join( self.annotationRoot, annotationDir )
                annotationDir = os.path.normpath( annotationDir )

            if not os.path.isdir( annotationDir ):
                continue

            fileNames = os.listdir( annotationDir )

            for fileName in fileNames:

                fileName.strip()

                components = fileName.split( self.extensionMarker )
                if len(components) > 1:
                    extension = components[-1]
                else:
                    extension = ""

                if not extension == self.extension:
                    continue

                if not os.path.isabs( fileName ):
                    fileName = os.path.join( annotationDir, fileName )
                    fileName = os.path.normpath( fileName )

                if not fileName in self.annotatedFiles.keys():

                    print( "Add to annotatedFiles: %s" % fileName )

                    self.annotatedFiles[fileName] = [ fileName ]
                    self.setProperties( fileName )

                    data = {}
                    data["path"] = fileName

                    dataList.append( deepcopy(data) )

        return dataList


    # Rename as an effective way of commenting out.
    def get_object_data(self, original_object, context):

        if not self.initialized:
            self.init( context )

        fileName = original_object["path"]
        fileName = os.path.normpath( fileName )
        print( "fileName: %s" % fileName )

        if not fileName in self.annotatedFiles.keys():

            self.annotatedFiles[fileName] = getAnnotatedFiles( fileName )
            print( "Add to annotatedFiles: %s" % str(self.annotatedFiles[fileName]) )

            self.setProperties( fileName )

        numAnnotatedFiles = len( self.annotatedFiles[fileName] )

        return { "numAnnotatedFiles": numAnnotatedFiles }


class NumAnnotatedFiles(Metric):
    id = "numAnnotatedFiles"
    label = "Number of annotated files"
    prop = "numAnnotatedFiles"
    default = 0
    granularity = "file"
