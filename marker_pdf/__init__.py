import os,sys,os.path
import random,shutil
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

class MarkerPDF(object):
    def __init__(self,delete_tmp=False,tmp_folder='tmp',ratio=20):
        """init class for MarkerPDF with params:delete_tmp,tmp_folder,ratio:"""
        self.tmp_folder = tmp_folder
        self.dir_path = os.path.dirname(__file__)
        self.ratio = ratio
        self.delete_tmp = delete_tmp
        self.tmp_folder = tmp_folder
        self.merger = PdfFileMerger()
        try:
            if os.path.isfile('{tmp_folder}/__init__.py'.format(tmp_folder=tmp_folder)) is False:
                os.mkdir('{tmp_folder}'.format(tmp_folder=tmp_folder))
                open(os.path.join('{tmp_folder}'.format(tmp_folder=tmp_folder), '__init__.py'), "a")
        except Exception as e:
            pass
    def _delete_tmp(self):
        if self.delete_tmp == True:
            shutil.rmtree(self.tmp_folder)
        else:
            pass
    def _make_folder(self,name):
        name_folder = name.split('.')
        name_folder = name_folder[0]
        tmp_folder = self.tmp_folder
        try:
            if os.path.isfile('{tmp_folder}/{name_folder}/__init__.py'.format(tmp_folder=tmp_folder,name_folder=name_folder)) is False:
                os.mkdir('{tmp_folder}/{name_folder}'.format(tmp_folder=tmp_folder,name_folder=name_folder))
                open(os.path.join('{tmp_folder}/{name_folder}'.format(tmp_folder=tmp_folder,name_folder=name_folder), '__init__.py'), "a")
        except Exception as e:
            pass
    def _split(self,name):
        self._make_folder(name)
        name_folder = name.split('.')
        name_folder = name_folder[0]
        infile = PdfFileReader(open(name, 'rb'))
        for i in xrange(infile.getNumPages()):
            p = infile.getPage(i)
            outfile = PdfFileWriter()
            outfile.addPage(p)
            with open('{tmp_folder}/{name_folder}/{name}.pdf'.format(name = i,name_folder=name_folder,tmp_folder=self.tmp_folder), 'wb') as f:
                outfile.write(f)
    def _replace_marker(self,name,name_marker):
        name_folder = name.split('.')
        name_folder = name_folder[0]
        self._split(name)
        number = len(os.listdir('{tmp_folder}/{name_folder}'.format(tmp_folder=self.tmp_folder,name_folder=name_folder)))
        number = number-1
        ratio = (100/int(self.ratio))
        number_ratio = number/ratio
        print number_ratio
        random_page = []
        count = 0
        while count <= number_ratio:
            randomPDF = int(random.uniform(1, (number)))
            if randomPDF in random_page:
                pass
            else:
                random_page.append(randomPDF)
                shutil.copy(name_marker, "{tmp_folder}/{name_folder}/{name}.pdf".format(name=randomPDF,name_folder=name_folder,tmp_folder=self.tmp_folder))
                count = count +1
        
    def create_marker(self,name,name_marker,name_output=None):
        print "starting...."
        name_folder = name.split('.')
        name_folder = name_folder[0]
        self._replace_marker(name=name,name_marker=name_marker)
        if name_output == None:
            name_output = name.split('.')
            name_output = name_output[0]
        files = [x for x in os.listdir('{tmp_folder}/{name_folder}'.format(tmp_folder=self.tmp_folder,name_folder=name_folder)) if x.endswith('.pdf')]
        for fname in sorted(files):
            self.merger.append('{tmp_folder}/{name_folder}/{files}'.format(tmp_folder=self.tmp_folder,name_folder=name_folder,files=fname))
        self.merger.write("{name}-output.pdf".format(name=name_output))
        print "finish"
        self._delete_tmp()
    def watermark(self,name,name_marker,name_output=None):
        print "starting...."
        if name_output==None:
            name_output = name.split('.')
            name_output = '{name}-watermark.pdf'.format(name=name_output[0])

        output = PdfFileWriter()

        pdf = PdfFileReader(open(name, 'rb'))
        w_pdf = PdfFileReader(open(name_marker, 'rb'))
        watermark = w_pdf.getPage(0)

        for i in xrange(pdf.getNumPages()):
            page = pdf.getPage(i)
            page.mergePage(watermark)
            output.addPage(page)

        with open(name_output, 'wb') as f:
            output.write(f)
        print "success"