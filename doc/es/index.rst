===============================
Validación de cuentas bancarias
===============================

Permite la validación de cuentas bancarias de terceros o empresas. Al añadir el
número de cuenta bancaria, debe añadir de qué país es la cuenta. Si la cuenta
no es correcta, un mensaje le notificará que revise el número de cuenta bancaria.

Este módulo se basa en una librería de validación de cuentas bancarias. 
Dependiendo de si existe o no el método de validación de un país en concreto,
Tryton validará o no las cuentas bancarias para el mismo.

Módulos de los que depende
==========================

Instalados
----------

.. toctree::
   :maxdepth: 1

   /party_bank/index

Dependencias
------------

* Bancos_

.. _Bancos: ../party_bank/index.html
