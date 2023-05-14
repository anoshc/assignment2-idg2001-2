import json

def test_index(app, client):
    res = client.get('/contacts')

    assert res.status_code == 200
    expected = {'message': 'Data uploaded successfully'}
    assert expected == json.loads(res.get_data(as_text=True))
