from PyPDF2 import PdfReader
from typing import AnyStr
from gentopia.tools.basetool import *
import requests  
from io import BytesIO

class PDFReaderFromURLArgs(BaseModel):
    url: str = Field(..., description="URL of the PDF file to be read")

class PDFRead(BaseTool):
    """Tool that adds the capability to read PDF files from a URL and extract text."""

    name = "pdf_reader"
    description = "Reads a PDF file from a URL and extracts the text content."

    args_schema: Optional[Type[BaseModel]] = PDFReaderFromURLArgs

    def _run(self, url: AnyStr) -> str:
        try:
            # Download the PDF file from the URL
            response = requests.get(url)
            if response.status_code == 200:
                # Load the PDF content from bytes
                reader = PdfReader(BytesIO(response.content))
                text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text()
                return text
            else:
                return f"Failed to download PDF. Status code: {response.status_code}"
        except Exception as e:
            return f"Error reading PDF file from URL: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError