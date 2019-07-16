import datetime
from jinja2     import Template, Environment, FileSystemLoader
from subprocess import call
from .yml_to_tex import yml_to_tex as yml

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
)
#datetime.datetime.now().isoformat()#.split('T')[0]

def y2t(yml_string):
    document = yml.yml_to_tex(yml_string)
    return {"document": document}

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

def write_out(string, filename="default.tex", backup="", latex=True, engine=["latexmk", "--pdf"], externalize=""):
    if "tex" not in filename:
        filename += ".tex"

    if backup:
        open(f"{backup}/{filename}", "w").write(string)

    open(filename, "w").write(string)

    if latex:
        compile_pdf(filename, engine=engine, externalize=externalize)

if __name__ == "__main__":
    print("meme")
