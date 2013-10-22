from app import db, models
from config import basedir
import csv
import os
from pprint import pprint
import re
import logging

VALID_COLUMNS_RE = ['variety', 'country', 'region', 'sku', 'distributor-url', 'unit-of-measurement', 'quantity', 'price-break-\d+', 'price-\w{3}-\d+', 'description', 'image-url', 'attributes', 'category', 'moq', 'order-multiple', 'max-order', 'on-order-quantity', 'on-order-eta', 'packaging', 'form', 'year', 'grower']

# VALID = {
    # 'variety': {'re': 'variety'},
    # 'country': {'re': 'country'},
    # 'price-break': {'re': 'price-break-\d+'},
# }

class FeedReaderException(Exception):
    pass

class FeedReader:
    # Function to check column headings
    def check_columns(self, feedfilepath):
        # Compile list of regular expressions
        # To Do: Handle letter cases and whitespace
        regexes = map(re.compile, VALID_COLUMNS_RE)

        with open(feedfilepath, 'rb') as csvfile:
            # Get first row - column headers
            cols = csv.reader(csvfile).next()
            
            # Check duplicates
            if len(cols) != len(set(cols)):
                raise FeedReaderException("Duplicate column headings")
            
            # Get column headers that are 'valid'
            valid_cols = [col for col in cols for regex in regexes if regex.match(col)]
            
            # This is arguably a bad way to check for invalid headings
            if len(valid_cols) != len(cols):
                raise FeedReaderException("Invalid column heading")
              
            # Store those column headers
            self.cols = cols


    def __init__(self, feedfilepath):
        self.feedfilepath = feedfilepath
        self.check_columns(feedfilepath)
        
        # To Do: catch errors here
        # should we be keeping a file handle open this long?
        
        self.csvfile = open(feedfilepath, 'rb')
        self.reader = csv.DictReader(self.csvfile)

    def __iter__(self):
        return self

    # Get the next row (iteration)
    def next(self):
        try:
            rowdict = self.reader.next()
        except StopIteration:
            # We're at the end of the file, so close it and stop iteration
            self.csvfile.close()
            raise StopIteration
           
        # Make an empty dictionary to assemble an Offer row
        out = dict()
        
        for col, value in rowdict.iteritems():
            # it would be nice to turn this into a switch/case statement or some neater structure
            
            # To Do: Sanitize all inputs - keys and values
            
            # First - ditch empty values
            if value.strip() == "":
                logging.debug('empty value, ignoring')
        
            # Handle price points
            elif re.match('price-break-\d+', col):
                
                # Figure out the price point index number
                break_index = re.match('price-break-(\d+)', col).group(1)
                
                # Assume USD for now
                # This assumes that the price col is there and we dont really know that. Handle!
                price = float(rowdict['price-usd-%s' % (break_index)])
            
                # Get the quantity
                quantity = float(value)
                
                # Assemble and append to list in dictionary
                try:
                    out['pricebreaks'].append({'quantity': quantity, 'price': price})
                    
                # this is the first time we've gotten a pricebreak, so create the list
                except KeyError:
                    out['pricebreaks'] = [{'quantity': quantity, 'price': price}]
                
            elif re.match('price-\w{3}-\d+', col):
                logging.debug('found price break price point')
                
                
            elif value.strip() == "":
                logging.debug('empty value, ignoring')
            
            elif re.match('min-order|max-order|moq|order-multiple', col):
                try:
                    out[col] = float(value)
                except ValueError:
                    logging.warn('Attempt to convert to float failed')
                    pass
            
            elif col == 'year':
                try:
                    out[col] = int(value)
                except ValueError:
                    logging.warn('Year is invalid')
                    pass
            else:
                out[col] = value
                
        return out


# Given a data feed file, update the DB
def add_data_from_file(id, feedfilepath):
    # Currently this only handles adding data the first time
    # Merging updates is not implemented
    # Should look something like:
    # if sku already in db:
    #   do update - evaluate each column
    # else
    #   add
    # for skus in db and not in file
    #   if mode is DELETE
            # do delete
        # if mode is LEAVE
            # do nothing (log)
        # if mode is ASK??
            # interactive mode?
            
    # Identify distributor and make sure they exist
    # Either crawler is associated with distributor by UUID
    # Or user (file upload) is associated with distributor by UUID
    
    # To Do: check exists
    
    # Get distributor
    d = models.Distributor.query.get(id)
    
    # get each row as a cleaned up dict
    # Really, this is a function for "add models from dictionary"
    for row in FeedReader(feedfilepath):
        
        logging.debug("Add a row")
        pprint(row)
            
        # Check for empty row
        if row == {}:
            logging.warn("blank row, skipping")
            continue
            
        # To Do: check if SKU exists in d.offers
        
        # - Setup Hop -
        # To Do: Fix these exact matches, handle closeness, whitespace, case
        hop = models.Hop.query.filter_by(variety=row['variety'], country=row['country']).first()
        
        if hop is None:
            # Add it
            hop = models.Hop(
                variety = row['variety'],
                country = row['country'],
                # macro_classification
                description = row['description'],
                # description - handle multiple descriptions per hop variety from multiple sources. currently the first description entered "wins" - no good
                )
            
            # No session.add needed - gets included with the Offer
        
        # - Setup PriceBreaks -
        pricebreak_m = []
        for p in row['pricebreaks']:
            pricebreak_m.append(
                models.PriceBreak(quantity=p['quantity'], price=p['price'])
                )
            # No session.add needed - gets included with the Offer

        # - Setup Offer -
        
        # Add required stuff
        o = models.Offer(
            hop = hop,
            distributor = d,
            sku=row['sku'],
            url=row['distributor-url'],
            form = row['form'], # need to clean this up
            #max_order = float(row['max-order']),
            min_order = 0,
            quantity = 1,
            pricebreaks = pricebreak_m,
            )
            
        # Deal with optional items
        try:
            o.region = row['region']
        except KeyError:
            pass
            
        try:
            o.year = row['year']
        except KeyError:
            pass
            
        try:
            o.max_order = row['max-order']
        except KeyError:
            pass    
            
        # Add the offer and associated parts:
        try:
            db.session.add(o)
        except:
            logging.error('DB error, rolling back')
            db.session.rollback()
            raise
        db.session.commit()

        