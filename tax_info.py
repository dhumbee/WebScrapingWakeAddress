# Tax class 

class Tax_Info:

	def __init__(self, real_estate_id, land_value, building_value,
				tax_relief, land_use_value, use_value_deferment,
				historic_deferment, total_deferred_value, 
				use_hist_tax_relief, total_value):
		self.__real_estate_id = real_estate_id
		self.__land_value = land_value
		self.__building_value = building_value
		self.__tax_relief = tax_relief
		self.__land_use_value = land_use_value
		self.__use_value_deferment = use_value_deferment
		self.__historic_deferment = historic_deferment
		self.__total_deferred_value = total_deferred_value
		self.__use_hist_tax_relief = use_hist_tax_relief
		self.__total_value = total_value		