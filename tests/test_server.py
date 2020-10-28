from synchro import Server

from helpers import diff, patch


class TestServerInit:
    """
    Test the __init__ function of the Server class
    """

    def test_defaults(self):
        """Test the __init__ function with default arguments"""
        s = Server()
        assert s.data == ""

    def test_custom_data(self):
        """Test the __init__ function with a custom data argument"""
        data = "cats and dogs"
        s = Server(data)
        assert s.data == data

    def test_custom_diff_func(self):
        """Test the __init__ function with a custom diff argument"""

        def data(doc1, doc2):
            pass

        s = Server(diff=data)
        assert s._diff is data

    def test_custom_patch_func(self):
        """Test the __init__ function with a custom patch argument"""

        def data(patch, doc):
            pass

        s = Server(patch=data)
        assert s._patch is data


class TestServerMain:
    """
    Test the connection, receive and receive_a functions of Server
    """

    def test_connection(self):
        """Test the connection function"""
        data = "flying cows"
        s = Server(data)
        conn = s.connection()
        result = {
            "id": 1,
            "data": data,
            "version": [0, 0],
        }

    def test_receive_normal(self):
        """
        Test the receive function under normal operation by simulating normal
        communication between two clients and a server
        """
        s = Server("i like to eet fud.", diff=diff, patch=patch)
        c1 = s.connection()
        c2 = s.connection()

        diff1 = diff("i like to eet fud.", "i like to eat fud.")
        data1 = {
            "id": 1,
            "version": [0, 0],
            "edits": [{"version": [0, 0], "diff": diff1}],
        }
        result1 = s.receive(data1)
        # the server sends a response saying "I received version one"
        expected1 = {"diff": "", "version": [1, 0], "rollback": False}

        diff2 = diff("i like to eet fud.", "i like to eet food.")
        data2 = {
            "id": 2,
            "version": [0, 0],
            "edits": [{"version": [0, 0], "diff": diff2}],
        }
        result2 = s.receive(data2)
        # the server sends a response saying
        # "I received version one, but you must use the diff to get up to date with the latest changes"
        expected2 = {
            "diff": "@@ -4,16 +4,16 @@\n ike to e\n-e\n+a\n t food.\n",
            "version": [1, 0],
            "rollback": False,
        }

        diff3 = diff("i like to eat fud.", "I like to eat fud.")
        data3 = {
            "id": 1,
            "version": [1, 1],
            "edits": [{"version": [1, 1], "diff": diff3}],
        }
        result3 = s.receive(data3)
        expected3 = {
            "diff": "@@ -12,7 +12,8 @@\n at f\n-u\n+oo\n d.\n",
            "version": [2, 1],
            "rollback": False,
        }

        assert expected1 == result1 and expected2 == result2 and expected3 == result3

    def test_receive_client_send_issue(self):
        """
        Test the receive function under the circumstances that the client's data
        was never received by the server
        """
        s = Server("i like to eet fud.", diff=diff, patch=patch)
        c1 = s.connection()

        # as the connection keeps timing out, the edit stack becomes bigger,
        # eventually becoming "data". There are 2 attempts before the server
        # finally receives the information
        diff1 = diff("i like to eet fud.", "i like to eat fud.")
        diff2 = diff("i like to eat fud.", "I like to eat fud.")
        diff3 = diff("I like to eat fud.", "I like to eat food.")
        data = {
            "id": 1,
            "version": [2, 0],
            "edits": [
                {"version": [0, 0], "diff": diff1},
                {"version": [1, 0], "diff": diff2},
                {"version": [2, 0], "diff": diff3},
            ],
        }
        result = s.receive(data)
        expected = {"diff": "", "version": [3, 0], "rollback": True}
        assert result == expected

    def test_receive_server_send_issue(self):
        """
        Test the receive function under the circumstances that the server's data
        was never received by the client
        """
        s = Server("i like to eet fud.", diff=diff, patch=patch)
        c1 = s.connection()

        # the client sends a successful response to the server. However, the
        # client never recieves a response. The slient sends another request
        # with both edits (since they are stored in the edit stack). The
        # server notices that the server version sent from the client is behind,
        # so performs a rollback. Everything then goes back to normal
        diff1 = diff("i like to eet fud.", "i like to eat fud.")
        diff2 = diff("i like to eat fud.", "I like to eat fud.")
        data = {
            "id": 1,
            "version": [1, 0],
            "edits": [
                {"version": [0, 0], "diff": diff1},
                {"version": [1, 0], "diff": diff2},
            ],
        }
        result = s.receive(data)
        expected = {"diff": "", "version": [2, 0], "rollback": True}
        assert result == expected


class TestServerCleanup:
    """
    Test the Server cleanup functions responsible for removing clients and
    reseting the client group
    """

    def test_close_connection(self):
        """
        Test the close_connection method responsible for removing a client
        by id
        """
        s = Server()
        c = s.connection()
        assert s.close_connection(c["id"]) == c["id"] and s._clients == set()

    def test_reset(self):
        """Test the reset method that clears all connections"""
        s = Server()
        c = s.connection()
        c1 = s.connection()
        assert s.reset() == {c["id"], c1["id"]} and s._clients == set()
