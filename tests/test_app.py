from .context import housemates


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    housemates.Housemates.run()
    captured = capsys.readouterr()

    assert "Hello World..." in captured.out
