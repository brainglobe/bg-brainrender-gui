from setuptools import setup, find_namespace_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="bg-brainrender-gui",
    version="0.0.5rc1",
    description="Visualisation and exploration of brain atlases and other anatomical data",
    install_requires=requirements,
    python_requires=">=3.6, <3.8",
    packages=find_namespace_packages(
        exclude=("docs", "tests*", "brainrender_gui/__pycache__")
    ),
    include_package_data=True,
    url="https://github.com/brainglobe/bg-brainrender-gui",
    author="Adam Tyson, Luigi Petrucco, Federico Claudi",
    author_email="federicoclaudi@protonmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    entry_points={
        "console_scripts": [
            "brainrender-gui = brainrender_gui.__init__:clilaunch",
        ]
    },
    zip_safe=False,
)
