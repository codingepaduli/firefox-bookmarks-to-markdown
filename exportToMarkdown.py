#!/usr/bin/env python

import json
import sys
from argparse import ArgumentParser

def parse_json_response(content, level, allowedSections, skipSections):
    """Recursively iterate over Mozilla Firefox bookmarks structure.
    
        The Mozilla Firefox bookmarks structure is recursive. Base element is a dict with an array of children elements (with the same structure).
        {
            title: "..."
            uri: "..."
            typeCode: 1234
            children = [ recursive, recursive, recursive ]
        }
        
        The typeCode has the following value:
            typeCode == 1 => "text/x-moz-place" (a bookmark)
            typeCode == 2 => "text/x-moz-place-container" (a bookmark folder)
            typeCode == 3 => "text/x-moz-place-separator" (a separator)
            typeCode == 4 => dynamic container (removed in Gecko 11)
            typeCode == -1 => unknown index
        
        If the current structure is a bookmark (typeCode == 1), it will be printed
        If the current structure is a bookmark section (typeCode == 2), the section will be printed and it will recursively iterate over the children list
        Other typeCode are skipped.
        
        Parameters
        ----------
        content : dict, mandatory
            The dict with a Mozilla Firefox bookmarks structure

        level : int, mandatory
            The level of nesting
        
        allowedSections : list, mandatory
            The list of allowed sections

        skipSections : list, mandatory
            The list of denied sections 
    """
    
    if content['typeCode'] == 1:
        printBookmark(content)
    elif content['typeCode'] == 2: 
        sectionAllowed = isSectionAllowed(content, allowedSections)
        sectionDenied = isSectionDenied(content, skipSections)
        # print('+%s+ is allowed: %s and denied: %s' % (content['title'], sectionAllowed, sectionDenied))
        if "children" in content and sectionAllowed and not sectionDenied:
            # skip the root folder
            if level > 0:
                printSection(content, level)
                
            for item in content['children']:
                parse_json_response(item, level + 1, allowedSections, skipSections)
    elif content['typeCode'] == 3:
        pass
    else:
        print('Strange type')

def printBookmark(bookmark):
    """Print the current bookmark (title and uri)"""
    if "title" in bookmark and "uri" in bookmark:
        titleParts = bookmark['title'].split(" - ", 1)
        titleParts.append('') # create a two element array (split() can return a single element array)

        # HTML sanitizer
        titleParts[0] = titleParts[0].replace('<','&lt;').replace('>','&gt;')
        titleParts[1] = titleParts[1].replace('<','&lt;').replace('>','&gt;')
        print('[' + titleParts[0] + ']' + '(' + bookmark['uri'] + ') - ' + titleParts[1] + '\\') # '\' meaning "new line" in Markdown


def printSection(section, level):
    """Print the current section title"""
    
    #print(f'<!-- {level} - (type) {section["typeCode"]} : (title) {section["title"]}  -->')
    print('')
    print('#' * level + ' ' + section['title'])
    print('')


def isSectionAllowed(section, allowedSections):
    """Check if the current section is in the allowed section list.

        The argument `section` is a mandatory dict.
        The argument `allowedSections` is a mandatory list of string.
        If the argument `allowedSections` is empty, all sections with a title are allowed.
        If the argument `section` has a title and the section title is in allowedSections, then the section is allowed.

        Parameters
        ----------
        section : dict, mandatory
            The dict with a title key

        allowedSections : list, mandatory
            The list of allowed sections
        
        Returns
        -------
        boolean
            True if the section is allowed, False otherwise
            
        Raises
        ------
        Error
            If no section or allowedSections are passed in as parameter or their type is wrong
    """
    
    if "title" not in section:
        sectionAllowed = False
    elif len(allowedSections) == 0:
        sectionAllowed = True;
    elif section['title'] in allowedSections:
        sectionAllowed = True
    else:
        sectionAllowed = False
    return sectionAllowed


def isSectionDenied(section, skipSections):
    """Check if the current section is in the denied section list.

        The argument `section` is a mandatory dict.
        The argument `skipSections` is a mandatory list of string.
        If the argument `skipSections` is empty, all sections with a title are allowed.
        If the argument `section` has a title and the section title is in skipSections, then the section is denied.

        Parameters
        ----------
        section : dict, mandatory
            The dict with a title key

        skipSections : list, mandatory
            The list of denied sections 
            
        Returns
        -------
        boolean
            True if the section is denied, False otherwise
            
        Raises
        ------
        Error
            If no section or skipSections are passed in as parameter or their type is wrong
    """
    
    if "title" not in section:
        sectionDenied = True
    elif len(skipSections) == 0:
        sectionDenied = False
    elif section['title'] not in skipSections:
        sectionDenied = False
    else: 
        sectionDenied = True
    return sectionDenied


if __name__ == "__main__":
    argparser = ArgumentParser(prog='exportToMarkdown', allow_abbrev=False, description="Firefox Json to Markdown utility")
    argparser.add_argument(
            "in_file",
            type=str,
            help="Path to input file."
        )
    argparser.add_argument(
            "-a",               # short parameter name
            "--allowed",        # long parameter name
            type=str,
            nargs='*',          # from 0 to infinite apparence as parameter
            metavar='sectionName', # the parameter list  name
            default=[],
            action='store',     # store the value
            help="Section allowed."
        )
    argparser.add_argument(
            "-d",               # short parameter name
            "--denied",         # long parameter name
            type=str,
            nargs='*',          # from 0 to infinite apparence as parameter
            metavar='sectionName', # the parameter list  name
            default=[],
            action='store',     # store the value
            help="Section denied."
        )
    parsed_args = argparser.parse_args()

    try:
        in_file = open(parsed_args.in_file, "rt")
    except IOError as e:
        print("Could not open input file `%s' for reading: %s" % (parsed_args.in_file, e), file=sys.stderr)
        sys.exit(2)

    try:
        # load the json dictionary from file
        data = json.load(in_file)
        # traverse the data dictionary and print the url in Markdown format
        parse_json_response(data, 0, parsed_args.allowed, parsed_args.denied)
    except Exception as e:
        print("Could not convert Firefox Json to Markdown `%s': %s" % (parsed_args.in_file, e), file=sys.stderr)
        sys.exit(4)
    finally:
        in_file.close()
