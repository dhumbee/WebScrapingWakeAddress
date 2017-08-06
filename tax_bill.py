# tax bill class

class Tax_Bill:

	def __init__(self, real_estate_id, account_num,
				amount_paid, paid_date, amount_due, due_date, 
				orig_due_date, interest_begins):
		self.__real_estate_id = real_estate_id
		self.__account_num = account_num
		self.__amount_paid = amount_paid
		self.__paid_date = paid_date
		self.__amount_due = amount_due
		self.__due_date = due_date
		self.__orig_due_date = orig_due_date
		self.__interest_begins = interest_begins