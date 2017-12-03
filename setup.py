from setuptools import find_packages, setup


INSTALL_REQUIREMENTS = [
    "tornado",
]
SETUP_REQUIREMENTS = [
    "milksnake",
]
TEST_REQUIREMENTS = []


def build_native(spec):
    build = spec.add_external_build(
        cmd=["cargo", "build", "--release"],
        path="./rust",
    )
    spec.add_cffi_module(
        module_path="papyrus._native",
        dylib=lambda: build.find_dylib("papyrus", in_path="target/release"),
        header_filename=lambda: build.find_header("papyrus.h", in_path="target"),
        rtld_flags=['NOW', 'NODELETE'],
    )


setup(
    name="papyrus",
    version="0.1.0",
    description="A POC Python/Rust echo server using websockets",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    milksnake_tasks=[build_native],
    install_requires=INSTALL_REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
)
