template = {
    "swagger": "2.0",
    "info": {
        "title": "GreenHouse REST API",
        "description": "API for controlling smart greenhouse",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "diaconu.andrei99@gmail.com",
            "url": "http://www.linkedin.com/in/andrei-diaconu-53a074216",
        },
        "termsOfService": "https://github.com/DiaconuAndr3i/Velvere",
        "version": "1.0"
    },
    "basePath": "/api",
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}