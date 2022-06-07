import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = 'flasktts'

setuptools.setup(
    name="flasktts",
    version="0.0.6",
    author="Kristof",
    description="flasktts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/py_flask_tts",
    packages=setuptools.find_packages(),
    install_requires=[
        'Flask>=1.1.2',
        'kcu>=0.0.73',
        'kffmpeg>=0.2.46',
        'pyttsx3>=2.90',
        'setuptools>=62.3.2',
        'Unidecode>=1.3.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)