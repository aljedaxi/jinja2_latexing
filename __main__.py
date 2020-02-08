from latex import do_everything_for_me

import datetime
from jinja2     import Template, Environment, FileSystemLoader
from subprocess import call
#from .yml_to_tex import yml_to_tex as yml
from yml_to_tex import yml_to_tex as yml

DEFAULT_TITLE = "a daxiin document"
DEFAULT_AUTHOR = "daxi"
                   #TODO: date or something
DEFAULT_FILENAME = "document.tex"
DEFAULT_EXTERNAL = "junk_drawer"

ENV = Environment(
    block_start_string      = '\BLOCK{',
    block_end_string        = '}',
    variable_start_string   = '\VAR{',
    variable_end_string     = '}',
    comment_start_string    = '%/*',
    comment_end_string      = '%*/',
    line_comment_prefix     = '%//',
    line_statement_prefix   = '%%',
    trim_blocks             = True,
    lstrip_blocks           = True,
    autoescape              = False,
    loader                  = FileSystemLoader("./jinja2_latexing"),
    #loader                  = FileSystemLoader("./"),
)
#datetime.datetime.now().isoformat()#.split('T')[0]

if __name__ == "__main__":
    import argparse 

    parser = argparse.ArgumentParser(
        description='Easily compile LaTeX documents',
        epilog='Honestly made with only my very specific needs in mind',
    )

    parser.add_argument('infile', metavar='I', type=str, #nargs='*',
                        help='a document which contains yml or LaTeX')
    parser.add_argument('--filename', 
                        action='store',
                        metavar='a', 
                        required=False,
                        type=str, 
                        help='author for document')
    parser.add_argument('--author', 
                        action='store',
                        metavar='a', 
                        required=False,
                        type=str, 
                        default=DEFAULT_AUTHOR,
                        help='author for document')
    parser.add_argument('--title', 
                        action='store',
                        metavar='t', 
                        required=False,
                        type=str, 
                        default=DEFAULT_TITLE,
                        help='title for document')
    parser.add_argument('--mode', 
                        action='store',
                        metavar='m', 
                        required=False,
                        type=str, 
                        default='unspecified',
                        help='title for document')

    args = parser.parse_args()

    infile = args.infile
    instring = open(infile).read()

    if args.filename:
        filename = args.filename
    else:
        filename = args.infile.split('.')[0]

    status = do_everything_for_me(
        instring,
        title=args.title,
        author=args.author,
        filename=filename,
        mode=args.mode,
    )

    if not status:
        print("something must be wrong")
