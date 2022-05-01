from openfisca_us.model_api import *


class state_income_tax_exempt_limit(Variable):
    value_type = float
    entity = TaxUnit
    label = "Income limit to be exempt from state income tax"
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).states.tax.income.exempt
        state = tax_unit.household("state_code_str", period)
        mars = tax_unit("marital_status", period)
        dependents = tax_unit("tax_unit_dependents", period)
        base_limit = p.limit[state][mars]
        dep_limit = dependents * p.dependent[state][mars]
        return base_limit + dep_limit