#!/usr/bin/env python
'''
Archivo de configuración para la instalación del proyecto.

Autores:
- A01749879 Julio Cesar Vivas Medina
- A01798380 Ulises Jaramillo Portilla

Fecha de creación: 2024-11-07

Fecha de modificación 2024-11-07
'''
from setuptools import find_packages, setup

requires = ["mesa"]

setup(
    name="sma-7-m1-actividad-1",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requires,
)
