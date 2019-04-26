#!/usr/bin/python3.7
import os
import argparse
import re


# takes the root directory and walks through all sub directories
# yielding the full path to files found
def getFileNames(searchRoot, fileExtension):
    for path,directories,files in os.walk(searchRoot):
        for f in files:
            if fileExtension == 'any':
                yield open(os.path.join(path,f))
            else:
                if f.lower().endswith(fileExtension):
                    yield open(os.path.join(path,f))


# yields the lines in a file, as well as passing forward the file name
def getLinesInFiles(files):
    for f in files:
        try:
            for line in f:
                yield line, f.name
        except:
            pass

# yields the line that contains the search term
def findTermInLines(lines, thisFile, searchTerm=None):
    #for line in lines:
    if searchTerm in lines:
        yield lines, thisFile


# initiates the whole process and prints results
def main(searchRoot, SearchTerm, fileExtension):
    files = getFileNames(searchRoot, fileExtension)

    # store the location we're in - only display file name once
    tempLoc = None

    for lines,thisFile in getLinesInFiles(files):
        for result,location in findTermInLines(lines, thisFile, searchTerm):
            if tempLoc != location:
                tempLoc = location
                if result is not None:
                    print("%s\n\t%s" % (location.replace(searchRoot, '/'), result.strip()))
            else:
                if result is not None:
                    print("\t%s" % (result.strip()))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Searches files within a given directory for a string.  returns the name of any file where the search term is found, and prints the line that term was on')
    parser.add_argument('-r', metavar='searchRoot', help='the root directory to search in.  ex: \"/rootDocuments/\"')
    parser.add_argument('-s', metavar='searchTerm', help='the term to search for')
    parser.add_argument('-x', metavar='fileExtension', help='optionally choose to only search specific files.  ex: \"txt\" (2-3 characters)', default='any')

    args = parser.parse_args()
    searchRoot = args.r
    searchTerm = args.s
    fileExtension = args.x
    
    # check for valid file path format
    if re.search("^\/[a-zA-Z\/]*\/$", searchRoot):
        if searchRoot is not None and searchTerm is not None:
            # check for valid file extension format
            if re.search("^[a-zA-Z0-9]{2,3}$",fileExtension):
                main(searchRoot, searchTerm, fileExtension)
            else:
                print("Incorrect file extension format.  example: \"txt\" (2-3 characters)")
        else:
            print("Please provide a search root directory and a search term")
    else:
        print("Please check the search root format.  example: \"/root/Documents/\"")
