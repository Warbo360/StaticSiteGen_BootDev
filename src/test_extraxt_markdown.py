import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links

class TestMarkdownExtractImage(unittest.TestCase):
    def test_valid_pattern(self):
        pattern1 = "![ThisIsATest](https://ThisIsATest.png)"
        pattern2 = "![](https://TestingWithNoAltText)"
        pattern3 = "Some test text around the wanted pattern ![AltText](https://url.png) More test text"
        pattern4 = (
            "Some place holder text to imbed multiple pattern that should match ![AltText](https://url.png)"
            "This should result in 3 matches total so should be a list of 3 elements when this test case finishes"
            "![AltText2](https://url2.jpeg), then how about one more for good measure ![Alt3](https://url3.gif) some padding"
            "also for good measure I would say"
        )
        self.assertEqual(extract_markdown_images(pattern1), [("ThisIsATest", "https://ThisIsATest.png")])
        self.assertEqual(extract_markdown_images(pattern2), [("", "https://TestingWithNoAltText")])
        self.assertEqual(extract_markdown_images(pattern3), [("AltText", "https://url.png")])
        self.assertEqual(
            extract_markdown_images(pattern4),
            [
                ("AltText", "https://url.png"),
                ("AltText2", "https://url2.jpeg"),
                ("Alt3", "https://url3.gif")
            ]
        )

    def test_not_valid_pattern(self):
        pattern1 = "![nested[]](https:www.nestbrackets.com)"
        pattern2 = "[NormalLink](https:www.wrongelement!.com)"
        pattern3 = "![NestedParens](https://().com)"
        self.assertEqual(extract_markdown_images(pattern1), [])
        self.assertEqual(extract_markdown_images(pattern2), [])
        self.assertEqual(extract_markdown_images(pattern3), [])

    def test_type_error(self):
        invalid_int = 21
        invalid_float = 2.1
        invalid_list = ["words", 21, 2.1]
        invalid_dict = {"test": 21, "test2": 2.1}
        invalid_tuple = (1, 2, 3)
        invalid_set = {1, 2, 3, 4}
        invalid_bool = True
        invalid_None = None
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_int)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_float)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_list)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_dict)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_tuple)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_set)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_bool)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_None)

class TestMarkdownExtractLink(unittest.TestCase):
    def test_valid_pattern(self):
        pattern1 = "[AltText](https://linktoimage.png)"
        pattern3 = "[Alt1](https://linktoimage1.png) some test text [Alt2](https://linktoimage2.png)"
        self.assertEqual(extract_markdown_links(pattern1), [("AltText", "https://linktoimage.png")])
        self.assertEqual(extract_markdown_links(
            pattern3),
            [("Alt1", "https://linktoimage1.png"), ("Alt2", "https://linktoimage2.png")]
        )

    def test_not_valid_pattern(self):
        pattern1 = "[nested[]](https:www.nestbrackets.com)"
        pattern2 = "![NormalLink](https:www.wrongelement!.com)"
        pattern3 = "[NestedParens](https://().com)"
        self.assertEqual(extract_markdown_links(pattern1), [])
        self.assertEqual(extract_markdown_links(pattern2), [])
        self.assertEqual(extract_markdown_links(pattern3), [])


    def test_type_error(self):
        invalid_int = 21
        invalid_float = 2.1
        invalid_list = ["words", 21, 2.1]
        invalid_dict = {"test": 21, "test2": 2.1}
        invalid_tuple = (1, 2, 3)
        invalid_set = {1, 2, 3, 4}
        invalid_bool = True
        invalid_None = None
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_int)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_float)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_list)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_dict)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_tuple)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_set)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_bool)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_None)

if __name__ == "__main__":
    unittest.main()
