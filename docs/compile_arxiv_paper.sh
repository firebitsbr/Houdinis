#!/bin/bash
# Houdinis Framework - arXiv Paper Compilation Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PAPER_SOURCE="arxiv_paper.tex"
OUTPUT_DIR="../output"
PAPER_NAME="houdinis_arxiv_paper"

echo -e "${BLUE}Houdinis Framework - arXiv Paper Compilation${NC}"
echo -e "${BLUE}=============================================${NC}"

# Check if LaTeX is installed
if ! command -v pdflatex &> /dev/null; then
    echo -e "${RED}[ERROR] pdflatex not found. Please install LaTeX distribution.${NC}"
    echo -e "${YELLOW}Ubuntu/Debian: sudo apt-get install texlive-full${NC}"
    echo -e "${YELLOW}CentOS/RHEL: sudo yum install texlive-scheme-full${NC}"
    exit 1
fi

echo -e "${GREEN}[INFO] LaTeX installation found${NC}"

# Check if source file exists
if [ ! -f "$PAPER_SOURCE" ]; then
    echo -e "${RED}[ERROR] Paper source file '$PAPER_SOURCE' not found${NC}"
    exit 1
fi

echo -e "${GREEN}[INFO] Paper source file found${NC}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Compile the paper
echo -e "${YELLOW}[BUILD] Compiling LaTeX paper...${NC}"

# First pass
echo -e "${BLUE}[BUILD] Running first pdflatex pass...${NC}"
pdflatex -output-directory="$OUTPUT_DIR" -interaction=nonstopmode "$PAPER_SOURCE" > "$OUTPUT_DIR/compile.log" 2>&1

# Second pass for references
echo -e "${BLUE}[BUILD] Running second pdflatex pass for references...${NC}"
pdflatex -output-directory="$OUTPUT_DIR" -interaction=nonstopmode "$PAPER_SOURCE" >> "$OUTPUT_DIR/compile.log" 2>&1

# Third pass to ensure everything is resolved
echo -e "${BLUE}[BUILD] Running final pdflatex pass...${NC}"
pdflatex -output-directory="$OUTPUT_DIR" -interaction=nonstopmode "$PAPER_SOURCE" >> "$OUTPUT_DIR/compile.log" 2>&1

# Check if compilation was successful
if [ -f "$OUTPUT_DIR/arxiv_paper.pdf" ]; then
    # Move and rename the output file
    mv "$OUTPUT_DIR/arxiv_paper.pdf" "$OUTPUT_DIR/${PAPER_NAME}.pdf"
    
    echo -e "${GREEN}[SUCCESS] Paper compiled successfully!${NC}"
    echo -e "${BLUE}[INFO] Output file: $OUTPUT_DIR/${PAPER_NAME}.pdf${NC}"
    
    # Show file information
    echo -e "${BLUE}[INFO] File size: $(du -h "$OUTPUT_DIR/${PAPER_NAME}.pdf" | cut -f1)${NC}"
    echo -e "${BLUE}[INFO] Pages: $(pdfinfo "$OUTPUT_DIR/${PAPER_NAME}.pdf" 2>/dev/null | grep Pages | awk '{print $2}' || echo "Unknown")${NC}"
    
    # Clean up auxiliary files
    echo -e "${YELLOW}[CLEAN] Removing auxiliary files...${NC}"
    rm -f "$OUTPUT_DIR"/*.aux "$OUTPUT_DIR"/*.log "$OUTPUT_DIR"/*.out "$OUTPUT_DIR"/*.toc "$OUTPUT_DIR"/*.bbl "$OUTPUT_DIR"/*.blg
    
    echo -e "${GREEN}[COMPLETE] arXiv paper ready for submission!${NC}"
    echo -e "${YELLOW}[NEXT] Review the generated PDF and follow the submission guide in README_ARXIV_SUBMISSION.md${NC}"
    
else
    echo -e "${RED}[ERROR] Paper compilation failed${NC}"
    echo -e "${YELLOW}[DEBUG] Check compilation log: $OUTPUT_DIR/compile.log${NC}"
    
    # Show last few lines of log for debugging
    if [ -f "$OUTPUT_DIR/compile.log" ]; then
        echo -e "${YELLOW}[DEBUG] Last 10 lines of compilation log:${NC}"
        tail -n 10 "$OUTPUT_DIR/compile.log"
    fi
    
    exit 1
fi

# Optional: Open PDF if on desktop environment
if command -v xdg-open &> /dev/null && [ -n "$DISPLAY" ]; then
    read -p "Would you like to open the PDF? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open "$OUTPUT_DIR/${PAPER_NAME}.pdf"
    fi
fi

echo -e "${BLUE}[INFO] Compilation complete. Files ready for arXiv submission.${NC}"
