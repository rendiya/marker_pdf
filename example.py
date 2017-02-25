from marker_pdf import MarkerPDF

marker = MarkerPDF(tmp_folder='tmp',ratio=10,delete_tmp=True) #ratio maker with percent 1-100
marker.create_marker(name='file.pdf',name_marker='marker.pdf')
marker.watermark(name='file.pdf',name_marker='marker.pdf')