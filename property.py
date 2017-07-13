#Property_Class

class Property:

	def __init__(self, real_estate_id, prop_desc, location_address, 
		location_city, location_state, location_zip, old_map, map_scale,
		vcs, prop_city, fire_dist, township, etj, spec_dist, zoning,
		hist_id_1, hist_id_2, permit_date, permit_num, deed_date,
		book_page, rev_stamps, pkg_sale_date, pkg_sale_price, total_assessed_value):
		self.__real_estate_id = real_estate_id
		self.__prop_desc = prop_desc
		self.__location_address = location_address
		self.__location_city = location_city
		self.__location_state = location_state
		self.__location_zip = location_zip
		self.__old_map = old_map
		self__map_scale = map_scale
		self.__vcs = vcs
		self.__prop_city = prop_city
		self.__fire_dist = fire_dist
		self.__township = township
		self.__etj = etj
		self.__spec_dist = spec_dist
		self.__zoning = zoning
		self.__hist_id_1 = hist_id_1
		self.__hist_id_2 = hist_id_2
		self.__permit_date = permit_date
		self.__permit_num = permit_num
		self.__deed_date = deed_date
		self.__book_page = book_page
		self.__rev_stamps = rev_stamps
		self.__pkg_sale_date = pkg_sale_date
		self.__pkg_sale_price = pkg_sale_price
		self.__total_assessed_value = total_assessed_value
