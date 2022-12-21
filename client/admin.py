from django.contrib import admin
from .models import (
    Loan ,LoanApplication,LoanOffer,LoanRepayment,LoanSchedule,LoanScoreBoard,
    Transaction , ScoreCriteriaCategory ,ScoreCriteriaOption , Offer
)
# Register your models here.


class ScoreCriterialStacked(admin.StackedInline):
    model = ScoreCriteriaOption

class ScoreCriteriaModelAdmin(admin.ModelAdmin):
    inlines = [ScoreCriterialStacked]  



class LoanLoanScheduleStacked(admin.StackedInline):
    model = LoanSchedule

class LoanApplicationModelAdmin(admin.ModelAdmin):
    inlines = [LoanLoanScheduleStacked]    


admin.site.register(Loan, LoanApplicationModelAdmin)
admin.site.register(LoanOffer)
admin.site.register(LoanRepayment)
admin.site.register(LoanSchedule)
admin.site.register(LoanScoreBoard)
admin.site.register(LoanApplication)
admin.site.register(Transaction)
admin.site.register(ScoreCriteriaCategory , ScoreCriteriaModelAdmin )
admin.site.register(ScoreCriteriaOption)
admin.site.register(Offer) 
