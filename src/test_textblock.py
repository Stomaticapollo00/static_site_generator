import unittest

from textblock import *

class TestTextBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype(self):
        textblock1 = "## heading"
        textblock2 = """```
print("hello world!")
```"""
        textblock3 = """>This is a quote.
>by Grog the Destroyer."""
        textblock4 = """- grocery list
- item 1
- item 2
- item 3"""
        textblock5 = """1. Ordered List
2. This includes a structure
3. Unlike, an unordered list"""
        textblock6 = """- No List here
I am just **highlighting** my text
with _dashes_ -"""
        textblock_type1 = block_to_blocktype(textblock1)
        textblock_type2 = block_to_blocktype(textblock2)
        textblock_type3 = block_to_blocktype(textblock3)
        textblock_type4 = block_to_blocktype(textblock4)
        textblock_type5 = block_to_blocktype(textblock5)
        textblock_type6 = block_to_blocktype(textblock6)
        self.assertEqual(textblock_type1, BlockType.HEADING)
        self.assertEqual(textblock_type2, BlockType.CODE)
        self.assertEqual(textblock_type3, BlockType.QUOTE)
        self.assertEqual(textblock_type4, BlockType.U_LIST)
        self.assertEqual(textblock_type5, BlockType.O_LIST)
        self.assertEqual(textblock_type6, BlockType.PARAGRAPH)
