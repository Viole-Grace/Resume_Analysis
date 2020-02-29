# from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage
# from io import BytesIO

# def pdf_to_text(path):

# 	manager = PDFResourceManager()
# 	retstr = BytesIO()
# 	layout = LAParams(all_texts=True)
# 	device = TextConverter(manager, retstr, laparams=layout)
# 	filepath = open(path, 'rb')
# 	interpreter = PDFPageInterpreter(manager, device)

# 	for page in PDFPage.get_pages(filepath, check_extractable=True):

# 		interpreter.process_page(page)
# 		text = retstr.getvalue()

# 	filepath.close()
# 	device.close()
# 	retstr.close()

# 	return text

# text = pdf_to_text('B.E. Project Synopis-converted.pdf')
# print(text)

import pdfminer
import os
import subprocess

def extract_data_from_file(filename='Resume-BE\ UPDATED\ Jan\ 2020.pdf', output_filename='extracted_data.txt'):

	command = 'pdf2txt.py -o {} {}'.format(output_filename,filename)
	os.system(command)
	# subprocess.call('pdf2txt.py -o {} {}'.format(output_filename,filename))

	return 0

extract_data_from_file()