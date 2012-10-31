#This file is part party_bank_validation module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
import logging
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Not, Bool

HAS_BANKNUMBER = False
BANK_COUNTRIES = [('', '')]
try:
    import banknumber
    HAS_BANKNUMBER = True
    for country in banknumber.countries():
        BANK_COUNTRIES.append((country, country))
except ImportError:
    logging.getLogger('party_bank_validation').warning(
            'Unable to import banknumber. Bank code validation disabled.')

STATES = {
    'readonly': ~Eval('active', True),
}
DEPENDS = ['active']

__all__ = ['BankAccount']
__metaclass__ = PoolMeta

class BankAccount:
    'Bank Account'
    __name__ = 'bank.account'
    bank_country = fields.Selection(BANK_COUNTRIES, 'Bank Country', states=STATES,
        depends=DEPENDS,
        help="Setting Bank country will enable validation of the Bank code.",
        translate=False)
    bank_number = fields.Function(fields.Char('Bank Number',
        on_change_with=['code', 'bank_country']), 'get_bank_number',
        searcher='search_bank_number')

    @classmethod
    def __setup__(cls):
        super(BankAccount, cls).__setup__()
        cls._constraints += [
            ('check_bank_number', 'invalid_bank_number'),
        ]
        cls._error_messages.update({
            'invalid_bank_number': 'Invalid Bank number!',
        })

    def on_change_with_bank_code(self):
        return (self.bank_country or '') + (self.code or '')

    def get_bank_number(self, name):
        return (self.bank_country or '') + (self.code or '')

    @classmethod
    def search_bank_number(cls, name, clause):
        res = []
        value = clause[2]
        for country, _ in BANK_COUNTRIES:
            if isinstance(value, basestring) \
                    and country \
                    and value.upper().startswith(country):
                res.append(('bank_country', '=', country))
                value = value[len(country):]
                break
        res.append(('code', clause[1], value))

    def check_bank_number(self):
        '''
        Check the Bank number depending of the country.
        '''
        if not HAS_BANKNUMBER:
            return True
        if not self.bank_country:
            return True

        code = self.code.replace(' ','')
        if not getattr(banknumber, 'check_code_' + \
                self.bank_country.lower())(code):
            #Check if user doesn't have put country code in code
            if code.startswith(self.bank_country):
                code = code[len(self.bank_country):]
                BankAccount.write([self], {
                    'code': code,
                    })
            else:
                return False
        return True
