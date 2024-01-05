import setuptools


__version__ = "0.0.0"

AUTHOR = "Aparna T Parkala"
PROJECT_NAME = "CREDIT CARD DEFAULTER PREDICTION"
DESCRIPTION = "Given customer information, the developed model should be able to predict if customer defaults on credit card payment or not."

def get_requirements_list()->list:
    """
        Returns list of libraries mentioned in requirements.txt file
    """
    with open("requirements.txt") as require_fobj:
        return require_fobj.readlines()

setuptools.setup(
    name=PROJECT_NAME,
    version=__version__,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=setuptools.find_packages(),
    install_requires = get_requirements_list()
)