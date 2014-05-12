from templateReplace import templateReplace
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BeamerPresentation:

    def __init__(self, title, name='Nick Edwards', institute='University of Edinburgh', email='nedwards@cern.ch', shorttitle=''):
        self.content = {}
        if not shorttitle: shorttile=title
        self.content['TITLE'] = title
        self.content['NAME'] = name
        self.content['INSTITUTE'] = institute
        self.content['EMAIL'] = email
        self.content['SHORTTITLE'] = shorttitle
        self.elements = []

    def add(self, element):
        self.elements.append( element )

    def writeTex(self, filename=''):
        bodytex = ""
        for elem in self.elements:
            bodytex += elem.tex() + "\n"
        self.content['BODY'] = bodytex
        template = ".".join(__file__.split("/")[:-1]) + "beamer_pres.template.tex"
        templateReplace(template, self.content, filename )

    def writePdf(self, filename=''):
        if '.pdf' in filename: filename=filename.replace('.pdf','')
        self.writeTex(filename+'.tex')
        os.system('pdflatex '+filename+'.tex')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BeamerSection:

    def __init__(self, title):
        self.title = title

    def tex(self):
        return "\\section{%s}" % (self.title)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BeamerSubSection:

    def __init__(self, title):
        self.title = title

    def tex(self):
        return "\\subsection{%s}" % (self.title)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BeamerSlide:

    def __init__(self, title):
        self.texstr = ""
        self.title = title
        pass

    def addText(self, text):
        self.texstr +=text+"\n"

    def addBullets(self, bullets):
        self.texstr += "\\begin{itemize}\n"
        for bullet in bullets:
            self.texstr += "\\item "+bullet+"\n"
        self.texstr += "\\end{itemize}\n"

    def addFigure(self, file, opts="", caption=None):
        self.texstr += "\\begin{figure}\n\\includegraphics[%s]{%s}\n" % (opts, file)
        if caption: self.texstr += "\\caption{%s}" % (caption,)
        self.texstr += "\\end{figure}\n"

    def _getFigureWidth(self, nFigs):
        if nFigs==1:
            return 0.9
        elif nFigs==2:
            return 0.47
        elif nFigs==3:
            return 0.32
        elif nFigs==4:
            return 0.4
        elif nFigs>6:
            return 0.24
        elif nFigs>4:
            return 0.32
        else:
            return 0.47

    def addFigures(self, files, captions=[], caption=None):
        self.texstr += "\\begin{figure}\n"
        if not len(captions):
            captions = ["",]*len(files)
        if len(captions) != len(files):
            raise RuntimeError("captions argument must be list of same length as files, or else an empty list")
        opts =  "width=%.2f\\textwidth" % self._getFigureWidth(len(files))
        for file, fig_caption in zip(files, captions):
            if fig_caption:
                fig_caption = "[%s]" % fig_caption
            self.texstr += "\\subfigure%s{\\includegraphics[%s]{%s}}\n" % (fig_caption, opts, file)
        if caption: self.texstr += "\\caption{%s}" % (caption,)
        self.texstr += "\\end{figure}\n"

    def tex(self):
        return "\\begin{frame}\n\\frametitle{%s}\n%s\\end{frame}" % (self.title, self.texstr)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BeamerBackupSection:
    def tex(self):
        str = """\section{Backup}
\\begin{frame}
\Huge{\centerline{The End}}
\end{frame} """
        return str
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    pres = BeamerPresentation("BeamerPresentation python module", shorttitle="BeamerPresentation")
    intro = BeamerSlide("Introduction")
    intro.addBullets(["Small python class for making presentations using the LaTeX beamer class", "Still being tested"])
    pres.add(intro)
    pres.add(BeamerSection("Examples"))
    slide1 = BeamerSlide("Some plots")
    slide1.addText("Look how nice the plots are!")
    slide1.addFigure("trk_z0_mc_perigee_z0_res_etaSingleSided.eps", "width=0.4\\textwidth")
    pres.add(slide1)
    for nPlots in range(1,20):
        slide = BeamerSlide("Some more plots")
        slide.addText("Looks very like the last one!")
        slide.addFigures(["trk_z0_mc_perigee_z0_res_etaSingleSided.eps",]*nPlots)
        pres.add(slide)
    pres.add(BeamerBackupSection())
    backup1 = BeamerSlide("A Bckup Slide")
    backup1.addText("No one looks at these!")
    pres.add(backup1)
    pres.writePdf("test")

