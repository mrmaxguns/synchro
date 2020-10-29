from synchro import DSClient
from helpers import diff

import pytest


class TestClientInit:
    """Test the __init__ method of the DSClient class"""

    def test_defaults(self):
        """Test the default configuration and parameters"""
        c = DSClient(1, "to be or not to be", [0, 0])
        assert c.id == 1


class TestDSClientMain:
    """Test the main methods of the DSClient class"""

    def test_commit_once(self):
        """Test the commit method during normal operation"""
        c = DSClient(1, "hy there", [0, 0])

        commit = c.commit("hi there")
        diff_data = diff("hy there", "hi there")
        expected = {
            "id": 1,
            "version": [0, 0],
            "edits": [{"version": [0, 0], "diff": diff_data}],
        }

        assert commit == expected

    def test_multiple_commits(self):
        """
        Test when multiple commits are sent without a server response, usually
        due to a timeout
        """
        c = DSClient(1, "thrust the time of your life", [0, 0])

        commit1 = c.commit("trust the time of your life")
        diff1 = diff("thrust the time of your life", "trust the time of your life")
        commit2 = c.commit("trust the timing of your life")
        diff2 = diff("trust the time of your life", "trust the timing of your life")

        expected = {
            "id": 1,
            "version": [1, 0],
            "edits": [
                {"version": [0, 0], "diff": diff1},
                {"version": [1, 0], "diff": diff2},
            ],
        }
        assert commit2 == expected

    def test_update(self):
        """
        Test the update function of the client
        """
        c = DSClient(1, "Yet Another Markup Language", [0, 0])

        commit = c.commit("Yaml Ain't a Markup Language")
        c.update(
            {
                "diff": "@@ -21,8 +21,9 @@\n Language\n+!\n",
                "version": [1, 0],
                "rollback": False,
            }
        )
        assert c.data == "Yaml Ain't a Markup Language!"

    def test_set_data(self):
        """Try setting the data for a client and ensure that you can't do so"""
        c = DSClient(1, "What is your favorite food?", [0, 0])
        with pytest.raises(AttributeError):
            c.data = "What is your favorite color?"
