from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'pycitylayers'
LONG_DESCRIPTION = 'an api wrapper to explore and query db'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pycitylayers", 
        version=VERSION,
        author="Milad Aghamohamadnia",
        author_email="<milad.aghamohamadnia@concordia.ca>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
                        "pandas",
                        "numpy",
                        "matplotlib",
                        "pyyaml",
                        "requests",
                        "shapely",
                        "jupyter",
                        "gql-query-builder==0.1.7",
                        "pycitylayers"
                        ], # add any additional packages that 
                            # needs to be installed along with your package. Eg: 'caer'
        keywords=['python', 'pycitylayers'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)