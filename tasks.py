from invoke import run
from invoke import task


@task
def clean(context):
    print("Cleaning ...")
    patterns = ['*.log', 'report/_*', 'report/figures', 'report/*.aux', 'report/*.log', 'report/*.out',
                'report/report.tex',
                'report/*.pdf', '*.pyc', 'report/*.pyc', 'report/*.bbl', 'report/*.blg']
    for pattern in patterns:
        context.run("rm -rf {}".format(pattern))


@task
def build_latex(context):
    print("Building latex file and figures through pweave ...")
    command = 'cd report && pweave -f texminted report.texw'
    run(command, hide=False, warn=True)


@task
def build_report(context):
    print("Building pdf through pdflatex ...")
    command = 'cd report ' \
              '&& pdflatex -shell-escape report.tex ' \
              '&& bibtex report.aux ' \
              '&& pdflatex -shell-escape report.tex ' \
              '&& pdflatex -shell-escape report.tex'
    run(command, hide=False, warn=True)


@task
def open_pdf(context):
    command = 'cd report && open report.pdf'
    run(command, hide=True, warn=True)


@task
def build(context):
    build_latex(context)
    build_report(context)
