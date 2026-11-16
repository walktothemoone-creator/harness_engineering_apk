import tempfile, unittest
from decimal import Decimal
from pathlib import Path
from summarize import summarize, to_markdown

HERE = Path(__file__).parent


class T(unittest.TestCase):
    def test_sample(self):
        totals, skipped = summarize(HERE / "sample.csv")
        self.assertEqual(totals, {"apple": Decimal("220.00"), "banana": Decimal("100")})
        self.assertEqual(skipped, 1)

    def test_markdown_total(self):
        md = to_markdown({"a": Decimal("1.5"), "b": Decimal("2")}, 0)
        self.assertIn("| **all** | **3.5** |", md)

    def test_bad_header(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write("x,y\n1,2\n")
        with self.assertRaises(SystemExit):
            summarize(f.name)


if __name__ == "__main__":
    unittest.main()
