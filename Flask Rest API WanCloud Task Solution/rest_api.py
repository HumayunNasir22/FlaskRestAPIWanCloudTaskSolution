from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class TotalDayModel(db.Model):
	country= db.Column(db.String(100), primary_key=True)
	confirmed = db.Column(db.Integer, nullable=False)
	deaths = db.Column(db.Integer, nullable=False)
	recovered = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"TotalDayModel(confirmed = {confirmed}, deaths = {deaths}, recovered = {recovered})"

class GeneralStatsModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	total= db.Column(db.String(200), nullable=False)
	recovered= db.Column(db.String(200), nullable=False)
	deaths= db.Column(db.String(200), nullable=False)
	current_infects=db.Column(db.String(200), nullable=False)

	def __repr__(self):
		return f"GeneralStatsModel(total = {total}, recovered = {recovered}, deaths = {deaths}, current_infects={current_infects})"

class DataDateModel(db.Model):
	date=db.Column(db.String, primary_key=True)
	confirmed = db.Column(db.Integer, nullable=False)
	deaths = db.Column(db.Integer, nullable=False)
	recovered = db.Column(db.Integer, nullable=False)
	active = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"DataDateModel(date = {date}, confirmed = {confirmed}, deaths = {deaths}, recovered={recovered},active={active})"


db.create_all()


day_put_args = reqparse.RequestParser()
day_put_args.add_argument("confirmed", type=int, help="Confirmed Cases required", required=True)
day_put_args.add_argument("deaths", type=int, help="Dead Cases required", required=True)
day_put_args.add_argument("recovered", type=int, help="Recovered Cases required", required=True)

day_update_args = reqparse.RequestParser()
day_update_args.add_argument("confirmed", type=int, help="Confirmed Cases required")
day_update_args.add_argument("deaths", type=int, help="Dead Cases required")
day_update_args.add_argument("recovered", type=int, help="Recovered Cases required")

stat_put_args = reqparse.RequestParser()
stat_put_args.add_argument("total", type=str, help="Total Cases required", required=True)
stat_put_args.add_argument("recovered", type=str, help="Recovered Cases required", required=True)
stat_put_args.add_argument("deaths", type=str, help="Dead Cases required", required=True)
stat_put_args.add_argument("current_infects", type=str, help="Current Infects Cases required", required=True)


date_put_args = reqparse.RequestParser()
date_put_args.add_argument("date", type=str, help="Date required", required=True)
date_put_args.add_argument("confirmed", type=int, help="Confirmed Cases required", required=True)
date_put_args.add_argument("deaths", type=int, help="Dead required", required=True)
date_put_args.add_argument("recovered", type=int, help="Recovered required", required=True)
date_put_args.add_argument("active", type=int, help="Active Cases required", required=True)

date_update_args = reqparse.RequestParser()
date_update_args.add_argument("date", type=str, help="Date required")
date_update_args.add_argument("confirmed", type=int, help="Confirmed Cases required", required=True)
date_update_args.add_argument("deaths", type=int, help="Dead required", required=True)
date_update_args.add_argument("recovered", type=int, help="Recovered required", required=True)
date_update_args.add_argument("active", type=int, help="Active Cases required", required=True)


resource_fields = {
	'country': fields.String,
	'confirmed': fields.Integer,
	'deaths': fields.Integer,
	'recovered': fields.Integer
}

resource_fields1={
     'id': fields.Integer,
     'total':fields.String,
     'recovered':fields.String,
     'deaths':fields.String,
     'current_infects':fields.String
	
}

resource_fields2={
     'date':fields.String,
     'confirmed':fields.String,
     'deaths':fields.String,
     'recovered':fields.String,
     'active':fields.String
	
}

class TotalCaseDay(Resource):
	@marshal_with(resource_fields)
	def get(self, countryName):
		result = TotalDayModel.query.filter_by(country=countryName).first()
		if not result:
			abort(404, message="Could not find data with that country")
		return result

	@marshal_with(resource_fields)
	def put(self, countryName):
		args = day_put_args.parse_args()
		result = TotalDayModel.query.filter_by(country=countryName).first()
		if result:
			abort(409, message="Country Already Presents...")

		day = TotalDayModel(country=countryName, confirmed=args['confirmed'], deaths=args['deaths'], recovered=args['recovered'])

		db.session.add(day)
		db.session.commit()
		return day, 201

	@marshal_with(resource_fields)
	def patch(self, countryName):
		args = day_update_args.parse_args()
		result = TotalDayModel.query.filter_by(country=countryName).first()
		if not result:
			abort(404, message="Country doesn't exist, cannot update")

		if args['confirmed']:
			result.confirmed = args['confirmed']
		if args['deaths']:
			result.deaths = args['deaths']
		if args['recovered']:
			result.recovered= args['recovered']

		db.session.commit()

		return result

class Stats(Resource):
	@marshal_with(resource_fields1)
	def get(self,stat_id):
		result = GeneralStatsModel.query.all()
		result = GeneralStatsModel.query.filter_by(id=stat_id).first()
		if not result:
			abort(404, message="Could not find stats with that id")
		return result

	@marshal_with(resource_fields1)
	def put(self,stat_id):
		args = stat_put_args.parse_args()
		result = GeneralStatsModel.query.filter_by(id=stat_id).first()
		if result:
			abort(409, message="Stat id taken...")
		stat= GeneralStatsModel(id=stat_id, total=args['total'],recovered=args['recovered'],deaths=args['deaths'],current_infects=args['current_infects'])
		db.session.add(stat)
		db.session.commit()
		return stat, 201

class DataDate(Resource):
	@marshal_with(resource_fields2)
	def get(self, Date):
		result = DataDateModel.query.filter_by(date=Date).first()
		if not result:
			abort(404, message="Could not find data with that date!")
		return result

	@marshal_with(resource_fields2)
	def put(self, Date):
		args = date_put_args.parse_args()
		result = DataDateModel.query.filter_by(date=Date).first()
		if result:
			abort(409, message="Date Already Presents...")

		newdata = DataDateModel(date=Date, confirmed=args['confirmed'], deaths=args['deaths'], recovered=args['recovered'],active=args['active'])

		db.session.add(newdata)
		db.session.commit()
		return newdata, 201

	@marshal_with(resource_fields2)
	def patch(self, Date):
		args = date_update_args.parse_args()
		result = DataDateModel.query.filter_by(date=Date).first()
		if not result:
			abort(404, message="Date doesn't exist, cannot update")

		if args['confirmed']:
			result.confirmed = args['confirmed']
		if args['deaths']:
			result.deaths = args['deaths']
		if args['recovered']:
			result.recovered= args['recovered']
		if args['active']:
			result.active= args['active']

		db.session.commit()


	


api.add_resource(TotalCaseDay, "/day/<string:countryName>")
api.add_resource(Stats,"/stats/<int:stat_id>")
api.add_resource(DataDate,"/datedata/<string:Date>")

if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0")