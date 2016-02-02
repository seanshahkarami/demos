_class_template = """
from struct import Struct

class {classname}(object):

    __slots__ = {fieldnames}

    _struct = Struct('{fieldformat}')

    def __bytes__(self):
        return self._struct.pack({packfields})
"""

# TODO add sane __init__


def namedstruct(classname, fields, endian='<'):
    fieldnames = tuple(name for name, _ in fields)
    fieldformat = ''.join(type for _, type in fields)
    packfields = ', '.join(map(lambda name: 'self.{}'.format(name), fieldnames))

    code = _class_template.format(classname=classname,
                                  fieldnames=fieldnames,
                                  fieldformat=fieldformat,
                                  packfields=packfields)

    env = dict()
    exec(code, env)
    return env[classname]
