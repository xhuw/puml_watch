from importlib import resources


def plantuml_path():
    return resources.path("puml_watch_plantuml.plantuml", "plantuml-1.2024.6.jar")
