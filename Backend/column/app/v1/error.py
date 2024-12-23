from flask import jsonify
from werkzeug.exceptions import HTTPException



#custom error handler for common HTTP errors

def register_error_handlers(app):

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({"error": "Resource not found", "status_code": 404}), 404

	@app.errorhandler(500)
	def internal_server_error(error):
		return jsonify({"error": "Internal server error", "status_code": 500}), 500

	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({"error": "Bad request", "status_code": 400}), 400

	@app.errorhandler(403)
	def forbidden(error):
		return jsonify({"error": "You don't have permission to access this resource", "status_code": 403}), 403

	#Catch any uncaught error gobally
	@app.errorhandler(Exception)
	def handle_generic_exceptions(error):
		if isinstance(error, HTTPException):
			return jsonify({"error": error.description, "status_code": error.code}), error.code
		return jsonify({"error": "Something went wrong", "status_code": 500}), 500