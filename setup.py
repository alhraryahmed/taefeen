from setuptools import find_packages, setup

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in hajj_umrah_manager/__init__.py
from hajj_umrah_manager import __version__ as version

setup(
	name="hajj_umrah_manager",
	version=version,
	description="نظام إدارة المعتمرين والحجوزات والأقساط والخزينة - شركة الطائفين لخدمات الحج والعمرة",
	author="Al-Taefeen Hajj & Umrah Services",
	author_email="info@altaefeen.example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
