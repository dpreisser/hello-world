
import os
import re


###############################################################################
##
## Parses a line at a time and checks if it has a comment.
## It is not a fully qualified parser. Rather it extracts
## only the first comment section of the line.
## It checks that // or /* */ are not part of a quote (string).
##
## Attention must be paid to the following limitations:
##
## - There can be only one comment in one line of code.
##   Thus /* comment 1 */ statement 1 /* comment 2 */
##   only returns comment 1. The remainder is skipped
##   and this line is considered to be a comment line.
##
## - Similar:
##   statement 1 /* comment 1 */
##   statement 2 // comment 1
##   would return comment 1 and the line is considered
##   to be a comment line.
##
## input:
## string, const: line
##
## input + output:
## bool: isInComment
## /* */ can span multiple lines.
## getComment parses a line at a time and thus has to know
## if we are already in a comment which spans multiple lines.
##
## output:
## list of strings: comments
## Currently the list has only 1 string if a comment is found.
##
###############################################################################

def getComment( line, isInComment ):

    size = len(line)
    idx = 0

    comments = []

    posBegin = 0
    posEnd = 0

    if isInComment:

        # Only one comment in one line of code is assumed.
        while idx < size-1:
        
            if line[idx] == "*" and line[idx+1] == "/":
                posEnd = idx+2
                aComment = line[posBegin:posEnd]
                comments.append( aComment ) 
                isInComment = False
                return comments, isInComment

            idx = idx + 1

        posEnd = size
        aComment = line[posBegin:posEnd]
        comments.append( aComment ) 

    else:

        isInQuote = False
        quote = ""

        while idx < size-1 and not isInComment:

            if isInQuote:

                if line[idx] == quote[0]:
                    isInQuote = False
                elif line[idx] == "\\" and line[idx+1] == quote[0]:
                    idx = idx + 1

            else:
                    
                if line[idx] == "'" or line[idx] == "\"":
                    isInQuote = True
                    quote = line[idx]
                    idx = idx + 1
                    continue

                if line[idx] == "/" and line[idx+1] == "/":
                    posBegin = idx
                    posEnd = size
                    aComment = line[posBegin:posEnd]
                    comments.append( aComment ) 
                    return comments, isInComment

                if line[idx] == "/" and line[idx+1] == "*":
                    posBegin = idx
                    isInComment = True
                    idx = idx + 1

            idx = idx + 1

            # Only one comment in one line of code is assumed.
            while idx < size-1 and isInComment:
        
                if line[idx] == "*" and line[idx+1] == "/":
                    posEnd = idx+2
                    aComment = line[posBegin:posEnd]
                    comments.append( aComment ) 
                    isInComment = False
                    return comments, isInComment

                idx = idx + 1

            if isInComment:
                posEnd = size
                aComment = line[posBegin:posEnd]
                comments.append( aComment ) 

    return comments, isInComment


def getAnnotatedFiles( fileName ):

    matchExpr = r'(.*?[/,\*,\s])annotationFile:\s*(.*?)($|\s+.*$)'

    annotatedFiles = []

    try:
        fileStream = open( fileName, "rt" )
    except IOError as what:
        print( what )
        return annotatedFiles

    line = 'NotEmpty'
    lineNumber = 0

    isInComment = False
    comments = []

    while line:
        
        line = fileStream.readline();
        lineNumber = lineNumber + 1
        
        comments, isInComment = getComment( line, isInComment ) 
        
        # This means we have actually found a comment line.
        if len(comments) > 0:

            # print( 'Comment: ' + comments[0] )
            res = re.findall( matchExpr, comments[0], re.M )

            if len(res) > 0:

                annotatedFile = res[0][1]

                if "*/" == annotatedFile[-2:]:
                    annotatedFile = annotatedFile[:-2]

                annotatedFiles.append( annotatedFile )


    return annotatedFiles

    
if "__main__" == __name__:

    import sys

    if 2 == len( sys.argv ):
        fileName = sys.argv[1]
        annotatedFiles = getAnnotatedFiles( fileName )
        print( annotatedFiles )
    else:
        print( "Provide a filename on the command line." )
