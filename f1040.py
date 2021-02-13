import pdfrw

pdf_str_encode = lambda x: pdfrw.objects.pdfstring.PdfString.encode(x)

class Person:

    def __init__(self):
        self.first_name = 'John'
        self.middle_name = 'Philip'
        self.last_name = 'Sousa'
        self.social_security_num = 'xxx-xxx-xxxx'
        self.home_street_address = '1600 Pennsylvania Av'
        self.home_apt_no = '1B'
        self.home_city = 'Washington, D.C.'
        self.state = 'DC'
        self.zip = '------'

class F1040:

    first_name_middle_init = 'FEFF00660031005F00300032005B0030005D'
    last_name = 'FEFF00660031005F00300033005B0030005D'
    home_street_address = 'FEFF00660031005F00300038005B0030005D'
    home_apt_no = 'FEFF00660031005F00300039005B0030005D'

    def __init__(self, head_of_household):
        self.F1040_template_path = 'templates/f1040.pdf'
        self.hoh = head_of_household

    def write_out(self):
        data = {}
        data[F1040.first_name_middle_init] = "{} {}.".format(self.hoh.first_name, self.hoh.middle_name[:1])
        data[F1040.last_name] = self.hoh.last_name
        data[F1040.home_street_address] = self.hoh.home_street_address
        data[F1040.home_apt_no] = self.hoh.home_apt_no

        template = pdfrw.PdfReader(self.F1040_template_path)
        annotations = [anno for page in template.pages for anno in page['/Annots']]
        for anno in annotations:
            key = anno['/T'][1:-1]
            if key in data:
                anno.update(pdfrw.PdfDict(V=pdf_str_encode(data[key])))
            else:
                anno.update(pdfrw.PdfDict(V=pdf_str_encode('')))
        template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write("ex55.pdf", template)

hoh = Person()
f1040 = F1040(hoh)
f1040.write_out()