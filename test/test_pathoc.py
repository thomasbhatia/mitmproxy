import json, cStringIO
from libpathod import pathoc, test, version
import tutils


class TestDaemon:
    @classmethod
    def setUpAll(self):
        self.d = test.Daemon(
            staticdir=tutils.test_data.path("data"),
            anchors=[("/anchor/.*", "202")]
        )

    @classmethod
    def tearDownAll(self):
        self.d.shutdown()

    def setUp(self):
        self.d.clear_log()

    def test_info(self):
        c = pathoc.Pathoc("127.0.0.1", self.d.port)
        c.connect()
        _, _, _, _, content = c.request("get:/api/info")
        assert tuple(json.loads(content)["version"]) == version.IVERSION

    def tval(self, requests, verbose=False):
        c = pathoc.Pathoc("127.0.0.1", self.d.port)
        c.connect()
        s = cStringIO.StringIO()
        c.print_requests(requests, verbose, s)
        return s.getvalue()

    def test_print_requests(self):
        reqs = [ "get:/api/info", "get:/api/info" ]
        assert self.tval(reqs, False).count("200") == 2
        assert self.tval(reqs, True).count("Date") == 2

    def test_parse_err(self):
        assert "Error parsing" in self.tval(["foo"])

    def test_conn_err(self):
        assert "Invalid server response" in self.tval(["get:'/p/200:d2'"])