import psycopg2
from config import config
 
 
def create_tables():
    #create tables in the PostgreSQL database
    commands = (
    	"""
		CREATE TABLE owner(
			real_estate_id text PRIMARY KEY,
			owner_1 text,
			owner_2 text,
			mailing_address_1 text,
			mailing_address_2 text,
			mailing_address_3 text
		)
    	""",
    	""" 
    	CREATE TABLE property(
    		real_estate_id text PRIMARY KEY, 
    		location_address text,
    		location_address_2 text,
    		old_map text,
    		map_scale text,
    		vcs text,
    		prop_city text,
    		fire_dist text,
    		township text,
    		etj text,
    		spec_dist text,
    		zoning text,
    		hist_id_1 text,
    		hist_id_2 text,
    		permit_date date,
    		permit_num text,
    		deed_date date,
    		book_page text,
    		rev_stamps text,
    		pkg_sale_date date,
    		pkg_sale_price numeric,
    		land_sale_date date,
    		and_sale_price numeric
    	)
		""",
		"""
		CREATE TABLE tax_info(
			real_estate_id text PRIMARY KEY,
			land_value numeric, 
			building_valuenumeric,
			tax_relief numeric,
			land_use_value numeric,
			use_value_deferment numeric,
			historic_deferment numeric,
			total_deferred_value numeric,
			use_hist_tax_relief numeric, 
			total_value numeric
		)
		""",
		"""
		CREATE TABLE building(
			real_estate_id text PRIMARY KEY,
			recycle_units text,
			apt_sc_sqft text,
			building_type text,
			units text,
			heated_area text,
			story_height text,
			style text,
			basement text,
			exterior text,
			const_type text,
			heating text,
			air_cond text,
			plumbing text,
			base_bldg_value numeric,
			grade text,
			cond_percent text, 
			market_adj1 text,
			market_adj2 text,
			accrued_percent text,
			incomplete_code text,
			card1_value text,
			other_cards text,
			year_blt numeric,
			eff_year date,
			addns text,
			remod text,
			int_adjust text,
			other_features text
		)
		""",
		"""
		CREATE TABLE land(
			real_estate_id text PRIMARY KEY,
			land_class text,
			soil_class text,
			deeded_acreage text,
			calc_acreage text,
			farm_use_year date,
			farm_use_flag text
		)
		""",
		"""
		CREATE TABLE sales(
			real_estate_id text PRIMARY KEY,
			account text,
			location_address text,
			dist text,
			b_type text,
			built text,
			size text,
			story_hgt text,
			price numeric,
			last_sold text
		)
		""",
		"""
		CREATE TABLE tax_bill(
			real_estate_id text PRIMARY KEY,
			account_num text,
			amount_paid numeric,
			paid_date date,
			amount_due numeric,
			due_date date, 
			orig_due_date date,
			interest_begins date
		)
		"""
	)
	print("hello")
	conn = None
    try:
    	# connect to the PostgreSQL server
    	conn = psycopg2.connect("dbname=Wake_County_Real_Estate user=postgres")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            #cur.execute(command)
            print(command)
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