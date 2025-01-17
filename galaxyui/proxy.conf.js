const PROXY_CONFIG = {
    "/api": {
        'target': "http://localhost:8089",
        'secure': false
    },
    "/static": {
        'target': "http://localhost:8089",
        'secure': false
    },
    "/admin": {
        'target': "http://localhost:8089",
        'secure': false
    },
    "/accounts": {
        'target': "http://localhost:8089",
        'secure': false
    },
    "/metrics": {
        'target': "http://localhost:8089",
        'secure': false
    },
    "/download": {
        'target': "http://localhost:8089",
        'secure': false
    }
}

module.exports = PROXY_CONFIG;
