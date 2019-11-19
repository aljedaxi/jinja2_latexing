#!/usr/bin/env python3

#TODO create mark down interface

import datetime
import os
from jinja2     import Template, Environment, FileSystemLoader
from subprocess import call
#from .yml_to_tex import yml_to_tex as yml
from yml_to_tex import yml_to_tex as yml
from ruamel import yaml

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
    loader                  = FileSystemLoader(os.path.dirname(os.path.realpath(__file__)))
    #loader                  = FileSystemLoader("./"),
)
#datetime.datetime.now().isoformat()#.split('T')[0]

def fill(template_file, meta, env=ENV):
    """
        fills a given template with data.
    """

    template = env.get_template(template_file)
    return template.render(**meta)

def compile_pdf(filename, engine=["latexmk", "--pdf"], externalize=""):
    if externalize:
        call(("mkdir", externalize))
        engine.append(f"-output-directory={externalize}")

    try:
        call((*engine, filename))
    except:
        call((engine, filename))

    if externalize:
        #bring the pdf into the current directory
        extensionless = os.path.splitext(filename)[0]
        call(("mv", f"{externalize}/{extensionless}.pdf", "./"))

def write_out(string, filename=DEFAULT_FILENAME, backup="", latex=True, engine=["latexmk", "--pdf"], externalize=""):
    if "tex" not in filename:
        filename += ".tex"

    if backup:
        open(f"{backup}/{filename}", "w").write(string)

    open(filename, "w").write(string)

    if latex:
        compile_pdf(filename, engine=engine, externalize=externalize)

def do_everything_for_me(
    string, 
    title=DEFAULT_TITLE,
    author=DEFAULT_AUTHOR,
    filename=DEFAULT_FILENAME,
    TEMPLATE="shell.tex",
    backup="", 
    latex=True, 
    engine=["latexmk", "--pdf"], 
    externalize=DEFAULT_EXTERNAL,
    mode='yaml',
):
    meta = {}
    if mode == 'yaml':
        meta = yaml.safe_load(string)
    else:
        meta['document'] = string
        meta['title'] = title
        meta['author'] = author

    write_out(
        fill(TEMPLATE, meta,),
        backup=backup,
        latex=latex,
        engine=engine,
        filename=filename,
        externalize=externalize,
    )

    return True

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
        help='author for document',
    )
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

    args = parser.parse_args()

    infile = args.infile
    instring = open(infile).read()

    status = do_everything_for_me(
        instring,
        title=args.title,
        author=args.author,
        filename=args.filename,
    )

    if not status:
        print("something must be wrong")
