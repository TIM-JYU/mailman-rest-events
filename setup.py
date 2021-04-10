from setuptools import setup, find_packages

setup(
    name="mailman-rest-event-dezhidki",
    version="0.0.1",
    description="Send mailman events via REST",
    author="Denis Zhidkikh",
    author_email="dezhidki@jyu.fi",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "mailman>=3"
    ],
)