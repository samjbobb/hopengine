# script to add a bunch of test data
import os
from app import db, models
from config import basedir
import data_processing
import logging

# Test data
distributor_list = [
    {'id': 1, 'name': 'Northern Brewer', 'country': 'US', 'url': "http://www.northernbrewer.com/", 'feedfile': 'northernbrewer_feed_file.csv'},
    {'id': 2, 'name': 'Midwest Supplies', 'country': 'US', 'url': "http://www.midwestsupplies.com/", 'feedfile': 'midwestsupplies_feed_file.csv'},
    {'id': 3, 'name': 'Freshops', 'country': 'US', 'url': "http://www.freshops.com/", 'feedfile': 'freshops_feed_file.csv'},
    ]
    
    
    
known_units = [
    {'symbol': 'oz',
    'name': 'US Ounce'
    },
    {'symbol': 'USD',
    'name': 'US Dollar'
    },
    {'symbol': '%',
    'name': 'Percent'
    },
    ]

def delete_all():
    # Delete everything
    # Need to configure ON DELETE CASCADE in models
    # Right now, just do it in order
    
    try: 
        prices = models.PriceBreak.query.delete()
        
        units = models.UnitOfMeasurement.query.delete()
        
        offers = models.Offer.query.delete()
        
        distributors = models.Distributor.query.delete()
        
        farms = models.Farm.query.delete()
        
        hops = models.Hop.query.delete()
    
    except:
        db.session.rollback()
        raise 
        
    db.session.commit()
    
def add_base():

    # Add test data:
    
    # Add sample distributors
    try:

        for distributor in distributor_list:
            d = models.Distributor(
                id=distributor['id'], 
                name=distributor['name'], 
                country=distributor['country'], 
                url=distributor['url']
                )
            db.session.add(d)
            
    except:
        logging.error('DB error, rolling back')
        db.session.rollback()
        raise
        
    db.session.commit()

    # Add sample units
    try:

        for unit in known_units:
            u = models.UnitOfMeasurement(
                name=unit['name'],
                symbol=unit['symbol']
                )
            db.session.add(u)
            
    except:
        logging.error('DB error, rolling back')
        db.session.rollback()
        raise
        
    db.session.commit()
    
    
    # Farm associated with a distributor 
    # dist = models.Distributor(name="Hops Direct", country="US", url='http://www.hopsdirect.com/', farm=models.Farm(name="Puterbaugh Farms", country="US", url="http://www.hopsdirect.com/about/"))

    
def add_from_test_files():
    for distributor in distributor_list:
        feedfilepath = os.path.join(basedir, 'distributor_data', distributor['feedfile'])
        data_processing.add_data_from_file(distributor['id'], feedfilepath)
    
if __name__ == "__main__":
    print "Deleting distributors and re-added test data"
    delete_all()
    add_base()
    add_from_test_files()