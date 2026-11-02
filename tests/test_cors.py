import pytest

from pboot import Pboot
from pboot_cors import CORS, cross_origin


@pytest.fixture
def app():
    app = Pboot(__name__)
    app.config['SECRET_KEY'] = 'test'
    return app


def test_cors_headers_on_matched_resource(app):
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    @app.route('/api/data')
    def data():
        return {'ok': True}

    with app.test_client() as c:
        r = c.get('/api/data', headers={'Origin': 'http://example.com'})

    assert r.status_code == 200
    # origins='*' 时回显请求 Origin 并加 Vary: Origin(与上游 flask-cors 行为一致)
    assert r.headers.get('Access-Control-Allow-Origin') == 'http://example.com'
    assert 'Origin' in r.headers.get('Vary', '')


def test_cors_not_applied_outside_resources(app):
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    @app.route('/other')
    def other():
        return {'other': True}

    with app.test_client() as c:
        r = c.get('/other', headers={'Origin': 'http://example.com'})

    assert r.status_code == 200
    assert 'Access-Control-Allow-Origin' not in r.headers


def test_preflight_request(app):
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    @app.route('/api/data', methods=['POST'])
    def data():
        return {'ok': True}

    with app.test_client() as c:
        r = c.options(
            '/api/data',
            headers={
                'Origin': 'http://example.com',
                'Access-Control-Request-Method': 'POST',
            },
        )

    assert r.status_code == 200
    assert 'POST' in r.headers.get('Access-Control-Allow-Methods', '')


def test_allow_headers_and_expose_headers(app):
    CORS(
        app,
        resources={
            r'/api/*': {
                'origins': '*',
                'allow_headers': ['Content-Type', 'Authorization'],
                'expose_headers': ['Content-Disposition'],
            }
        },
    )

    @app.route('/api/data')
    def data():
        return {'ok': True}

    with app.test_client() as c:
        r = c.get('/api/data', headers={'Origin': 'http://example.com'})

    assert r.headers.get('Access-Control-Expose-Headers') == 'Content-Disposition'


def test_cross_origin_decorator(app):
    @app.route('/deco')
    @cross_origin(origins='*')
    def deco():
        return {'deco': True}

    with app.test_client() as c:
        r = c.get('/deco', headers={'Origin': 'http://example.com'})

    assert r.status_code == 200
    assert r.headers.get('Access-Control-Allow-Origin') == 'http://example.com'
