"""
Base model
"""
__all__ = ['BaseModel']


class BaseModel(object):
    """Base Model for sqlalchemy classes

      * __init__ provides a default constructor ala sqlalchemy or django
                 declaritive default constructors.
      * __repr__ is class name and primarykey(s)
      * __str__ uses unicode if it can (we define that more...revisit??)
    """
    def __init__(self, **kwargs):
        """object initialization using keyword arguments
        bogus kwargs will generate an error...no extas allowed!"""

        for key, val in kwargs.items():
            if hasattr(self.__class__, key):
                setattr(self, key, val)
            else:
                raise TypeError("got unexpected keyword argument %r" % key)

    def __repr__(self):
        # model, keys = instance_state(self).key
        keys = self._sa_class_manager.mapper.primary_key_from_instance(self)
        if len(keys) == 1:
            key = keys[0]
            args = '(%r)' % (str(key) if isinstance(key, unicode) else key)
        else:
            args = repr(tuple(str(x) if isinstance(x, unicode) else x
                        for x in keys))
        return self.__class__.__name__ + args

    def __str__(self):
        "just try to make `print obj` work interactively"
        try:
            return str(unicode(self))
        except:
            return repr(self)
