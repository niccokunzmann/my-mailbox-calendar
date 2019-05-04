import pytest

@pytest.mark.parametrize("email_names,attributes", [
    # Thunderbird
    ( ["thunderbird_1"], {
      "summary": "Event", "description":None
    }),
    ( ["thunderbird_2", "thunderbird_2_edited"], {
      "summary": "Edited Event", "description":"now has a description"
    }),
    ( ["thunderbird_2", "thunderbird_2_edited"], {
      "summary": "Edited Event", "description":"now has a description"
    }),
    # Lotus Notes
    ( ["lotus_1"], {
      "summary": "test"}),
    ( ["lotus_1", "lotus_1_edited"], {
      "summary": "test - edited"}),
    ( ["lotus_1_edited", "lotus_1"], {
      "summary": "test - edited"}),
])
def test_one_email(emails, email_names, calendar, attributes):
    for email_name in email_names:
        calendar.receive(emails[email_name])
    all_events = calendar.list_events()
    assert len(all_events) == 1
    first_event = all_events[0]
    for attribute, value in attributes.items():
        assert first_event.get(attribute) == value

@pytest.mark.parametrize("email_names", [
  # no input
  [],
  # thunderbird
  ["thunderbird_1", "thunderbird_1_canceled"],
  # lotus notes
  ["lotus_2", "lotus_2_canceled"],
])
def test_email_cancelled(emails, email_names, calendar):
    for email_name in email_names:
        calendar.receive(emails[email_name])
    assert calendar.list_events() == []
    
