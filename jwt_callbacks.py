from flask import jsonify
from blocklist import BLOCKLIST

def register_jwt_callbacks(jwt):

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        #! this function checks if the token is in the blocklist.
        #! if it is, it returns True and the token is revoked.
        #! if it is not, it returns False and the token is not revoked.
        return jwt_payload["jti"] in BLOCKLIST

    #! I can add extra information to the JWT token when it is created.
    #! This is useful for adding user roles or permissions to the token.
    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     if identity == 1: #! admin user
    #         return {"is_admin": True}
    #     return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )
    # JWT configuration ends
