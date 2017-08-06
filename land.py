# class Land

class Land:
	
	def __init__(self, real_estate_id, land_class, soil_class,
				deeded_acreage, calc_acreage, farm_use_year,
				farm_use_flag):
		self.__real_estate_id = real_estate_id
		self.__land_class = land_class
		self.__soil_class = soil_class
		self.__deeded_acreage = deeded_acreage
		self.__calc_acreage = calc_acreage		
		self.__farm_use_year = farm_use_year
		self.__farm_use_flag = farm_use_flag