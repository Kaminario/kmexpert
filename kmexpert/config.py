#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

from kmexpert.base.tooling import class_to_name
from kmexpert.base.execution_context import ExecCtx
from kmexpert.base.procedure_base_abs import ProcedureBaseAbs
from kmexpert.base.tooling import clean_style


class Config(object):
    Procedures = dict()  # type: Dict[str, type(ProcedureBaseAbs)]
    Tags = dict()

    @classmethod
    def add_procedure(cls, procedure_class):
        cls.Procedures[class_to_name(procedure_class)] = procedure_class
        cls.Tags.setdefault(class_to_name(procedure_class), set())

    @classmethod
    def add_tag(cls, procedure_class, tag):
        tag = str(tag).lower()
        cls.Tags.setdefault(class_to_name(procedure_class), set()).add(tag)

    @classmethod
    def get_procedure(cls, procedure_name):
        # type: (str) -> type(ProcedureBaseAbs)
        return cls.Procedures.get(procedure_name)

    @classmethod
    def procedures_names(cls):
        return cls.Procedures.keys()

    @classmethod
    def procedures(cls):
        # type: () -> Dict[str, type(ProcedureBaseAbs)]
        return cls.Procedures

    @classmethod
    def procedures_names_by_tags(cls, tags):
        tags = set(map(str.lower, map(str, tags)))
        return [name for name in cls.procedures_names() if tags & cls.Tags[name]]

    @classmethod
    def tags(cls):
        res = set()
        for tags_ in cls.Tags.values():
            res |= set(tags_)
        return res

    @classmethod
    def procedures_names_by_search(cls, text):
        # type: (str) -> List[str]
        def text_in_procedure(procedure_cls, text):
            return text.lower() in clean_style(procedure_cls(ExecCtx()).repr()).lower()

        return [name for name, cls_ in cls.Procedures.items() if text_in_procedure(cls_, text)]


def register_procedure(procedure_class):
    Config.add_procedure(procedure_class)
    return procedure_class


def tag(tag_):
    def decorator(procedure_class):
        Config.add_tag(procedure_class, tag_)
        return procedure_class
    return decorator


def tags(tags_):
    def decorator(procedure_class):
        for tag_ in tags_:
            Config.add_tag(procedure_class, tag_)
        return procedure_class
    return decorator
