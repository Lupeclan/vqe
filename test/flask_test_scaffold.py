from pytest import fixture


@fixture
def client(app):
    return app.test_client()
