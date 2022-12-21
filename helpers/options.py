

class ModelFieldOptions:

    LOAN_STATUS = (
        ('active','Active'),
        ('completed','Completed'),
    )
    LOAN_REASON = (
        ('education','Education'),
        ('medical','Medical'),
        ('rent','Rent'),
        ('travel','Travel'),
        ('business','Business'),
        ('goods','Goods'),
        ('event','Event'),
        ('household','Household'),
        ('other','other'),
    )
    LOAN_APPLICATION_STATUS = (
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
    )
    
    LOAN_REPAYMENT_TYPE = (
        ('auto','Auto'),
        ('custom','Custom'),
    )
    LOAN_REPAYMENT_STATUS = (
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','Failed'),
    )


    OFFER_TYPE = (
        ('month','Month'),
        ('year','Year')
    ) 


    EMPLOYMENT_STATUS = (
        ('unemployed','Unemployed'),
        ('entrepreneur','Entrepreneur'),
        ('employed','Employed'),
    )
    EDUCATIONAL_STATUS = (
        ('graduate','Graduate'),
        ('under_graduate','Under graduate'),
        ('post_graduate','Post graduate'),
        ('high_school','High school'),
        ('other','other'),
    )
    MARITAL_STATUS = (
        ('single','Single'),
        ('married','Married'),
        ('divorce','Divorce'),
    )
    RESIDENT_TYPE = (
        ('owned','Owned'),
        ('rented','Rented'),
    )
    CHILDREN_COUNT = (
        ('one','One'),
        ('two','Two'),
        ('other','Three and above'),
    )


    KYC_TYPE = [
        'BVN','NIN'
    ]