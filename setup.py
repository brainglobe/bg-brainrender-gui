# from setuptools import setup, find_namespace_packages

# with open("requirements.txt") as f:
#     requirements = f.read().splitlines()

# setup(
#     name="bgviewer",
#     version="0.0.1rc0",
#     description="Visualisation and exploration of brain atlases",
#     install_requires=requirements,
#     extras_require={
#         "dev": [
#             "sphinx",
#             "recommonmark",
#             "sphinx_rtd_theme",
#             "pydoc-markdown",
#             "black",
#             "pytest-cov",
#             "pytest",
#             "gitpython",
#             "coverage",
#             "pre-commit",
#         ]
#     },
#     python_requires=">=3.6, <3.8",
#     packages=find_namespace_packages(exclude=("docs", "tests*")),
#     include_package_data=True,
#     url="https://github.com/brainglobe/bgviewer",
#     author="Adam Tyson, Luigi Petrucco, Federico Claudi",
#     author_email="adam.tyson@ucl.ac.uk",
#     classifiers=[
#         "Development Status :: 3 - Alpha",
#         "Operating System :: POSIX :: Linux",
#         "Operating System :: Microsoft :: Windows :: Windows 10",
#         "Operating System :: MacOS :: MacOS X",
#         "Programming Language :: Python",
#         "Programming Language :: Python :: 3.6",
#         "Programming Language :: Python :: 3.7",
#         "Programming Language :: Python :: 3.8",
#         "Intended Audience :: Developers",
#         "Intended Audience :: Science/Research",
#     ],
#     entry_points={
#         "console_scripts": [
#             "bgviewer = bgviewer.viewer:main",
#             "bgviewer3d = bgviewer.viewer3d:main",
#         ]
#     },
#     zip_safe=False,
# )
