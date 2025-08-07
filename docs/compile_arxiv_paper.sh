#!/bin/bash
# arXiv Paper Compilation and Submission Preparation Script
# Compiles the Houdinis Framework paper for arXiv submission

set -e

# Configuration
PAPER_NAME="arxiv_paper"
OUTPUT_DIR="arxiv_submission"
DOCS_DIR="/home/test/Downloads/Projetos/Houdinis/docs"

echo "===== arXiv Paper Compilation Script ====="
echo

# Check if we're in the right directory
if [ ! -f "$DOCS_DIR/${PAPER_NAME}.tex" ]; then
    echo "[ERROR] Paper source file not found: $DOCS_DIR/${PAPER_NAME}.tex"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo "[INFO] Created output directory: $OUTPUT_DIR"

# Copy paper source to output directory
cp "$DOCS_DIR/${PAPER_NAME}.tex" "$OUTPUT_DIR/"
echo "[INFO] Copied paper source to output directory"

# Change to output directory for compilation
cd "$OUTPUT_DIR"

echo "[INFO] Compiling LaTeX paper..."

# First compilation
pdflatex "${PAPER_NAME}.tex" > /dev/null 2>&1 || {
    echo "[ERROR] First pdflatex compilation failed"
    echo "Check the LaTeX source for errors"
    exit 1
}

# Second compilation for references
pdflatex "${PAPER_NAME}.tex" > /dev/null 2>&1 || {
    echo "[ERROR] Second pdflatex compilation failed"
    exit 1
}

echo "[SUCCESS] Paper compiled successfully!"
echo

# Check output file
if [ -f "${PAPER_NAME}.pdf" ]; then
    echo "[INFO] Generated PDF: ${OUTPUT_DIR}/${PAPER_NAME}.pdf"
    echo "[INFO] PDF size: $(du -h "${PAPER_NAME}.pdf" | cut -f1)"
    echo "[INFO] PDF pages: $(pdfinfo "${PAPER_NAME}.pdf" 2>/dev/null | grep Pages | awk '{print $2}' || echo "Unknown")"
else
    echo "[ERROR] PDF generation failed"
    exit 1
fi

# Clean up auxiliary files
echo "[INFO] Cleaning up auxiliary files..."
rm -f *.aux *.log *.out *.toc *.bbl *.blg

# Copy submission files
cp "$DOCS_DIR/README_ARXIV_SUBMISSION.md" ./
echo "[INFO] Copied submission README"

# Create submission package
echo "[INFO] Creating submission package..."
zip -q "${PAPER_NAME}_submission.zip" "${PAPER_NAME}.tex" "${PAPER_NAME}.pdf" "README_ARXIV_SUBMISSION.md"
echo "[SUCCESS] Created submission package: ${PAPER_NAME}_submission.zip"

echo
echo "===== Submission Summary ====="
echo "Paper Title: Houdinis Framework: A Comprehensive Quantum Cryptography"
echo "             Exploitation Platform for Post-Quantum Security Assessment"
echo "Author: Mauro Risonho de Paula Assumpção"
echo "Categories: cs.CR (primary), quant-ph, cs.ET"
echo "Files ready for arXiv submission:"
echo "  - ${PAPER_NAME}.tex (LaTeX source)"
echo "  - ${PAPER_NAME}.pdf (Compiled paper)"
echo "  - README_ARXIV_SUBMISSION.md (Submission guide)"
echo "  - ${PAPER_NAME}_submission.zip (Complete package)"
echo
echo "Next steps:"
echo "1. Review the compiled PDF"
echo "2. Visit https://arxiv.org/submit"
echo "3. Upload ${PAPER_NAME}.tex"
echo "4. Select categories and complete metadata"
echo "5. Submit for moderation"
echo
echo "[SUCCESS] arXiv submission preparation complete!"

# Return to original directory
cd - > /dev/null
