from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

# Macro-classification for Hops
CLASS_AROMA = 0
CLASS_BITTER = 1
CLASS_DUAL = 2

# Alembic is set up for DB migrations!!
# When you make a change here, do the following from the flaskapp1 directory (directory above app)
# Run: alembic revision --autogenerate -m "description of change"
# Go check the upgrade script in alembic/versions
# Run: alembic upgrade head
# Version control it!:
# Run: git add .
# Run: git commit -a


# Stuff from mega-tutorial

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True )
    email = db.Column(db.String(120), index = True, unique = True )
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    
    # Required methods for Flask-Login
    
    # is the user allowed to login?
    def is_authenticated(self):
        return True
    
    # is the user allowed to login?
    def is_active(self):
        return True
    
    # return true only for fake users?
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return unicode(self.id)
    
    def __repr__(self):
        return '<User %r>' % (self.nickname)

# Stuff for hopengine:

class Hop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    variety = db.Column(db.String(500)) # variety name
    country = db.Column(db.String(2)) # the two letter ISO country code
    macro_classification = db.Column(db.SmallInteger)
    description = db.Column(db.String(1000))
    __table_args__ = (db.UniqueConstraint('variety', 'country', name='variety_country_unique'),)
    
    def __repr__(self):
        return '<Hop %r %r>' % (self.variety, self.country)
        
class Farm(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(500))
    country = db.Column(db.String(2)) # the two letter ISO country code
    url = db.Column(db.String(1000))

    def __repr__(self):
        return '<Farm %r>' % (self.name)
        
class Distributor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(500))
    country = db.Column(db.String(2)) # the two letter ISO country code
    url = db.Column(db.String(1000))
    
    id_farm = db.Column(db.Integer, db.ForeignKey('farm.id'))
    farm = db.relationship('Farm', backref=db.backref('distributors', lazy='dynamic'))
    
    def __repr__(self):
        return '<Distributor %r>' % (self.name)

class UnitOfMeasurement(db.Model):
    # Should we make symbol the primary key?
    # Do we want to enforce a unique symbol for units? They're not unique across disciplines. But we definitely want to do something better here to protect data integrety. 
    # Maybe name.

    __tablename__ = 'unit_of_measurement' # flask-sqlalchemy would do this automagically, but i like the name to be explicit when going from CamelCase to camel_case
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(500))
    symbol = db.Column(db.String(20), unique = True)
    
    def __repr__(self):
        return '<UnitOfMeasurement %r>' % (self.name)
        
class Offer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sku = db.Column(db.String(500))
    url = db.Column(db.String(1000))
    form = db.Column(db.String(500)) # whole, pellet, etc... need to enum this...
    packaging = db.Column(db.String(500)) # mylar, plasic, nitro flushed... need to enum this...
    year = db.Column(db.Integer) # what year harvested
    max_order = db.Column(db.Float)
    min_order = db.Column(db.Float)
    pre_sale = db.Column(db.Boolean, default=False)
    quantity = db.Column(db.Float)
    organic = db.Column(db.Boolean, default=False)
    region = db.Column(db.String(500)) # like state or "pacific nw"... need to enum this...
    
    id_hop = db.Column(db.Integer, db.ForeignKey('hop.id'))
    hop = db.relationship('Hop', backref=db.backref('offers', lazy='dynamic'))
    
    id_distributor = db.Column(db.Integer, db.ForeignKey('distributor.id'))
    distributor = db.relationship('Distributor', backref=db.backref('offers', lazy='dynamic'))
    
    id_farm = db.Column(db.Integer, db.ForeignKey('farm.id'))
    farm = db.relationship('Farm', backref=db.backref('offers', lazy='dynamic'))
    
    id_unit = db.Column(db.Integer, db.ForeignKey('unit_of_measurement.id'))
    unit = db.relationship('UnitOfMeasurement', foreign_keys=[id_unit])
    # no backref - I never need to go from unitofmeasurement to where it's used
    
    id_currency = db.Column(db.Integer, db.ForeignKey('unit_of_measurement.id'))
    currency = db.relationship('UnitOfMeasurement', foreign_keys=[id_currency])
    
    def __repr__(self):
        return '<Offer %s>' % (self.sku)
    
class PriceBreak(db.Model):
    # tablename is price_break
    # To do: determine appropriate unique constraints here 
    # Joint unique constraint on quantity and offer?
    id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
    
    id_offer = db.Column(db.Integer, db.ForeignKey('offer.id'))
    offer = db.relationship('Offer', backref=db.backref('pricebreaks', lazy='dynamic'))
    
    def __repr__(self):
        return '<PriceBreak %s %s>' % (self.quantity, self.price)
        