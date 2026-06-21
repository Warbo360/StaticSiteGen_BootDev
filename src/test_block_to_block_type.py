import unittest
from textnode import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        text1 = "## This is a heading"
        text2 = "This is a normal paragraph block"
        text3 = "####### This has too many \"#\" to be a heading block and should be a paragraph one instead"
        text4 = "##" 
        # Want to see how this evals personally, evals to a paragraph, need to rework func to allow for empty headings
        # For now works just fine
        self.assertEqual(block_to_block_type(text1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(text3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(text4), BlockType.PARAGRAPH)

    def test_code(self):
        text1 ="""```
This is a code block and should be could and return BlockType.CODE
```"""
        text2 = """```
This is a example of a multi-line code block that should still return
BlockType.CODE, it would really suck if it did not
```"""
        text3 = """```
This is an example of a code block that is not closed and should return as just a paragraph"""
        text4 = """```

```"""
        text5 = """```
```"""
        text6 = """```Python
This is an example of a code block with an identifying language added
```"""
        self.assertEqual(block_to_block_type(text1), BlockType.CODE)
        self.assertEqual(block_to_block_type(text2), BlockType.CODE)
        self.assertEqual(block_to_block_type(text3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(text4), BlockType.CODE)
        self.assertEqual(block_to_block_type(text5), BlockType.CODE)
        self.assertEqual(block_to_block_type(text6), BlockType.CODE)

    def test_quote(self):
        text1 = """> Some quote text
> Some quote text
> Some more quote text"""
        text2 = """>Some quote text
> Some quote text
>Some quote text
> Some quote text
>
>
>
>
"""
        text3 = """> Some quote text
Not quote text here
> Some quote text"""
        text4 = """>A quote that goes here"""
        self.assertEqual(block_to_block_type(text1), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(text2), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(text3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(text4), BlockType.QUOTE)

if __name__ == "__main__":
    unittest.main()
