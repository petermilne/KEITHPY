#!/usr/bin/python

# This is a demo of creating a pdf file with several pages.

import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

a = np.arange(1,100)

# Create the PdfPages object to which we will save the pages:
# The with statement makes sure that the PdfPages object is closed properly at
# the end of the block, even if an Exception occurs.
pdf =  PdfPages('test_pdf.pdf')
plt.figure(figsize=(3, 3))
plt.plot(a,a, 'r-o')
plt.title('Test PDF')
pdf.savefig()  # saves the current figure into a pdf page
plt.close()

plt.figure(figsize=(8, 6))
plt.plot(a,a)
plt.title('Page Two')
pdf.savefig()
plt.close()

fig = plt.figure(figsize=(4, 5))
plt.plot(a,a, 'r-o')
plt.title('Page Three')
pdf.savefig(fig)  # or you can pass a Figure object to pdf.savefig
plt.close()

pdf.close()

'''
    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Multipage PDF Example'
    d['Author'] = u'Jouni K. Sepp\xe4nen'
    d['Subject'] = 'How to create a multipage pdf file and set its metadata'
    d['Keywords'] = 'PdfPages multipage keywords author title subject'
    d['CreationDate'] = datetime.datetime(2009, 11, 13)
    d['ModDate'] = datetime.datetime.today()
'''
