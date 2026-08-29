#!/usr/bin/env python3
"""
Anydoc Example - Document to Markdown Converter

This script converts various document formats (Word, PowerPoint, Excel, PDF, etc.)
to clean GitHub-Flavored Markdown using the firecrawl-anydoc library.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import anydoc
except ImportError:
    print("Error: firecrawl-anydoc is not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is optional, continue without it
    pass


def find_input_file(filename: str) -> Path:
    """
    Find the input file. If it's not an absolute path, look in the data/ folder.

    Args:
        filename: Filename or path to the document

    Returns:
        Path object to the file

    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    file_path = Path(filename)

    # If absolute path or relative path that exists, use it directly
    if file_path.is_absolute() or file_path.exists():
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filename}")
        return file_path

    # Otherwise, look in the data/ folder
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    data_file = data_dir / filename

    if data_file.exists():
        return data_file

    raise FileNotFoundError(
        f"File not found: {filename}\n"
        f"Searched in:\n"
        f"  - Current directory: {file_path.absolute()}\n"
        f"  - Data directory: {data_file.absolute()}"
    )


def get_output_path(input_path: Path, output_arg: Optional[str]) -> Optional[Path]:
    """
    Determine the output path for the markdown file.

    Args:
        input_path: Path to the input file
        output_arg: Output argument from command line

    Returns:
        Path object for output file, or None if outputting to console
    """
    if output_arg is None:
        return None

    if output_arg == "auto":
        # Auto-generate output filename in output/ folder
        script_dir = Path(__file__).parent
        output_dir = script_dir / "output"
        output_dir.mkdir(exist_ok=True)

        # Change extension to .md
        output_filename = input_path.stem + ".md"
        return output_dir / output_filename

    # Use specified output path
    return Path(output_arg)


def convert_document(
    input_path: Path,
    ocr: Optional[str] = None,
    format_hint: Optional[str] = None
) -> str:
    """
    Convert a document to Markdown using anydoc.

    Args:
        input_path: Path to the input document
        ocr: OCR mode ("hosted" or None)
        format_hint: Optional format hint for signature-less formats

    Returns:
        Markdown string

    Raises:
        Exception: If conversion fails
    """
    try:
        # Read file content
        with open(input_path, 'rb') as f:
            file_bytes = f.read()

        # Detect format
        detected_format = anydoc.format_from_bytes(file_bytes)
        if detected_format:
            print(f"Detected format: {detected_format}", file=sys.stderr)
        elif format_hint:
            print(f"Using format hint: {format_hint}", file=sys.stderr)
        else:
            print("Warning: Could not detect format from content", file=sys.stderr)

        # Convert to markdown
        if ocr:
            # Check if FIRECRAWL_API_KEY is set
            if not os.getenv('FIRECRAWL_API_KEY'):
                print(
                    "Warning: FIRECRAWL_API_KEY not set. OCR may have rate limits.\n"
                    "Set the API key in .env file or environment variable.",
                    file=sys.stderr
                )
            markdown = anydoc.to_markdown_bytes(
                file_bytes,
                format_hint or detected_format,
                ocr=ocr
            )
        else:
            markdown = anydoc.to_markdown_bytes(
                file_bytes,
                format_hint or detected_format
            )

        return markdown

    except Exception as e:
        raise Exception(f"Conversion failed: {str(e)}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Convert documents to Markdown using anydoc',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.docx
  %(prog)s report.pdf --output auto
  %(prog)s scan.pdf --ocr hosted --output auto
  %(prog)s data.csv --format csv --output results.md
  %(prog)s /path/to/file.xlsx --output auto

Supported formats:
  Word (.docx, .doc), PowerPoint (.pptx, .ppt), Excel (.xlsx, .xls),
  PDF (.pdf), OpenDocument (.odt, .ods, .odp), RTF (.rtf),
  EPUB (.epub), CSV (.csv)
        """
    )

    parser.add_argument(
        'filename',
        help='Document filename (in data/ folder) or full path to the file'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file path. Use "auto" to save in output/ folder with same name. '
             'If not specified, prints to console.',
        default=None
    )

    parser.add_argument(
        '--ocr',
        choices=['hosted'],
        help='Enable OCR for scanned PDFs using Firecrawl Parse API',
        default=None
    )

    parser.add_argument(
        '-f', '--format',
        help='Force document format (useful for signature-less formats like CSV)',
        default=None
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    try:
        # Find input file
        if args.verbose:
            print(f"Searching for file: {args.filename}", file=sys.stderr)

        input_path = find_input_file(args.filename)

        if args.verbose:
            print(f"Found file: {input_path}", file=sys.stderr)
            print(f"File size: {input_path.stat().st_size:,} bytes", file=sys.stderr)

        # Convert document
        print(f"Converting {input_path.name}...", file=sys.stderr)
        markdown = convert_document(input_path, args.ocr, args.format)

        # Determine output
        output_path = get_output_path(input_path, args.output)

        if output_path:
            # Save to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"Successfully saved to: {output_path}", file=sys.stderr)
        else:
            # Print to console
            print("\n" + "="*80, file=sys.stderr)
            print("MARKDOWN OUTPUT:", file=sys.stderr)
            print("="*80 + "\n", file=sys.stderr)
            print(markdown)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
