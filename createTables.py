import psycopg2
from config import config
 
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
    	"""
		CREATE TABLE owner(
			real_estate_id text,
			owner_1 text,
			owner_2 text,
			mailing_address_1 text,
			mailing_address_2 text,
			mailing_address_3 text
		)
    	""",
    	""" 
    	CREATE TABLE property(
    		real_estate_id, 
    		location_address,
    		location_address_2,
    		old_map,
    		map_scale,
    		vcs,
    		prop_city,
    		fire_dist,
    		township,
    		etj,
    		spec_dist,
    		zoning,
    		hist_id_1,
    		hist_id_2,
    		permit_date,
    		permit_num,
    		deed_date,
    		book_page,
    		rev_stamps,
    		pkg_sale_date,
    		pkg_sale_price,
    		land_sale_date,
    		and_sale_price
    	)
		""",
		"""
		CREATE TABLE tax_info(
			real_estate_id,
			land_value, 
			building_value,
			tax_relief,
			land_use_value,
			use_value_deferment,
			historic_deferment,
			total_deferred_value,
			use_hist_tax_relief, 
			total_value
		)
		""",
		"""
		CREATE TABLE building(
			real_estate_id,
			recycle_units,
			apt_sc_sqft,
			building_type,
			units,
			heated_area,
			story_height,
			style,
			basement,
			exterior,
			const_type,
			heating,
			air_cond,
			plumbing,
			base_bldg_value,
			grade,
			cond_percent, 
			market_adj1,
			market_adj2,
			accrued_percent,
			incomplete_code,
			card1_value,
			other_cards,
			year_blt,
			eff_year,
			addns,
			remod,
			int_adjust,
			other_features
		)
		""",
		"""
		CREATE TABLE land(
			real_estate_id,
			land_class,
			soil_class,
			deeded_acreage,
			calc_acreage,
			farm_use_year,
			farm_use_flag
		)
		""",
		"""
		CREATE TABLE sales(
			real_estate_id,
			account,
			location_address,
			dist,
			b_type,
			built,
			size,
			story_hgt,
			price,
			last_sold
		)
		""",
		"""
		CREATE TABLE tax_bill(
			real_estate_id,
			account_num,
			amount_paid,
			paid_date,
			amount_due,
			due_date, 
			orig_due_date,
			interest_begins
		)
	""")
conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
 
if __name__ == '__main__':
    create_tables()