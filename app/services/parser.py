from io import BytesIO
import docx
from pypdf import PdfReader

class FileParser:
    @staticmethod
    def parse_file(file_contents: bytes, filename: str) -> str:
        """Parse PDF or DOCX file and return text content"""
        if filename.endswith('.pdf'):
            return FileParser._parse_pdf(file_contents)
        
        if filename.endswith('.docx'):
            return FileParser._parse_docx(file_contents)
        else:
            raise ValueError("Unsupported file format. Please upload PDF or DOCX.")
    
    @staticmethod
    def _parse_pdf(file_contents: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdffile = BytesIO(file_contents)
            reader = PdfReader(pdffile)
            text = ""
            for pages in reader.pages:
                text += pages.extract_text()
            return text
        
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    @staticmethod
    def _parse_docx(file_contents: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            docxfile = BytesIO(file_contents)
            doc = docx.Document(docxfile)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX: {str(e)}")
