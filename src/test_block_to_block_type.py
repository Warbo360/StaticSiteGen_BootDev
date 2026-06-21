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

    def test_unordered_list(self):
        text1 = """- An unorder list
- An unordered list
- An unordered list"""
        text2 = """-I forgot the space to start this list!
- Unordered list
- Unordered list
- Unordered list"""
        self.assertEqual(block_to_block_type(text1), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(text2), BlockType.PARAGRAPH)

    def test_ordered_lists(self):
        text1 = """1. An ordered list here
2. An ordered list here
3. An ordered list here"""
        text2 = """1. An order list here
- Not an ordered list, this return false
3. This does not matter since the one before breaks the rules"""
        text3 = """10. An out of order list at the first element
2. This should return false
3. Should still return false"""
        text4 = """1. Testing string
3. Out of order string should return false
4. Should return false
"""
        text5 = """1. Just a single element ordered list with no line break"""
        text6 = 21
        text7 = """1 I forgot the period to make this a list
2. So this should return false
3. I'm really sure"""
                
        self.assertEqual(block_to_block_type(text1), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(text2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(text3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(text4), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(text5), BlockType.ORDERED_LIST)
        with self.assertRaises(TypeError):
            _ = block_to_block_type(text6)
        self.assertEqual(block_to_block_type(text7), BlockType.PARAGRAPH)

    def test_multiple_types(self):
        text1 = """# This is a heading for markdown"""
        text2 = """```
This is a code block
```"""
        text3 = """> This is a quote block
> I sure hope it returns a block quote"""
        text4 = """- This is an unorder list
- Unordered list preferably"""
        text5 = """1. This is an ordered list
2. This is the 2nd item in the ordered list
3. This is the 3rd item in the ordered list"""
        text6 = """# This is going to combine all of them and this should be a paragraph
```Python
This is totally real code
```
> NOw a quote block
> Now a quote block
- Now an unordered list
- More unordered list
1. Now an ordered list
2. The 2nd part"""
        self.assertEqual(block_to_block_type(text1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text2), BlockType.CODE)
        self.assertEqual(block_to_block_type(text3), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(text4), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(text5), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(text6), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
