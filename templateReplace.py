
def templateReplace(template, content, ofilename=None ):
    filestr = file(template).read()
    for key, val in content.iteritems():
        if not "$"+key+"$" in filestr:
            print "WARNING: key %s not found in template %s" % (key, template)
        else:
            filestr = filestr.replace('$'+key+'$', val)
    if not ofilename:
        return filestr
    ofile = file(ofilename, 'w')
    ofile.write(filestr)
    ofile.flush()
    ofile.close()
    
