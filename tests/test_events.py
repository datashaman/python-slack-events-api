import time
import pytest

def test_event_emission(adapter):
    test_event_emission.event_handled = False

    # Events should trigger an event
    @adapter.on('reaction_added')
    def event_handler(event_data):
        test_event_emission.event_handled = True

        event = event_data['event']
        assert event["reaction"] == 'grinning'

    data = pytest.reaction_event_fixture
    timestamp = int(time.time())
    signature = pytest.create_signature(adapter.signing_secret, timestamp, data)

    with adapter.server.test_client() as client:
        res = client.post(
            '/slack/events',
            data=data,
            content_type='application/json',
            headers={
                'X-Slack-Request-Timestamp': timestamp,
                'X-Slack-Signature': signature
            }
        )
        assert res.status_code == 200

    assert test_event_emission.event_handled
