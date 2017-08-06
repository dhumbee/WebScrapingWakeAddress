# Building class

class Building:

	def __init__(self, real_estate_id, recycle_units, apt_sc_sqft,
				 building_type, units, heated_area, story_height, style,
				 basement, exterior, const_type, heating, air_cond, 
				 plumbing, base_bldg_value, grade, cond_percent, market_adj1,
				 market_adj2, accrued_percent, incomplete_code, card1_value,
				 other_cards, year_blt, eff_year, addns, remod, int_adjust,
				 other_features):
		self.__real_estate_id = real_estate_id
		self.__recycle_units = recycle_units
		self.__apt_sc_sqft = apt_sc_sqft
		self.__building_type = building_type
		self.__units = units		
		self.__heated_area = heated_area
		self.__story_height = story_height
		self.__style = style
		self.__basement = basement
		self.__exterior = exterior
		self.__const_type = const_type
		self.__heating = heating
		self.__air_cond = air_cond
		self.__plumbing = plumbing
		self.__base_bld_value = base_bldg_value
		self.__grade = grade
		self.__cond_percent = cond_percent
		self.__market_adj1 = market_adj1
		self.__market_adj2 = market_adj2
		self.__accrued_percent = accrued_percent
		self.__incomplete_code = incomplete_code
		self.__card1_value = card1_value
		self.__other_cards = other_cards
		self.__year_blt = year_blt
		self.__eff_year = eff_year
		self.__addns = addns
		self.__remod = remod
		self.__int_adjust = int_adjust
		self.__other_features = other_features
