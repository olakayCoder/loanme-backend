from typing import Dict
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
import os 
User = get_user_model()


def create_jwt_pair_for_user(user: User):
    """
    Obtains pairs of tokens ie ( access and refresh for the user)
    :param ::: user >> an object of the user to create token for
    """
    refresh = RefreshToken.for_user(user)

    tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}

    return tokens



INVALID_CODES = [111111,222222,333333,444444,555555,666666,777777,888888,999999]


class ScoreCriterial:

    SCORE_POINT: Dict =  {

    # marital
    'personal_marital_single':5,
    'personal_marital_married':5,
    'personal_marital_divorce':5,

    # children
    'personal_children_1':5,
    'personal_children_2':5,
    'personal_children_3_above':5,

    # gender
    'personal_gender_male':5,
    'personal_gender_female':5,

    # education
    'e&e_education_level_undergraduate':5,
    'e&e_education_level_graduate':5,
    'e&e_education_level_olevel':5,
    'e&e_education_level_technical':5,

    # employment
    'e&e_employment_employed':5,
    'e&e_employment_unemployed':5,
    'e&e_employment_entrepreneur':5,

    # income/salary
    'e&e_monthly_income_below_50k':5,
    'e&e_monthly_income_below_100k':5,
    'e&e_monthly_income_below_200k':5,
    'e&e_monthly_income_below_500k':5,
    'e&e_monthly_income_below_1m':5,
    'e&e_monthly_income_below_other':5,

    # residence
    'address_residence_owned':5,
    'address_residence_rented':5,

    # residence price
    'address_rent_per_yer_below_100k':5,
    'address_rent_per_yer_below_200k':5,
    'address_rent_per_yer_below_500k':5,
    'address_rent_per_yer_below_1m':5,
    'address_rent_per_yer_below_other':5,


    # loan reason
    'loan_reason_education':5,
    'loan_reason_medical':5,
    'loan_reason_rent':5,
    'loan_reason_travel':5,
    'loan_reason_business':5,
    'loan_reason_goods':5,
    'loan_reason_event':5,
    'loan_reason_household':5,
    'loan_reason_other':5,
 
}




class LoanApplicationScore:

    def score_application(data:Dict)-> int:
        """
        Score user loan application data
        :param ::: data >> dictionary of the response data

        We score using the following option choose in the following choices.
        ### marital , children , gender , education , employment , income/salary
        ### residence_type , residence_price , loan reason
        """
        if not isinstance(data, Dict ):
            raise TypeError('Invalid argument type . %d is not of type dict' % (data))
        # print(data)
        return None





def get_current_timestamp():
    current_ = datetime.datetime.now()
    return f'{current_.year}{current_.month}{current_.day}{current_.hour}{current_.minute}{current_.second}-{current_.year}'