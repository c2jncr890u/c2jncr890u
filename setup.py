
from distutils.core import setup

setup(
    name='c2',
    version = "0.1",
    packages = ["c2lib"],
    py_modules = ["c2lib.codegen","c2lib.core","c2lib.parser","c2lib.toplevel","c2lib.types"],
    scripts = ["c2"],
)
