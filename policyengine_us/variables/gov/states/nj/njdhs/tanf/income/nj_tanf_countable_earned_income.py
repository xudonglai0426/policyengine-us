from policyengine_us.model_api import *


class nj_tanf_countable_earned_income(Variable):
    value_type = float
    entity = SPMUnit
    label = "New Jersey TANF countable earned income"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.NJ

    def formula(spm_unit, period, parameters):
        person = spm_unit.members
        # Get gross earned income.
        gross_earned_income = spm_unit("nj_tanf_gross_earned_income", period)
        p = parameters(
            period
        ).gov.states.nj.njdhs.tanf.income.earned_income_deduction
        months_enrolled_in_tanf = person("months_enrolled_in_tanf", period)
        weekly_hours_worked = person("weekly_hours_worked", period)
        # New Jerset Admin Code 10:90-3.8(b)
        person_meet_higher_work_hours_threshold = (
            weekly_hours_worked >= p.work_hours_threshold
        )
        person_enrolled_in_tanf_for_first_month = (
            months_enrolled_in_tanf <= p.first_month_threshold
        )
        person_enrolled_in_tanf_for_consecutive_months = (
            months_enrolled_in_tanf <= p.consecutive_month_threshold
        ) and (months_enrolled_in_tanf > p.first_month_threshold)
        person_enrolled_in_tanf_for_additional_months_with_work_hours_over_20 = (
            months_enrolled_in_tanf > p.consecutive_month_threshold
            and person_meet_higher_work_hours_threshold
        )
        person_enrolled_in_tanf_for_additional_months_with_Work_hours_below_20 = (
            months_enrolled_in_tanf > p.first_month_threshold
        )
        if person_meet_higher_work_hours_threshold:
            if person_enrolled_in_tanf_for_first_month:
                return gross_earned_income * (
                    1 - p.higher_work_hours.first_month_percent
                )
            elif person_enrolled_in_tanf_for_consecutive_months:
                return gross_earned_income * (
                    1 - p.higher_work_hours.consecutive_month_percent
                )
            elif person_enrolled_in_tanf_for_additional_months_with_work_hours_over_20:
                return gross_earned_income * (
                    1 - p.higher_work_hours.additional_percent
                )
        else:
            if person_enrolled_in_tanf_for_first_month:
                return gross_earned_income * (
                    1 - p.lower_work_hours.first_month_percent
                )
            elif person_enrolled_in_tanf_for_additional_months_with_Work_hours_below_20:
                return gross_earned_income * (
                    1 - p.lower_work_hours.additional_percent
                )
