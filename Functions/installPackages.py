import pip

packages=['requests','selenium','bs4', 'sklearn', 'numpy', 'editdistance', 'networkx', 'nltk', 'textblob']

def installPackages():
    for package in packages:
        pip.main(['install',package])
