# Anydoc Example Implementation

A command-line tool for converting various document formats to clean GitHub-Flavored Markdown using [Firecrawl's anydoc library](https://github.com/firecrawl/anydoc).

## Features

- Convert Word, PowerPoint, Excel, PDF, OpenDocument, RTF, EPUB, and CSV files to Markdown
- Automatic format detection from file content
- Optional OCR support for scanned PDFs
- Command-line interface with flexible arguments
- Save to file or output to console
- Preserves document structure (headings, tables, lists, code blocks, etc.)

## Supported Formats

| Format | Extensions |
|--------|-----------|
| Microsoft Word | `.docx`, `.doc` |
| Microsoft PowerPoint | `.pptx`, `.ppt` |
| Microsoft Excel | `.xlsx`, `.xls` |
| PDF | `.pdf` |
| OpenDocument | `.odt`, `.ods`, `.odp` |
| Rich Text Format | `.rtf` |
| EPUB | `.epub` |
| CSV | `.csv` |

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd anydoc-example
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up environment for OCR:
```bash
cp .env.example .env
# Edit .env and add your FIRECRAWL_API_KEY
```

## Usage

### Basic Usage

Place your documents in the `data/` folder and run:

```bash
python convert.py document.docx
```

This will print the converted Markdown to the console.

### Save to File

Use `--output auto` to automatically save to the `output/` folder:

```bash
python convert.py report.pdf --output auto
```

Or specify a custom output path:

```bash
python convert.py report.pdf --output /path/to/output.md
```

### Using Full Paths

You can also specify the full path to a document:

```bash
python convert.py /path/to/document.xlsx --output auto
```

### OCR for Scanned PDFs

Enable OCR for PDFs with scanned pages:

```bash
python convert.py scan.pdf --ocr hosted --output auto
```

**Note**: OCR requires a Firecrawl API key for higher rate limits. Set `FIRECRAWL_API_KEY` in your `.env` file.

### Force Format Detection

For files without clear signatures (like CSV), you can force the format:

```bash
python convert.py data.csv --format csv --output auto
```

### Verbose Mode

Enable detailed output during conversion:

```bash
python convert.py document.docx --output auto --verbose
```

## Command-Line Arguments

### Required Arguments

- `filename` - Document filename (searches in `data/` folder) or full path to the file

### Optional Arguments

- `-o, --output` - Output file path. Use `"auto"` to save in `output/` folder with the same name. If not specified, prints to console.
- `--ocr` - Enable OCR for scanned PDFs using Firecrawl Parse API. Options: `hosted`
- `-f, --format` - Force document format (useful for signature-less formats like CSV)
- `-v, --verbose` - Enable verbose output with detailed processing information

## Examples

### Example 1: Convert Word Document

```bash
# Place report.docx in data/ folder
python convert.py report.docx --output auto
# Output saved to output/report.md
```

### Example 2: Convert PDF with OCR

```bash
python convert.py scanned-invoice.pdf --ocr hosted --output auto
```

### Example 3: Convert and Print to Console

```bash
python convert.py presentation.pptx
```

### Example 4: Convert CSV with Format Hint

```bash
python convert.py sales-data.csv --format csv --output results.md
```

### Example 5: Convert from Absolute Path

```bash
python convert.py ~/Documents/important.xlsx --output auto --verbose
```

## Project Structure

```
anydoc-example/
├── data/                    # Place your input documents here
│   └── .gitkeep
├── output/                  # Converted markdown files (auto-generated)
│   └── .gitkeep
├── convert.py              # Main conversion script
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment configuration
├── .gitignore             # Git ignore patterns
└── README.md              # This file
```

## How It Works

1. **File Discovery**: The script searches for the input file in the `data/` folder or uses the full path if provided
2. **Format Detection**: Automatically detects the document format from file content signatures
3. **Conversion**: Uses the firecrawl-anydoc library to convert the document to clean GitHub-Flavored Markdown
4. **Output**: Either prints to console or saves to a file in the `output/` folder

## Features Preserved in Conversion

- Headings with anchor links
- Text styling (bold, italic, strikethrough)
- Code blocks with syntax highlighting hints
- Hyperlinks
- Lists (ordered, unordered, task lists)
- Tables (including merged cells)
- Block quotes
- Footnotes
- Equations (as LaTeX)
- Images (as alt text with raw bytes available)

## Environment Variables

- `FIRECRAWL_API_KEY` - Required for OCR functionality with higher rate limits. Get your API key from [Firecrawl](https://www.firecrawl.dev/)

## Troubleshooting

### File Not Found

If you get a "File not found" error:
- Make sure the file is in the `data/` folder, or
- Provide the full path to the file

### Import Error

If you get an import error for `anydoc`:
```bash
pip install -r requirements.txt
```

### OCR Rate Limits

If OCR hits rate limits:
- Set up your `FIRECRAWL_API_KEY` in the `.env` file
- The library includes a free tier with rate limits

## License

This example implementation is provided as-is for demonstration purposes. The underlying anydoc library is developed by [Firecrawl](https://github.com/firecrawl/anydoc).

## Contributing

Feel free to submit issues or pull requests to improve this example implementation.

## Resources

- [Anydoc GitHub Repository](https://github.com/firecrawl/anydoc)
- [Firecrawl Documentation](https://docs.firecrawl.dev/)
- [Python Package](https://pypi.org/project/firecrawl-anydoc/)
