from scripts import dependencies
from scripts.enums import SubProjects


def all_dependencies():
    for subproject in SubProjects:
        dependencies(subproject)


def api_dependencies():
    dependencies(SubProjects.API)